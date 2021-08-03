#!/usr/bin/python3

import sqlite3
import time

UPDATE_INTERVAL = 3600 # Default is every hour.

def get_time_range(epoch):
    current_epoch = epoch
    lower_epoch = current_epoch - current_epoch % UPDATE_INTERVAL
    upper_epoch = lower_epoch + UPDATE_INTERVAL
    return lower_epoch, upper_epoch

conn = sqlite3.connect('test.db')
c = conn.cursor()

programs = []

for record in c.execute("""
                            SELECT *
                            FROM Programs;
                        """):
     programs.append(record[0])

print(programs)

#with open("open_programs", "r") as file:
#    open_programs = file.readlines()
open_programs = []

current_epoch = 1478968907 # int(time.time())
lower_epoch, upper_epoch = get_time_range(current_epoch)

c.execute("""
            SELECT *
            FROM ProgramLogs
            ORDER BY DateTime ASC Limit 1;
        """)
first_epoch = c.fetchone()[-2]

logs = []
condition_logs = [] # Will store the programs that have been run with the currently opened programs.

# Separated from the for loop in version 1 to minimise the number of database queries.

while upper_epoch > first_epoch:
    print(lower_epoch, upper_epoch)

    # Similar to logs but resets with each iteration.
    range_logs = []

    for log in c.execute("""
                            SELECT *
                            FROM ProgramLogs
                            WHERE ProgramLogs.OpenClose='Open'
                            AND ProgramLogs.DateTime>='{0}'
                            AND ProgramLogs.DateTime<'{1}';
                        """.format(str(lower_epoch), str(upper_epoch))):
        log = list(log)
        log[2] = (log[2]//3600 + 1) * 3600
        range_logs.append(log[0])
        logs.append(log)

    # Checks if the currently open programs have been open togother in the past.
    # This could be done exactly (so no extra programs were open with the current
    # set-up) but this may not be useful.
    program = False # Incase open_programs is empty.
    for program in open_programs:
        if program not in range_logs:
            program = False
            break
        else:
            range_logs.remove(program)

    if program:
        condition_logs.append(range_logs)
    else:
        condition_logs.append([])

    times_run.append(0)
    lower_epoch -= 86400 # A day.
    upper_epoch -= 86400

for program in programs:

    if "\'" + program + "\'" in open_programs:
        continue

    c.execute("""
                SELECT *
                FROM ProgramLogs
                WHERE ProgramLogs.ProgramName='{0}'
                ORDER BY DateTime ASC Limit 1;
            """.format(program))

    earliest_epoch = c.fetchone()[-2]
    print(earliest_epoch)

    program_logs = list(logs)
    times_run = []
    program_log_counter = 0

    # Using logs as the length of the array will be static throughout the loop.
    for record in logs:
        if record[2] < earliest_epoch:
            program_logs.remove(record)

    lower_epoch, upper_epoch = get_time_range(current_epoch)
    times_run = 0
    possible_times_run = 0

    while upper_epoch > earliest_epoch:
        for record in logs:
            if record[0] == program:
                times_run += 1
        possible_times_run += 1

    times_run.append(program_log_counter)

    summ = 0
    for num in times_run:
        if num > 0:
            summ += 1
    prob = summ / len(times_run)
    pers = sum(times_run) // len(times_run)

    programs[programs.index(program)] = [program, times_run, prob, pers]

for program in programs:
    print(program)
