# -*- coding: utf-8 -*-
import requests
import time
import json
import inspect

import fileutils
import config

class TelegramBot:
    _token = ""
    _id_file = "last_id"
    _last_id = 0
    _cmd_registry = {}

    def __init__(self, token):
        self._token = token
        self._last_id = fileutils.loadLastUpdateId(self._id_file)
        print("[Bot] started. Last update id: %s" % self._last_id)

    def getUpdates(self):
        url = "https://api.telegram.org/bot" + self._token + "/getUpdates"
        try:
            response = requests.get(url)
            return response.json()
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            print("Connection issue")
        return None

    def sendMessageGet(self, chat_id, msg):
        url = 'https://api.telegram.org/bot' + self._token + '/sendMessage?chat_id=' + str(chat_id) + '&parse_mode=Markdown&text=' + msg
        response = requests.get(url)
        return response.json()

    ## send photo via POST method
    def sendPhoto(self, chat_id, url_img, caption=""):
        url = 'https://api.telegram.org/bot' + self._token + '/sendPhoto'
        data = {'chat_id': chat_id, 'photo': url_img, 'caption': caption, 'parse_mode': 'html', 'disable_notification': True}
        return requests.post(url, data=data)


    ## POST message
    def sendMessage(self, chat_id, msg, markup=None):
        url = 'https://api.telegram.org/bot' + self._token + '/sendMessage'
        data = {'chat_id': chat_id, 'text': msg, 'parse_mode': 'html', 'disable_notification': True}

        if markup is not None:
            data['reply_markup'] = json.dumps(markup)
        # { 'inline_keyboard': [[ { 'text' : 'Visit Unofficed', 'url': 'http://unofficed.com'} ]] }
        return requests.post(url, data=data)

    def process_updates(self):
        updates = self.getUpdates()
        if not updates: return # netowrk issue
        status = updates['ok']
        if not status:
            print("[Bot] Failed to parse updates json")
        else:
            updates = updates['result']
            for update in updates: self.process(update)

            if fileutils.loadLastUpdateId(self._id_file) != self._last_id:
                fileutils.storeLastUpdateId(self._id_file, self._last_id)

    def run(self):
        while True:
            self.process_updates()
            time.sleep(1)

    def process(self, update):
        _last_id = update['update_id']
        if self._last_id >= _last_id: return
        self._last_id = _last_id

        message = update.get('message')
        if message is not None:
            if message['text'][0] == '/': self.process_cmd(message)
            else: self.process_msg(message)
        
        query = update.get('callback_query')
        if query:
            print(query)

    ## process message from update
    def process_msg(self, message):
        chat_id = message['chat']['id']
        text = message['text']
        self.sendMessage(chat_id, "Hello " + text)
        print("[Bot] Processing message (%d): %s" % (self._last_id, text))

    ## process command from update
    def process_cmd(self, message):
        chat_id = message['chat']['id']
        name = message['text'][1:] # get command without slash
        cmd = self._cmd_registry.get(name)
        if cmd is not None:
            name, desc, func, kb = cmd
            self.sendMessage(chat_id, func(message), kb)
            print("[Bot] \'%s\' command executed (%d)" % (name, self._last_id))

    ## add bot command
    def register_cmd(self, name, desc, func, kb=None):
        command = self._cmd_registry.get(name)
        if command is None:
            self._cmd_registry[name] = (name, desc, func, kb)
            print("[Bot] \'%s\' comamnd added" % name)

    def get_cmd_list(self):
        return self._cmd_registry.items()

bot = TelegramBot(config.token)

def bot_command(function):
    name = function.__name__
    desc = inspect.signature(function).parameters['desc'].default
    kb = inspect.signature(function).parameters.get('kb')
    if (kb is not None): kb = kb.default
    bot.register_cmd(name, desc, function, kb)
