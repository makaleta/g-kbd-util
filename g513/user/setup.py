#!/usr/bin/env python3

import os
from time import sleep

COLOR = "a04000"
COLOR_INACTIVE = "000000"
COLOR_ALT = "999999"
COLOR_INDICATOR = "f01020"


def g513_led(command):
    os.system(f"g513-led {command}")


def lock_status(xset_output, key):
    return xset_output[xset_output.index(key) + 2] == "on"


def get_statuses():
    xset_output = os.popen("xset q").read().strip().split()
    return (
        lock_status(xset_output, "Caps"),
        lock_status(xset_output, "Num"),
        lock_status(xset_output, "Scroll"),
    )


def get_changes():
    states = get_statuses()
    changes = (
        None if curr == last else curr for curr, last in zip(states, get_changes.last)
    )
    get_changes.last = states
    return changes


get_changes.last = (None, None, None)


def show_capslock_status(capslock_on: bool | None):
    if capslock_on is None:
        return
    elif capslock_on:
        g513_led(f"-k shiftl {COLOR_INDICATOR}")
    else:
        g513_led(f"-k shiftl {COLOR}")

def show_numlock_status(numlock_on: bool | None):
    if numlock_on is None:
        return
    elif numlock_on:
        g513_led(f"-g numeric {COLOR}")
    else:
        g513_led(f"-g numeric {COLOR_INACTIVE}")
        for key in ["2", "4", "6", "8", "lock", "0", "."]:
            g513_led(f"-kn num{key} {COLOR_ALT}")
        g513_led("-c")
def show_scrolllock_status(scrolllock_on: bool | None):
    if scrolllock_on is None:
        return
    elif scrolllock_on:
        g513_led(f"-k scroll_lock {COLOR_INDICATOR}")
    else:
        g513_led(f"-k scroll_lock {COLOR}")

while True:
    changes = get_changes()
    show_capslock_status(next(changes))
    show_numlock_status(next(changes))
    show_scrolllock_status(next(changes))
    sleep(0.9)
    pass
