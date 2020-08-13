from botToken import token
from src.bot import bot

import signal
import sys

def signal_handler(signal, frame):
    print ('You pressed Ctrl+C - or killed me with -2')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
# print 'Press Ctrl+C'
# signal.pause()

bot.run(token)