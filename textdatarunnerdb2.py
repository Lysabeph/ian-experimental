#!/usr/bin/python3

import sqlite3
import time

# Connects to the database.
conn = sqlite3.connect('dbtrial2.db')
c = conn.cursor()

# Creates an empty array for the unique programs.
programs = []
new_time = str(int(time.time()))

# Reads the last unixepoch time when the update was performed.
with open("latest_time", "r") as file:
    latest_time = file.readline()

# Gets all the unique programs stored in the database.
for record in c.execute("SELECT * FROM Programs;"):
     programs.append(record[1])

# Loops through all the unique programs.
for program in programs:
    c.execute("SELECT ProgramNumber, TotalRunTime, TimesRun FROM Programs WHERE Programs.ProgramName='" + str(program) + "';")
    sqllist = c.fetchone()
    program_number = sqllist[0] # Get the unique number identifier for the program.
    running_time_total = sqllist[1] # Gets the previous total run time.
    counter = sqllist[2] # Gets the previous run counter.

    pstate = None

    # Loops through all the logs recorded after the last update.
    for record in c.execute("SELECT * FROM ProgramLogs WHERE ProgramNumber='" + str(program_number) + "' AND DateTime>'" + latest_time + "' ORDER BY ProgramLogs.DateTime;"):

        # If the previous log was the opening of a program.
        if pstate == "Open":

            # Ignores if the same program is logged to have been opened twice.
            if record[-1] == "Open":
                continue
            # Calculates the time a program was open once the close log is found.
            else:
                ftime = record[-2]
                running_time_total += (int(ftime) - int(stime))
                pstate = "Close"

        # If the previous log was the closing of a program or the start of a new program's logs.
        else:

            # Adds one to the program counter for all open records.
            if record[-1] == "Open":
                stime = record[-2]
                counter += 1
                pstate = "Open"
            # Ignores if the same program is logged to have been closed twice.
            else:
                continue

    # Updates the records of the database with the new information about each program.
    c.execute("UPDATE Programs SET TimesRun='" + str(counter) + "', TotalRunTime='" + str(running_time_total) + "' WHERE Programs.ProgramNumber='" + str(program_number) + "';")

# Commits all changes to the database and closes the connection.
conn.commit()
conn.close()

# Writes the new latest time since update.
with open("latest_time", "w") as file:
    file.write(str(new_time))
