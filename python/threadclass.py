#!/usr/bin/python3

from threading import Thread
from queue import Queue
from time import sleep

class ThreadPoolThread(Thread):
    def __init__(self, **kwargs):
        self.queue = kwargs.pop('queue')
        self.result = kwargs.pop('result')
        self._kwargs = {}
        Thread.__init__(self, **kwargs)
        self.queue.put(self)

    def run(self):
        try:
            self.result.put( self._target(*self._args, **self._kwargs) )
        finally:
            self.queue.get()

q = Queue(5)
r = Queue()

def test(*args):
    print(*args)
    sleep(3)
    return args

for i in range(16):
    thr = ThreadPoolThread(target=test, args=(i,), queue=q, result=r)
    thr.start()


while True:
    print(r.get_nowait())
