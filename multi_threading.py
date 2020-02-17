import logging
from threading import Thread


class MyWorker(Thread):
    def __init__(self, queue, func_run):
        Thread.__init__(self)
        self.queue = queue
        self.func_run = func_run

    def run(self):
        while True:
            data = self.queue.get()

            try:
                self.func_run(data)
            finally:
                self.queue.task_done()

