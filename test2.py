from datetime import datetime

DATETIME_FORMAT = '%A/%d/%m/%Y/%H:%M:%S'

logs_array = []

with open("log2.txt", "r") as log_file:
    for line in log_file:
        logs_array.append(line.split(" "))
        if logs_array[-1][-1][-1] == "\n":
            logs_array[-1][-1]=logs_array[-1][-1][0:-1]
        print(logs_array[-1])

open_programs={}
total_time={}

for log in logs_array:
    pid = log[0]
    name = log[1]
    time = log[-2]
    open_close = log[-1]
    if open_close == "Open":
        open_programs[pid]=time
    else:
        open_time = open_programs[pid]
        open_programs.pop(pid, None)
        close_time = time

        open_datetime = datetime.strptime(open_time, DATETIME_FORMAT)
        close_datetime = datetime.strptime(open_time, DATETIME_FORMAT)
        total_open_time_datatime = close_datetime - open_datetime

        if name in total_time:
            total_time[name]+=total_open_time_datatime
        else:
            total_time[name]=total_open_time_datatime
