from queue import Queue
from threading import Thread


class SimpleThreading():
    def __init__(self, num_threads=-1):
        self.results = Queue()
        self.threads = Queue(num_threads)

    def create_threaded_func(self, func):
        def thread_func(*args, **kwargs):
            try:        self.results.put(func(*args, **kwargs))
            finally:    self.threads.get()

        def thread_func_start(*args, **kwargs):
            thr = Thread(target=thread_func, args=args, kwargs=kwargs)
            self.threads.put(thr)
            thr.start()

        #return thread_func_start
        self.threaded_func = thread_func_start
        return self.threaded_func

    def yield_queue_results(self, background_thread=None):
        if bg_thr:
            bg_thr_is_alive = lambda: bg_thr.is_alive()
        else:
            bg_thr_is_alive = lambda: False

        while True:
            try:   yield self.results.get(True, 1)
            except GeneratorExit: return
            except Exception:     pass

            if (not bg_thr_is_alive() and
                    self.results.qsize() == 0 and
                    self.threads.qsize() == 0):
                break

        while True:
            try:   yield self.results.get_nowait()
            except GeneratorExit: return
            except Exception:     break



def getThread_2(board, thread):
    return getJson(thread_url % (board, thread))


st = SimpleThreading(100)
func = st.create_threaded_func( getThread_2 )

def getAllThreadsOfBoard_2(board):
    catalog = getCatalog(board)
    for cata in catalog:
        for thread in cata['threads']:
            try:
                func('b', thread['no'])
            except Exception as e:
                print(e)

bg_thr = Thread(target=getAllThreadsOfBoard_2, args=('b',))
bg_thr.start()

alls = list(st.yield_queue_results(bg_thr))

