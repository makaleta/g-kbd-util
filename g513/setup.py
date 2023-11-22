#!/usr/bin/env python3

import os
import sys
from time import sleep

COLOR = "a04000"
COLOR_USED = "00a000"
COLOR_CACHE = "0000a0"
COLOR_SYS = "a00000"


MEM_TOTAL = int(os.popen("vmstat -SM -s | head -1 | sed 's/[^0-9]//g'").read().strip())


def g513_led(command):
    os.system(f"g513-led {command}")


def numlock_status():
    num_lock_status = (
        os.popen("xset -q | sed -n 's/^.*Num Lock:\s*\(\S*\).*$/\1/p'").read().strip()
    )
    if num_lock_status == "on":
        g513_led("numeric 999999")
    else:
        g513_led("numeric 000000")


def sysstats():
    sysstat = os.popen("vmstat -y -SM | tail -n 1").read().strip().split()
    mem_free = int(sysstat[3])
    mem_cache = int(sysstat[5])
    sys_sys = int(sysstat[13])
    sys_idle = int(sysstat[14])
    sys_sys_blocks = int((sys_sys / 100) * 9)
    sys_used_blocks = 9 - int((sys_idle / 100) * 9)
    mem_nonused_blocks = int(((mem_free + mem_cache) / MEM_TOTAL) * 5)
    mem_cache_blocks = int((mem_cache / MEM_TOTAL) * 5)
    index = 1
    draw = 0
    while draw < sys_sys_blocks:
        g513_led(f"-kn f{index} {COLOR_SYS}")
        index += 1
        draw += 1
    draw = 0
    while draw < sys_used_blocks:
        g513_led(f"-kn f{index} {COLOR_USED}")
        index += 1
        draw += 1
    while index <= 8:
        g513_led(f"-kn f{index} {COLOR}")
        index += 1
    draw = 0
    while draw < mem_cache_blocks:
        g513_led(f"-kn f{index} {COLOR_CACHE}")
        index += 1
        draw += 1
    while draw < mem_nonused_blocks:
        g513_led(f"-kn f{index} {COLOR}")
        index += 1
        draw += 1
    while index <= 12:
        g513_led(f"-kn f{index} {COLOR_USED}")
        index += 1
    g513_led("-c")


g513_led(f"-a {COLOR}")

while True:
    sysstats()
    sleep(0.7)
    pass
