#!/usr/bin/python3

import os, sys
import argparse
from string import Template
from operator import itemgetter
from collections import namedtuple

Error = namedtuple('Error', ('name', 'code', 'description'))
def parseErrorLine(line):
    name, code, desc = line.split(' ', 2)
    return Error(name, int(code), desc)

macro_errors_get = '''
#define ERRORS_GET(CODE)
    (
        (CODE >= ${ERRORS}_MIN && CODE <= ${ERRORS}_MAX) ?
           ($ERRORS[CODE - ${ERRORS}_MIN] ?
            $ERRORS[CODE - ${ERRORS}_MIN] :
            $UNKNOWN_ERROR) :
        $UNKNOWN_ERROR
    )
'''

optStrError = 'strerror(CODE)'
optDynamic  = None

def optFixedString(s):
    return '"%s"' % s

def optDynamicString(s):
    global optDynamic
    optDynamic = 'char ${ERRORS}_UNKNOWN[%d];' % (len(s) + 2)
    return '(sprintf(${ERRORS}_UNKNOWN, "%s", CODE), ${ERRORS}_UNKNOWN)' % s

errors = filter(None, os.popen('errno -l').read(-1).split('\n'))
errors = map(parseErrorLine, errors)
errors = list(errors)
names =  list(map(itemgetter(0), errors))

parser = argparse.ArgumentParser(description='generate error names for C')
parser.add_argument('--var',  default='ERRORS', help='use this variable for array')
parser.add_argument('--no-e', dest='offset',    help='strip leading E', action='store_const', const=1, default=0)
parser.add_argument('--null-value', default='0', help='use this as NULL value')

group = parser.add_argument_group('Unknown error', 'What to return if errorcode was not found in array')
group = group.add_mutually_exclusive_group()
group.add_argument('--null', dest='unknown_error', action='store_const', const='NULL',
    help='Return NULL')
group.add_argument('--fixed-string', dest='unknown_error', default='UNKNOWN', type=optFixedString,
    help='Return a fixed string')
group.add_argument('--strerror',     dest='unknown_error', action='store_const', const=optStrError,
    help='Return the result of ' + optStrError)
group.add_argument('--dynamic',      dest='unknown_error', type=optDynamicString,
    help='Return a dynamic string. (add %%d for code)')

parser.add_argument('--only', nargs='+', help='only export these', choices=names, metavar='ERROR')
parser.add_argument('--simple',   action='store_true', help='Simple')
#parser.add_argument('--comment', action='store_true')
args = parser.parse_args()

errors.sort(key=itemgetter(1))
max_errno = errors[-1].code
errors_size = max_errno + 1

if args.only:
    errors = list(filter(lambda e: e.name in args.only, errors))

def fillTemplate(s):
    return Template(s).substitute(
        UNKNOWN_ERROR=Template(args.unknown_error).substitute(ERRORS=args.var),
        ERRORS=args.var
    )

def printT(s):
    print(fillTemplate(s))

def printMacro(s):
    lines = fillTemplate(s).strip().split('\n')
    last  = lines.pop(-1)
    for l in lines:
        print(l, '\\')
    print(last)


# ==== begin output ====

print("//", ' '.join(sys.argv), '\n')

if args.simple:
    XX = [args.null_value] * errors_size
    for error in errors:
        XX[error.code] = '"%s"' % error.name[args.offset:]

    printT("#define ${ERRORS}_SIZE %d" % (errors_size))
    print()
    printT("const char * $ERRORS[%d] = { %s };" % (errors_size, ', '.join(XX)))
    print()

else:
    min_errno = errors[0].code
    max_errno = errors[-1].code
    errors_size = max_errno - min_errno + 1

    XX = [args.null_value] * errors_size
    for error in errors:
        XX[error.code - min_errno] = '"%s"' % error.name[args.offset:]
        
    printT("#define ${ERRORS}_SIZE %d" % (errors_size))
    printT("#define ${ERRORS}_MIN  %d" % (min_errno))
    printT("#define ${ERRORS}_MAX  %d" % (max_errno))
    print()
    printT("const char * $ERRORS[%d] = { %s };" % (errors_size, ', '.join(XX)))
    print()

    if optDynamic:
        printT(optDynamic)
        print()

    printMacro(macro_errors_get)
