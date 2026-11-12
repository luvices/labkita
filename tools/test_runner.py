import os
import sys
import time
from vncdotool import api

client = api.connect('127.0.0.1::5900')

def press_char(ch):
    shift_map = {
        '_': 'minus', '+': '=', ':': ';', '"': "'",
        '<': ',', '>': '.', '?': 'fslash', '~': '`',
        '!': '1', '@': '2', '#': '3', '$': '4', '%': '5',
        '^': '6', '&': '7', '*': '8', '(': '9', ')': '0',
        '{': '[', '}': ']', '|': 'bslash'
    }
    char_map = {
        ' ': 'space', '-': 'minus', '/': 'fslash', '\\': 'bslash'
    }

    if ch in shift_map:
        client.keyDown('shift')
        client.keyPress(shift_map[ch])
        client.keyUp('shift')
    elif ch in char_map:
        client.keyPress(char_map[ch])
    elif ch.isupper():
        client.keyDown('shift')
        client.keyPress(ch.lower())
        client.keyUp('shift')
    else:
        client.keyPress(ch)
    time.sleep(0.015)

def type_cmd(s):
    for ch in s:
        press_char(ch)
    client.keyPress('return')

for arg in sys.argv[1:]:
    if arg.startswith('type:'):
        type_cmd(arg[5:])
    elif arg.startswith('rawtype:'):
        for ch in arg[8:]:
            press_char(ch)
    elif arg.startswith('envtype:'):
        val = os.environ[arg[8:]]
        type_cmd(val)
    elif arg.startswith('envrawtype:'):
        val = os.environ[arg[11:]]
        for ch in val:
            press_char(ch)
    elif arg.startswith('pause:'):
        time.sleep(float(arg[6:]))
    elif arg.startswith('capture:'):
        client.captureScreen(arg[8:])
    elif arg.startswith('key:'):
        k = arg[4:]
        if k == 'backspace': k = 'bsp'
        client.keyPress(k)
    elif arg.startswith('combo:'):
        keys = [('bsp' if x == 'backspace' else x) for x in arg[6:].split('-')]
        for k in keys[:-1]:
            client.keyDown(k)
        client.keyPress(keys[-1])
        for k in reversed(keys[:-1]):
            client.keyUp(k)
    elif arg.startswith('mouse:') or arg.startswith('click:'):
        x, y = map(int, arg.split(':')[1].split(','))
        client.mouseMove(x, y)
        time.sleep(0.1)
        client.mouseDown(1)
        time.sleep(0.1)
        client.mouseUp(1)
