#!/usr/bin/python3

import os
import argparse
from operator import itemgetter

def parseErrorLine(line):
    name, code, desc = line.split(' ', 2)
    return (name, int(code), desc)

errors = filter(None, os.popen('errno -l').read(-1).split('\n'))
errors = map(parseErrorLine, errors)
errors = list(errors)
names = list(map(itemgetter(0), errors))

parser = argparse.ArgumentParser(description='generate error')
parser.add_argument('--var',  default='ERRORS', help='use this variable for array')
parser.add_argument('--only', nargs='+', help='only export these', choices=names)
args = parser.parse_args()

errors.sort(key=itemgetter(1))
max_errno = errors[-1][1] #max(errors, key=itemgetter(1))[1]
errors_size = max_errno + 1

XX = ['NULL'] * errors_size
for error in errors:
    if not args.only or error[0] in args.only:
        XX[error[1]] = '"%s"' % error[0]

print("#define %s_SIZE %d" % (args.var.upper(), errors_size))
print("const char *%s[%d] = {" % (args.var, errors_size))
print(', '.join(XX))
print("};")

