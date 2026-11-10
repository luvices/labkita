import sys
import time
from vncdotool import api

client = api.connect('127.0.0.1::5900')

def press_char(ch):
    shift_map = {
        '_': 'minus', '+': 'equal', ':': 'semicolon', '"': 'apostrophe',
        '<': 'comma', '>': 'period', '?': 'slash', '~': 'grave',
        '!': '1', '@': '2', '#': '3', '$': '4', '%': '5',
        '^': '6', '&': '7', '*': '8', '(': '9', ')': '0',
        '{': 'bracketleft', '}': 'bracketright', '|': 'backslash'
    }
    char_map = {
        ' ': 'space', '-': 'minus', '=': 'equal', ';': 'semicolon',
        "'": 'apostrophe', ',': 'comma', '.': 'period', '/': 'slash',
        '`': 'grave', '[': 'bracketleft', ']': 'bracketright', '\\': 'backslash'
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
    elif arg.startswith('mouse:'):
        x, y = map(int, arg[6:].split(','))
        client.mouseMove(x, y)
        client.mousePress(1)
