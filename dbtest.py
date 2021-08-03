#!/usr/bin/python3

import sqlite3

c = sqlite3.connect("test.db")
#c.cursor().execute("CREATE TABLE Programs ( ProgramID INTEGER PRIMARY KEY, ProgramName varchar(31), TimesRun int, TotalRunTime datetime);")
c.cursor().execute("INSERT INTO Programs (ProgramName, TimesRun, TotalRunTime) VALUES ('Chrome', '24', '2016-10-11 14:51:24');")

c.commit()

for i in c.cursor().execute("SELECT * From Programs;"):
    print(i)

c.close()
