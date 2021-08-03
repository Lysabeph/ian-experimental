#!/usr/bin/python3

import os
import sched
import time

s = sched.scheduler(time.time, time.sleep)

def updater():
    os.system("python3 stattrial5.0.py &")

def program_scheduler():
    s.enter(3600, 1, updater)
    s.run()
    
    return True

updater()
os.system("python3 Project\ Interface5.0.py")
os.system("./trial12.0 &")
t = 3540 - int(time.time())%3600

if t > 0:
    time.sleep(t)
    
updater()
while True:
    program_scheduler()
