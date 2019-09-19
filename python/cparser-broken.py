#!/usr/bin/python3

import sys, re

precedence = re.escape('''\
&& || <<= >>= <= >= == != -= += *= /= %= &= ^= |= ++ -- ** // /* */
 << >> ->''').replace('\\ ', '|')
precedence += '|\\\\.'            # Escape sequences (`.` must match newline!)
precedence += '|[\\w_][\\w\\d_]*' # Identifiers
syntax     = '''[](){}<>&|:;!?=+-*/'"#`$%~,^'''
pattern    = '%s|[^%s\\s]+|[%s]|\n|\\s+' % (
    precedence, re.escape(syntax), re.escape(syntax)
)

isnumber = re.compile('-?\\d+')

class Tokenizer():
    ''' Tokenizer class.  '''

    def __init__(self, s):
        self.ungetted = []
        s = re.sub('\\\\n', '', s)
        self.tokenit = Tokenizer.basic_tokenize(s)
        self.line_count = 1

    def __iter__(self):
        return self

    def __next__(self):
        try:               tok = self.ungetted.pop(0)
        except IndexError: tok = next(self.tokenit)
        self.line_count += '\n' in tok
        return tok

    @staticmethod
    def basic_tokenize(s):
        return iter(re.findall(pattern, s))#, re.DOTALL))

    def peek(self, idx=0):
        while True:
            try:
                return self.ungetted[idx]
            except IndexError:
                self.ungetted.append(next(self.tokenit))

    def unget(self, token):
        self.ungetted.insert(0, token)

    def SynError(self, m):
        return Exception("Syntax Error on line %s: %s" % (self.line_count, m))



class Base():
    def __init__(self, parent, children=None):
        try:    assert(isinstance(parent, Base))
        except: raise Exception(self.__class__)
        self.parent   = parent
        self.children = children or []

    #def __repr__(self):
    #    return '<%s %s>' % (
    #        str(self.__class__).split('.')[1].split("'")[0], repr(self.children))

    def __repr__(self):
        return self.repr2()

    def repr2(self, i=0):
        cname = str(self.__class__).split('.')[1].split("'")[0]
        r = '%s<%s ' % (' ' * i, cname)
        for c in self.children:
            if isinstance(c, Base):
                r2 = c.repr2(i+1)
            else:
                r2 = c.strip()

            if len(r2) < 70:
                r += ' ' + r2
            else:
                r += '\n%s%s' % (' ' * i, r2)
        r+='>\n'
        return r

        return '%s<%s %s>' % (
            '  '*i, cname, repr(self.children, i + 1))

    def __iter__(self):
        return iter(self.children)

    def getiterator(self): # Explicit version, since ``str`` is also iterable
        return iter(self.children)

    def finalize(self):
        pass

    def to_c(self):
        pass

    def getlast(self):      return self.children[-1]
    def setlast(self,v):    self.children[-1] = v
    last = property(fget=getlast, fset=setlast)


# =============================================================================
# === Grammar stuff ===========================================================
# =============================================================================

# All possible tokens can be found in this list.
# ``ANY`` is just an alias for ``GRAMMAR``.
GRAMMAR = ANY = []
SUBSTITUTABLE = []
CODEBLOCKS    = []

# === Token Classes ===========================================================
class Script(Base):
    def __init__(self, parent, children=None):
        self.parent = parent
        self.children = children or []
class SingleQuoted(Base):                       pass
class DoubleQuoted(Base):                       pass
class CommandSubstitution(Base):                pass
class Comment(Base):                            pass
class Command(Base):                            pass
class SubShell(Base):                           pass
class Backquote(Base):                          pass
class CommandGroup(Base):                       pass
class BraceExpansion(Base):                     pass
class TildeExpansion(Base):                     pass
class Assignment(Base):                         pass
class DoubleTest(Base):                         pass
class SingleTest(Base):                         pass
class Arithmetic(Base):                         pass
class ArithmeticSubst(Base):                    pass
class EscapedString(Base):                      pass
class GettextString(Base):                      pass

# === Control Operators =======================================================
# TODO: OP ( )
class ControlOperator(Base):                    pass # <BASE CLASS>
class ControlOr(ControlOperator):               pass # ||
class ControlBg(ControlOperator):               pass # &
class ControlAnd(ControlOperator):              pass # &&
class ControlTerm(ControlOperator):             pass # ; <newline>
class ControlCaseTerm(ControlOperator):         pass # ;;
class ControlCaseFallThrough(ControlOperator):  pass # ;&
class ControlCaseTestNext(ControlOperator):     pass # ;;&
class ControlPipe(ControlOperator):             pass # |
class ControlPipeErr(ControlOperator):          pass # |&


# =============================================================================
# === Parsing Rules ===========================================================
# =============================================================================
class AllowedFactory():
    objects = {}

    @staticmethod
    def get(parsers):
        o =     AllowedSubtokens(parsers)
        try:    AllowedFactory.objects[id(parsers)].append(o)
        except: AllowedFactory.objects[id(parsers)] = [o]
        return o

    @staticmethod
    def setup():
        for allowed_objs in AllowedFactory.objects.values():
            dicted = {}
            if allowed_objs[0].parsers is not None: #TODO?
                for p in allowed_objs[0].parsers:
                    try:    dicted[p.start].append(p)
                    except: dicted[p.start] = [p]

            for o in allowed_objs:
                o.parsers = dicted

        AllowedFactory.objects.clear()

class AllowedSubtokens(): # TODO: subparses group
    '''
    This class is used for choosing an appropriate rule from a set of rules.

    For faster access, all possible rules are summarized in a dictionary
    of the form:
        {<Start Token>: <Possible Rule> ...}

    Since the list of allowed parsers will change during the creation of the
    grammar and many parsing rules share the same set of allowed parsers,
    AllowedFactory.setup() will setupt the dictionary.
    '''
    __slots__ = ('parsers',)
    def __init__(self, parsers):
        self.parsers = parsers 

    def getparser(self, token, tokenizer, parentklass):
        for rule in self.parsers.get(token, ()):
            if rule.match(token, tokenizer, parentklass):
                return rule
        return None


class RuleBase():
    '''
    Base class for a rule.
    Each Rule must have a ``start`` field, containing the first matching tag.
    Matching can be refined using the ``match`` method
    '''
    def match(*a):
        return True

class OneTokenRule(RuleBase):
    '''
    This is used for parsing only a single token
    '''
    def __init__(self, token, klass):
        self.start = token
        self.klass = klass

    def parse(self, token, tokenizer, parentklass):
        return self.klass(parentklass)

class GroupedRule(RuleBase):
    '''
    This is used for matching everything from a single ``start`` token
    to an ``end`` token.
    '''
    __slots__  =   ('klass','start','subparsers','end')
    def __init__(self, klass, start, subparsers, end):
        self.klass = klass
        self.start = start
        self.end   = end
        if subparsers is not None:
            self.subparsers = AllowedFactory.get(subparsers)
        else:
            self.subparsers = None

    def parse(self, token, tokens, parentklass):
        klass = self.klass(parentklass, [token])
        rule = None
        for tok in tokens:
            #print(repr(tok))
            if self.end == tok:
                return klass

            if self.subparsers is not None:
                rule = self.subparsers.getparser(tok, tokens, klass)

            if rule:
                klass.children.append( rule.parse(tok, tokens, klass) )
            else:
                klass.children.append(tok)

        if self.end is None:
            return klass
        raise tokens.SynError("%s: Expected: ``%s``" % (klass, self.end))


#OPs = {
#    '||':   ControlOr,      '&&':   ControlAnd,
#    '&':    ControlBg,      ';':    ControlTerm,
#    '\n':   ControlTerm,    ';;':   ControlCaseTerm,
#    '|':    ControlPipe,    '|&':   ControlPipeErr,
#    ';&':   ControlCaseFallThrough,
#    ';;&':  ControlCaseTestNext
#}
#
## Simple, One-Token Rules
#CONTROL_OPERATORS = [
#    OneTokenRule(token, klass) for token, klass in OPs.items()
#]

# Simple Grouping Rules
_ = lambda *args: GroupedRule(*args)
ScriptRule              = _(Script,               None,   ANY,             None)
DoubleQuotedRule        = _(DoubleQuoted,         '"',    None,   '"')
#SubShellRule            = _(SubShell,             '(',    ANY,             ')')
#DoubleTestRule          = _(DoubleTest,           '[[',   SUBSTITUTABLE,   ']]')
#SingleTestRule          = _(SingleTest,           '[',    SUBSTITUTABLE,   ']')
#ArithmeticRule          = _(Arithmetic,           '((',   SUBSTITUTABLE,   '))')
#CommandSubstitutionRule = _(CommandSubstitution,  '$(',   ANY,             ')')
#ArithmeticSubstRule     = _(ArithmeticSubst,      '$((',  SUBSTITUTABLE,   '))')
#VariableAdvRule         = _(Variable,             '${',   SUBSTITUTABLE,   '}')
#EscapedStringRule       = _(EscapedString,        "$'",   None,            "'")
#GettextStringRule       = _(GettextString,        '$"',   SUBSTITUTABLE,   '"')

# Now we have access to the Rules
#SUBSTITUTABLE.extend([
#    VariableRule, VariableAdvRule,
#    BackquoteRule, CommandSubstitutionRule, ArithmeticSubstRule,
#    EscapedStringRule, # TODO: EscapedString are not valid in ""
#    GettextStringRule
#])

#GRAMMAR.extend(CONTROL_OPERATORS)
GRAMMAR.extend([
    ScriptRule,
    #DoubleQuotedRule
])

AllowedFactory.setup()

def parse(s):
    tokenizer = Tokenizer(s)
    tok = next(tokenizer)
    return ScriptRule.parse(tok, tokenizer, None)

with open(sys.argv[1], 'r') as fh:
    s = fh.read()

grouped = parse(s)

for c in grouped.children:
    print(c)
