from threading import Thread
from lib.utils import save_result


class Writer(Thread):

    def __init__(self, w_queue, filename):
        Thread.__init__(self)
        self.w_queue = w_queue
        self.filename = filename

    def run(self):
        while True:
            url = self.w_queue.get()
            save_result(url, self.filename)