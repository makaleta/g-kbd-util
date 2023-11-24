#!/usr/bin/env python3

import os
from time import sleep


def g513_led(command):
    os.system(f"g513-led {command}")


def get_numlock_status():
    xset_output = os.popen("xset q").read().strip().split()
    return xset_output[xset_output.index("Num") + 2] == "on"


def get_numlock_change():
    numlock_on = get_numlock_status()
    if numlock_on != get_numlock_change.last:
        get_numlock_change.last = numlock_on
        return numlock_on


get_numlock_change.last = None


def show_numlock_status(numlock_on: bool | None):
    if numlock_on is None:
        return
    elif numlock_on:
        g513_led("-g numeric a04000")
    else:
        g513_led("-g numeric 000000")
        for key in ["2", "4", "6", "8", "lock", "0", "."]:
            g513_led(f"-kn num{key} 999999")
        g513_led("-c")


while True:
    show_numlock_status(get_numlock_change())
    sleep(0.9)
    pass
