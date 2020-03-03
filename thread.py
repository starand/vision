# -*- coding: utf-8 -*-
import threading
import time

class Thread(threading.Thread):
    _exitFlag = False
    _delay = 60

    def __init__(self, name, delay=2):
        threading.Thread.__init__(self)
        self._name = name
        self._delay = delay

    def start(self):
        threading.Thread.start(self)
        print("[%s] has started" % self._name)

    def stop(self):
        self._exitFlag = True

    def run(self):
        while not self._exitFlag:
            self.do_run()
            time.sleep(self._delay)

        print("[%s] has stopped" % self._name)

    def do_run(self):
        print('do nothing')


if __name__ == '__main__':
    notifier = Thread('test')
    notifier.start()

    time.sleep(10)
    notifier.stop()

    notifier.join()