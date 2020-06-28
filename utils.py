# -*- coding: utf-8 -*-
import requests
import datetime
import json
from weather import Weather
from io import StringIO
from config import tasksLink

def getUrlContent(url):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.text
    return None

def getBuySellPair(currency):
    url = 'https://minfin.com.ua/currency/auction/%s/buy/lvov/' % currency
    content = getUrlContent(url)
    if content is None: return (0, 0)

    keyword = '</small>'
    pos = content.index(keyword) + len(keyword)
    end_pos = content.index('<', pos)
    buy = content[pos:end_pos].strip()

    pos = content.index(keyword, end_pos) + len(keyword)
    end_pos = content.index('<', pos)
    sell = content[pos:end_pos].strip()

    return (buy, sell)

def getCurrencyInfo():
    output = 'USD. Buy: %s, Sell: %s' % getBuySellPair('usd')
    output += '\nEUR. Buy: %s, Sell: %s' % getBuySellPair('eur')
    return output

def getCurrentTime():
    currentDT = datetime.datetime.now()
    return "%02d:%02d" % (currentDT.hour, currentDT.minute)

def getWeatherInfo():
    weather = Weather()
    return "%0.0f °C, %s" % (weather.getTemperature(), weather.getStatus())

def getTasksInfo():
    url = tasksLink
    content = getUrlContent(url)
    if content is None: return 'No active tasks!'
    tasks = json.loads(content)

    output = ''
    for task in tasks:
        id = task['e_id']
        name = task['e_name']
        desc = task['e_desc']
        time = task['e_time']
        output += "Task: %s: %s -- %s.\n" % (name, desc, time)

    if len(output) == 0: output = 'No active tasks!'
        
    return output

if __name__ == '__main__':
    print(123)