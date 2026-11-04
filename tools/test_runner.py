import sys
import time
from vncdotool import api

client = api.connect('127.0.0.1::5900')

def type_cmd(s):
    for ch in s:
        if ch == ' ':
            client.keyPress('space')
        elif ch == '-':
            client.keyPress('minus')
        elif ch == '/':
            client.keyPress('fslash')
        elif ch == '&':
            client.keyDown('shift')
            client.keyPress('7')
            client.keyUp('shift')
        elif ch == '>':
            client.keyDown('shift')
            client.keyPress('.')
            client.keyUp('shift')
        elif ch == '|':
            client.keyDown('shift')
            client.keyPress('bslash')
            client.keyUp('shift')
        elif ch.isupper():
            client.keyDown('shift')
            client.keyPress(ch.lower())
            client.keyUp('shift')
        else:
            client.keyPress(ch)
        time.sleep(0.01)
    client.keyPress('return')

for arg in sys.argv[1:]:
    if arg.startswith('type:'):
        type_cmd(arg[5:])
    elif arg.startswith('pause:'):
        time.sleep(float(arg[6:]))
    elif arg.startswith('capture:'):
        client.captureScreen(arg[8:])
    elif arg.startswith('key:'):
        client.keyPress(arg[4:])
