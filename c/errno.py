#!/usr/bin/python3

import os, sys
import argparse
from string import Template
from operator import itemgetter
from collections import namedtuple

Error = namedtuple('Error', ('name', 'code', 'description'))

macro_errname = '''
#define ERRORS_GET(CODE)
    (
        (CODE >= ERRORS_MIN && CODE <= ERRORS_MAX) ?
           ($ERRORS[CODE - ERRORS_MIN] ?
            $ERRORS[CODE - ERRORS_MIN] :
            $UNKNOWN_ERROR) :
        $UNKNOWN_ERROR
    )
'''

def parseErrorLine(line):
    name, code, desc = line.split(' ', 2)
    return Error(name, int(code), desc)

errors = filter(None, os.popen('errno -l').read(-1).split('\n'))
errors = map(parseErrorLine, errors)
errors = list(errors)
names = list(map(itemgetter(0), errors))

parser = argparse.ArgumentParser(description='generate error')
parser.add_argument('--null-value', default='0', help='use this as NULL value')
parser.add_argument('--unknown-error', default='"UNKNOWN"', help='...')
parser.add_argument('--var',  default='ERRORS', help='use this variable for array')
parser.add_argument('--no-e', dest='offset', help='strip leading E', action='store_const', const=1, default=0)
parser.add_argument('--only', nargs='+', help='only export these', choices=names)
parser.add_argument('--strip', action='store_true')
parser.add_argument('--comment', action='store_true')
args = parser.parse_args()

print("//", ' '.join(sys.argv), '\n')

errors.sort(key=itemgetter(1))
max_errno = errors[-1].code
errors_size = max_errno + 1

if args.only:
    errors = list(filter(lambda e: e.name in args.only, errors))

def fillTemplate(s):
    return Template(s).substitute(UNKNOWN_ERROR=args.unknown_error, ERRORS=args.var)

def printT(s):
    print(fillTemplate(s))

def printMacro(s):
    s = fillTemplate(s)
    lines = s.strip().split('\n')
    last = lines.pop(-1)
    for l in lines:
        print(l, '\\')
    print(last)

if args.strip:
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
    printMacro(macro_errname)

else:
    XX = [args.null_value] * errors_size
    for error in errors:
        XX[error.code] = '"%s"' % error.name[args.offset:]

    printT("#define ${ERRORS}_SIZE %d" % (errors_size))
    print()
    printT("const char * $ERRORS[%d] = { %s };" % (errors_size, ', '.join(XX)))
    print()
