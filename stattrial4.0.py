#!/usr/bin/python3

import sqlite3
import time

TIME_PERIOD = 86400 # Default is every day.
UPDATE_INTERVAL = 3600 # Default is every hour.

def get_time_range(epoch):
    current_epoch = epoch
    lower_epoch = current_epoch - current_epoch % UPDATE_INTERVAL
    upper_epoch = lower_epoch + UPDATE_INTERVAL
    return lower_epoch, upper_epoch

def get_probability(variable, dictionary):
    has_run_counter = 0
    c.execute("""
                SELECT Programs.TimesRun
                FROM Programs
                WHERE Programs.ProgramNumber='{0}';
            """.format(str(variable)))
    total_times_run = c.fetchone()[0]
    multi_array = []

    for key in dictionary:
        multi_array.append(dictionary[key])

    for array in multi_array:
        if variable in array:
            has_run_counter += 1
            total_times_run += array.count(variable)

    probability = has_run_counter/len(multi_array)
    print(str(variable) + ":", probability, "=", has_run_counter, "/", str(len(multi_array)))
    if (total_times_run/len(multi_array))//1 > 1:
        persistance = True

    else:
        persistance = False

    return probability, persistance

conn = sqlite3.connect('dbtrial2.db')
c = conn.cursor()

programs = []

for record in c.execute("""
                            SELECT *
                            FROM Programs;
                        """):
     programs.append([record[0], record[1]])

open_programs = []
open_program_nmubers = []

#open_program_numbers = []
#
#with open("open_programs", "r") as file:
#    open_programs = file.readlines()
#
#for program in open_programs:
#    c.execute("""
#            SELECT Programs.ProgramNumber
#            FROM Programs
#            WHERE Programs.ProgramName='{}';
#        """.format(program))
#
#        open_programs_numbers.append=c.fetchone()[0]

current_epoch = 1486190301 # int(time.time())
lower_epoch, upper_epoch = get_time_range(current_epoch)

c.execute("""
            SELECT ProgramLogs.DateTime
            FROM ProgramLogs
            ORDER BY DateTime ASC Limit 1;
        """)
first_epoch = c.fetchone()[0]

print("Programs:", programs, "\nFirst Epoch:", first_epoch)

logs = {} # Stores each epoch key with a list value of all the programs running at the time.
condition_logs = {} # Will store the programs that have been run with the currently opened programs.

# Separated from the for loop in version 1 to minimise the number of database queries.

while upper_epoch > first_epoch:
    print(lower_epoch, "(lower);", upper_epoch, "(upper)")

    # Similar to logs but resets with each iteration.
    range_logs = []

    for log in c.execute("""
                            SELECT *
                            FROM ProgramLogs
                            WHERE ProgramLogs.OpenClose='Open'
                            AND ProgramLogs.DateTime>='{0}'
                            AND ProgramLogs.DateTime<'{1}';
                        """.format(str(lower_epoch), str(upper_epoch))):
        range_logs.append(log[1])

    logs[upper_epoch] = range_logs

    # Checks if the currently open programs have been open togother in the past.
    # This could be done exactly (so no extra programs were open with the current
    # set-up) but this may not be useful.

    program = False # Incase open_programs is empty.

    if open_programs:
        for program in open_programs:
            if program not in range_logs:
                program = False
                break

        if program:
            condition_logs[upper_epoch] = range_logs

        else:
            condition_logs[upper_epoch] = []

    else:
        condition_logs = logs

    lower_epoch -= TIME_PERIOD
    upper_epoch -= TIME_PERIOD

for program in programs:
    program_logs = dict(condition_logs)

    if "\'" + program[1] + "\'" in open_programs:
        continue

    c.execute("""
                SELECT *
                FROM ProgramLogs
                WHERE ProgramLogs.ProgramNumber='{0}'
                ORDER BY DateTime ASC Limit 1;
            """.format(program[0]))

    earliest_epoch = c.fetchone()[-2]
    print("Earliest Epoch:", earliest_epoch, "(" + str(program) + ")")

    for times in list(program_logs.keys()):
        if times < earliest_epoch:
            program_logs.pop(times, None)

    if len(program_logs) > 4:
        probability, persistance = get_probability(program[0], program_logs)

    else:
        probability, persistance = get_probability(program[0], logs)

    programs[programs.index(program)] = [program, probability, persistance]



for program in programs:
    print(program)
