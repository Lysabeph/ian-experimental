#!/usr/bin/python3

import random
import time

DEFAULT = 50
PROGRAMS = ["firefox", "pluma", "eom", "shutter", "rhythmbox"]

def update(pid, unixepoch):

    unixepoch+=random.randint(8,18)
    pid+=random.randint(2,5)

    if pid > 35000:
        pid = 1500

    return pid, unixepoch

def f(n):

    free_programs = list(PROGRAMS)
    open_programs = []
    unixepoch = int(time.time())
    pid = 1500
    
    for _ in range(n):

        if len(free_programs) == 0:
            oc = 0
        elif len(open_programs) == 0:
            oc = 1
        else:
            oc = random.choice([0, 1])

        if oc == 1:
            program = random.choice(free_programs)
            line = str(pid) + " " + program + " " + str(unixepoch) + " " + "Open\n"
            open_programs.append(program)
            free_programs.remove(program)
        else:
            program = random.choice(open_programs)
            line = str(pid) + " " + program + " " + str(unixepoch) + " " + "Close\n"
            free_programs.append(program)
            open_programs.remove(program)

        with open("test_logs", "a") as file:
            file.write(line)

        pid, unixepoch = update(pid, unixepoch)
    
    for program in open_programs:

        line = str(pid) + " " + program + " " + str(unixepoch) + " " + "Close\n"

        with open("test_logs", "a") as file:
            file.write(line)

        pid, unixepoch = update(pid, unixepoch)

n = input("Enter the number of lines to be written to the test_logs file: ")

try:
    n = int(n)
except ValueError:
    n = DEFAULT
    print("Input invalid, default value used (" + str(DEFAULT) + ")")

f(n)
