from thread import Thread
from tgbot import bot

import time
import utils
import config

class Notifier(Thread):
    _regularTimeNotifications = {}

    def __init__(self, name, delay=2):
        Thread.__init__(self, name, delay)

    def do_run(self):
        time = utils.getCurrentTime()
        #print(time)
        for t in self._regularTimeNotifications:
            #print(' -- %s' % t)
            if t == time:
                for task in self._regularTimeNotifications[time]:
                    bot.sendMessage(config.recepient, task())
                    print("[%s] \'%s\' task executed" % (self._name, task.__name__))
        
    def add_daily_task(self, time, task):
        entry = self._regularTimeNotifications.get(time)
        if entry is None: entry = list()

        entry.append(task)
        print("[%s] \'%s\' task added" % (self._name, task.__name__))
        self._regularTimeNotifications[time] = entry
        
    def del_regular_notification(self, time, task):
        pass


if __name__ == '__main__':
    ## add notifications
    notifier = Notifier('notifier', 10)
    notifier.add_daily_task("14:27", utils.getCurrencyInfo)
    notifier.start()

    time.sleep(10)
    notifier.stop()

    notifier.join()