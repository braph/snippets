#!/usr/bin/python3

{
    'try_': 'raise Exception',
    '':     'return None'
}

{
    'eat': 
     1}


template_re = {'''
try:
    m = pattern.match(self.s, self.pos)
    self.pos = m.regs[0][1]
    return m[0]
except AttributeError:
    return None
''',

_return='


template_str = '''
if self.s.startswith(string, self.pos):
    return string
else:
    raise Exception
'''


template = '''
def {name}(self, {arg}):
    \'\'\' {doc} \'\'\'
    {init}
    {true}
    {false}
'''

for try_prefix in ('', 'try_'):
    for func_type in ('read', 'peek', 'eat'):
        for match_type in ('str', 're'):
            name = '%s%s_%s' % (try_prefix, func_type, match_type)
            arg = ('string' if match_type == 'str' else 'pattern'),
            on_error = ('raise Exception' if try_prefix else 'return None')




            print(template.format(
                name=name, arg=arg, doc='',







def generate():
    pass

    def read_str(string):
        ''' Read string from token stream, return it. Exception if not found. '''
        if self.s.startswith(string, self.pos):
            self.pos += len(string)
            return string
        else:
            raise Exception
