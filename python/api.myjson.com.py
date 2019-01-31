#!/usr/bin/python3

import time
import json
import requests
from queue import Queue
from threading import Thread

url = 'http://api.myjson.com/bins/' # 5 *
# https://api.myjson.com/bins/ncAes

def getChars(*args):
    args = iter(args)
    for c1 in args:
        c2 = next(args)
        for c in range(ord(c1), ord(c2) + 1):
            yield chr(c)

def GC2(num, *args):
    for s in getChars(*args):
        if num == 1:
            yield s
        else:
            for c in GC2(num - 1, *args):
                yield s + c

#for c in getChars('a', 'z', 'A', 'Z', '1', '9'):
#    pass

q = Queue(200)

def get(code):
    try:
        print(code, end=' ', flush=True)
        res = requests.get(url + code)

        try:
            if 'This website is under heavy load' in res.text:
                q.put(1) # retry
                time.sleep(3)
                return get(code)
            if json.loads(res.text).get("status", 0) == 404:
                return
        except:
            pass

        with open("%s.json" % (code), 'w') as fh:
            fh.write(res.text)
    finally:
        q.get()

def run(code):
    q.put(1)
    thr = Thread(target=get, args=(code, ))
    thr.start()

for s in GC2(5, 'a', 'z', 'A', 'Z', '1', '9'):
    run(s)


#print(list(getChars('a', 'c', '1', '3')))
#print(list(GC2(2, 'a', 'c')))
