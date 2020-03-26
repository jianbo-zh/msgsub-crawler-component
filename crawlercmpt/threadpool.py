import queue
import threading

class threadPoolManager():
    '''
    线程池管理
    '''
    def __init__(self, thread_count=1, queue_maxsize=10):
        self.thread_count = thread_count
        self.thread_list = []
        self.work_queue = queue.Queue(queue_maxsize)
        self.flag = {"is_running": True}

        for i in range(thread_count):
            t = threadManager(i, self.work_queue, self.flag)
            t.start()
            self.thread_list.append(t)

    def add_work(self, func, *args):
        '''
        添加任务
        '''
        if not self.flag['is_running']:
            raise RuntimeError("thread pool is closed")

        self.work_queue.put((func, args))

    def close_thread_pool(self):
        '''
        关闭进程池
        '''
        self.flag['is_running'] = False
        print("close pool")
        for t in self.thread_list:
            t.join()


class threadManager(threading.Thread):
    '''
    线程处理任务队列
    '''
    def __init__(self, thread_id, work_queue, flag):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.work_queue = work_queue
        self.flag = flag

    def run(self):
        while self.flag['is_running']:
            try:
                func, args = self.work_queue.get(timeout=3)
            except:
                pass
            else:
                func(*args)
                self.work_queue.task_done()