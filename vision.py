#!/usr/bin/python3

from tgbot import *
import utils
from notifier import Notifier
from weather import Weather
import os

@bot_command
def start(message, desc='to start conversation', kb= {
        'inline_keyboard': [[
            { 'text' : 'Currency', 'callback_data': '/currency_query'},
            { 'text' : 'Tasks', 'callback_data': '/tasks_query'},
            { 'text' : 'Weather', 'callback_data': '/weather_query'}
        ]]
    }):
    return "To start work with helper, use the following commands:"

@bot_query
def currency_query(msg, desc='Currency query handler'):
    return utils.getCurrencyInfo()

@bot_query
def tasks_query(msg, desc='Tasks query handler'):
    return utils.getTasksInfo()

@bot_query
def weather_query(msg, desc='Weather query handler'):
    return utils.getWeatherInfo()

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

@bot_command
def fx(msg, desc='Forex commands', kb= {
        'inline_keyboard': [[
            { 'text' : 'Today', 'callback_data': '/fxtoday_query'},
            { 'text' : 'History', 'callback_data': '/fxhistory_query'}
        ]]
    }):
    return "Select command:"


@bot_query
def tasks_query(msg, desc='Tasks query handler'):
    return utils.getTasksInfo()


if __name__ == '__main__':
    print(os.path.dirname(os.path.realpath(__file__)))
    ## add notifications
    notifier = Notifier('notifier', 60) # run check once per minute
    notifier.add_daily_task("07:10", utils.getWeatherInfo)
    notifier.add_daily_task("07:10", utils.getCurrencyInfo)
    notifier.add_daily_task("07:10", utils.getTasksInfo)

    #notifier.add_daily_task("14:43", utils.getCurrentTime)
    notifier.start()

    bot.run()

    # wait for all threads to stop
    notifier.stop()
    notifier.join()

