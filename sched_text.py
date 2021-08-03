#!/usr/bin/python3

import os
import sched
import time

s = sched.scheduler(time.time, time.sleep)

def updater():
    print("!!!")

def program_scheduler():
    s.enter(10, 1, updater)
    s.run()
    
    return True

updater()
time.sleep(2)

while True:
    program_scheduler()
