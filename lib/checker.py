from threading import Thread
from lib.utils import do_requests


class Check(Thread):

    def __init__(self, u_queue, w_queue, progress, timeout):
        Thread.__init__(self)
        self.u_queue = u_queue
        self.w_queue = w_queue
        self.progress = progress
        self.timeout = timeout

    def run(self):
        while True:
            url = self.u_queue.get()
            do_requests(url, self.w_queue, self.timeout)
            self.u_queue.task_done()
            self.progress.put(1)
