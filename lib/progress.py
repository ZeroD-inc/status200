from progressbar import ProgressBar
from threading import Thread


class Progress(Thread):

    def __init__(self, maxvalue, progress):
        Thread.__init__(self)
        self.maxvalue = maxvalue
        self.bar = ProgressBar(maxval=maxvalue).start()
        self.progress = progress

    def run(self):
        x = 0
        while x <= self.maxvalue:
            self.bar.update(x)
            x += self.progress.get()
        self.bar.finish()
