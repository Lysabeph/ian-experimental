#!/usr/bin/python3

import sqlite3
import time

HOUR = 3600
DAY = 86400
WEEK = 604800

UPDATE_INTERVAL = HOUR # Default is every hour.

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
    
for program in programs:

#    if "\'" + program + "\'" in open_programs:
#        continue

    current_epoch = 1478968907 # int(time.time())
    lower_epoch, upper_epoch = get_time_range(current_epoch)

    c.execute("""
                SELECT *
                FROM ProgramLogs
                WHERE ProgramLogs.ProgramName='{0}'
                ORDER BY DateTime ASC Limit 1;
            """.format(program))
    earliest_epoch = c.fetchone()[-2]
    print(earliest_epoch)
    array = []

    while upper_epoch > earliest_epoch:
        print(lower_epoch, upper_epoch)
        run_logs = []
        for log in c.execute("""
                                SELECT *
                                FROM ProgramLogs
                                WHERE ProgramLogs.ProgramName='{0}'
                                AND ProgramLogs.OpenClose='Open'
                                AND ProgramLogs.DateTime>='{1}'
                                AND ProgramLogs.DateTime<'{2}';
                            """.format(program, str(lower_epoch), str(upper_epoch))):
            run_logs.append(log)
        print(run_logs)
        array.append(len(run_logs))
        lower_epoch-=DAY
        upper_epoch-=DAY

    
    summ = 0
    for num in array:
        if num > 0:
            summ+=1
    prob = summ/len(array)
    pers = sum(array)//len(array)

    programs[programs.index(program)] = [program, array, prob, pers]
    

for program in programs:
    print(program)
