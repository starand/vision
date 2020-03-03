from tgbot import *
import utils
from notifier import Notifier
from weather import Weather

@bot_command
def start(message, desc='to start conversation', kb= {
        'inline_keyboard': [[ { 'text' : 'currency', 'callback_data': '/currency'} ]] 
    }):
    return "an int"

@bot_command
def cmdlist(message, desc='returns command list'):
    return "\n".join(map(lambda x: "%s - %s" % (x[0], x[1][1]), bot.get_cmd_list()))

@bot_command
def weather(message, desc='returns weather information'):
    weather = Weather()
    res = bot.sendPhoto(message['chat']['id'], weather.getIcon(), utils.getWeatherInfo())
    return ""

@bot_command
def currency(message, desc='returns currency rates'):
    return utils.getCurrencyInfo()

@bot_command
def tasks(message, desc='returns todays tasks'):
    return utils.getTasksInfo()

if __name__ == '__main__':
    ## add notifications
    notifier = Notifier('notifier', 60) # run check once per minute
    notifier.add_daily_task("07:10", utils.getCurrencyInfo)
    notifier.add_daily_task("07:10", utils.getTasksInfo)

    #notifier.add_daily_task("14:43", utils.getCurrentTime)
    notifier.start()

    bot.run()

    # wait for all threads to stop
    notifier.stop()
    notifier.join()

