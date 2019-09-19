#!/usr/bin/python3
import re, itertools, threading, time
lock = threading.Lock()

with open('DOCNEW', 'r') as fh:
    cnt = fh.read()

with open('/usr/share/dict/german', 'r') as fh:
    dct = fh.read().lower()

#dct = dct.split()

cnt = cnt.replace('!', '')
cnt = cnt.replace(',', '')
wrds = re.split('[\n ]', cnt)
cs = set(cnt)
cs.remove(' ')
cs.remove('\n')
print(cs)
wsre = re.compile('\\s+')

crange = [ chr(c) for c in range(ord('a'), ord('z')+1) ]
#crange.extend([ chr(c) for c in range(ord('A'), ord('Z')+1) ])

cranges = []
for i in range(0, len(crange)):
    cranges.append(crange[i:] + crange[:i])

csstr = ''.join(cs)
csords = list(map(ord, cs))
def solve(t, r):
    for pm in itertools.permutations(r, len(cs)):
        #trans = ''.maketrans(csstr, ''.join(pm))
        trans = dict(zip(csords,pm))
        #print(trans)
        #print(trans2)
        #print(localwrds)
        #print(pm)
        count = 0
        for wrd in wsre.split(cnt.translate(trans)):
            if '\n%s\n'%wrd in dct:
                count +=1

        localwrds = None
        if count >= 4:
            localwrds = wsre.split(cnt.translate(trans))
            with lock:
                print("%d) Matched %d: key: %s wrds: %s" %(t, count, trans, localwrds))

thrds = []
for i, r in enumerate(cranges):
    r = list(map(ord,r))
    thrd = threading.Thread(target=solve, args=(i,r))
    thrds.append(thrd)
    thrd.start()

for thrd in thrds:
    thrd.join()
