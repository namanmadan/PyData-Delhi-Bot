from telegram.ext import Updater, CommandHandler
from telegram import ChatAction
from datetime import datetime, timedelta
from pytz import timezone
from time import sleep
import logging
import requests
import pytz
import re
import ast
import os
import json
import sys
import signal
import subprocess

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

"""
---Process ID Management Starts---
This part of the code helps out when you want to run your program in background using '&'. This will save the process id of the program going in background in a file named 'pid'. Now, when you run you program again, the last one will be terminated with the help of pid. If in case the no process exist with given process id, simply the `pid` file will be deleted and a new one with current pid will be created.
"""
currentPID = os.getpid()
if 'pid' not in os.listdir():
    with open('pid', mode='w') as f:
        print(str(currentPID), file=f)
else:
    with open('pid', mode='r') as f:
        try:
            os.kill(int(f.read()), signal.SIGTERM)
            print("Terminating previous instance of " +
                  os.path.realpath(__file__))
        except ProcessLookupError:
            subprocess.run(['rm', 'pid'])
    with open('pid', mode='w') as f:
        print(str(currentPID), file=f)
"""
---Process ID Management Ends---
"""

"""
---Token/Key Management Starts---
This part will check for the config.txt file which holds the Telegram and Meetup Token/Key and will also give a user friendly message if they are invalid. New file is created if not present in the project directory.
"""
configError = "Please open config.txt file located in the project directory and relace the value '0' of Telegram-Bot-Token with the Token you recieved from botfather and similarly for Meetup-API-Key"
if 'config.txt' not in os.listdir():
    with open('config.txt', mode='w') as f:
        json.dump({'Telegram-Bot-Token': 0, 'Meetup-API-Key': 0}, f)
        print(configError)
        sys.exit(0)
else:
    with open('config.txt', mode='r') as f:
        config = json.loads(f.read())
        if config["Telegram-Bot-Token"] or config["Meetup-API-Key"]:
            print("Token Present, continuing...")
            TelegramBotToken = config["Telegram-Bot-Token"]
            MeetupAPIKey = config["Meetup-API-Key"]
        else:
            print(configError)
            sys.exit(0)
"""
---Token/Key Management Ends---
"""

updater = Updater(token=TelegramBotToken)
dispatcher = updater.dispatcher

meetupApi = {'sign': 'true', 'key': MeetupAPIKey}

utc = pytz.utc

print("I'm On..!!")

def start(bot, update, args):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='''
Hi! My powers are solely for the service of PyData Delhi Community
Use /help to get /help''')

def website(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='https://pydatadelhi.github.io/ (WIP)')

def twitter(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='http://twitter.com/pydatadelhi')

def meetup(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id,text='https://www.meetup.com/PyDataDelhi/')

def nextmeetup(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        r=requests.get('http://api.meetup.com/PyDataDelhi/events', params=meetupApi)
        #print(r.json()[0])
        event_link=r.json()[0]['link']
        date_time=r.json()[0]['time']//1000
        utc_dt = utc.localize(datetime.utcfromtimestamp(date_time))
        indian_tz = timezone('Asia/Kolkata')
        date_time=utc_dt.astimezone(indian_tz)
        date_time=date_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        if 'venue' in r.json()[0]:
                venue=r.json()[0]['venue']['address_1']
                bot.sendLocation(chat_id=update.message.chat_id, latitude=r.json()[0]['venue']['lat'],longitude=r.json()[0]['venue']['lon'])
        else:
                venue='Venue is still to be decided'
        bot.sendMessage(chat_id=update.message.chat_id, text='''
Next Meetup
Date/Time : %s
Venue : %s
Event Page : %s
'''%(date_time, venue, event_link))

def nextmeetups(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        r=requests.get('http://api.meetup.com/PyDataDelhi/events', params=meetupApi)
        #print(re.sub('</a>','',re.sub('<a href="','',re.sub('<br/>',' ',re.sub('<p>',' ',re.sub('</p>','\n',r.json()[0]['description']))))))
        bot.sendMessage(chat_id=update.message.chat_id, text='''
Next Meetup Schedule
%s
'''%(re.sub('</a>','',re.sub('<a href="','',re.sub('<br/>',' ',re.sub('<p>',' ',re.sub('</p>','\n',r.json()[0]['description'])))))),parse_mode='HTML')

def facebook(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id, text='https://www.facebook.com/pydatadelhi')

def github(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id, text='https://github.com/pydatadelhi')

def invitelink(bot,update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        sleep(0.2)
        bot.sendMessage(chat_id=update.message.chat_id, text='https://t.me/joinchat/B71pNUGrUQ7QHuyUJq-Ajg')

def help(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
	sleep(0.2)
	bot.sendMessage(chat_id=update.message.chat_id, text='''
Use one of the following commands
/twitter - to get PyData Delhi Twitter link
/meetuppage - to get a link to PyData Delhi Meetup page
/nextmeetup - to get info about next Meetup
/nextmeetupschedule - to get schedule of next Meetup
/facebook - to get a link to PyData Delhi Facebook page
/github - to get a link to PyData Delhi Github page
/website - to get the website of PyData Delhi
/invitelink - to get an invite link for PyData Delhi Telegram Group of Volunteers
/help - to see recursion in action ;)

To contribute to|modify this bot : https://github.com/realslimshanky/PyData-Delhi-Bot
''')

dispatcher.add_handler(CommandHandler('start', start, pass_args=True))
dispatcher.add_handler(CommandHandler('website', website))
dispatcher.add_handler(CommandHandler('twitter', twitter))
dispatcher.add_handler(CommandHandler('meetuppage', meetup))
dispatcher.add_handler(CommandHandler('nextmeetup', nextmeetup))
dispatcher.add_handler(CommandHandler('nextmeetupschedule', nextmeetups))
dispatcher.add_handler(CommandHandler('facebook', facebook))
dispatcher.add_handler(CommandHandler('github', github))
dispatcher.add_handler(CommandHandler('invitelink', invitelink))
dispatcher.add_handler(CommandHandler('help', help))

updater.start_polling()
