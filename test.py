from datetime import datetime

DATETIME_FORMAT = '%A/%d/%m/%Y/%H:%M:%S'

logs_array = []

with open("log2.txt", "r") as log_file:
    for line in log_file:
        print(line)
        logs_array.append(line.split(" "))

#Removes the blank line at the end of the log_file.
#logs_array.remove(logs_array[-1])

programs = {}
popen = {}

for log in logs_array:
    #Gets Open/Close flag of given log record.
    status = log[-1]

    #If log record present in dictionary, updates info.
    if log[1] in programs:
        if status == 'Open\n':
            programs[log[1]][0] += 1
            popen[log[1]]=log[-2]
        elif status == 'Close\n':
            popen[log[1]]
            topen = popen[log[1]]#.split('/')[-1]
            tclose = programs[log[1]][-1]#.split('/')[-1]
            print(topen, "~", log[0], tclose)
            dtopen = datetime.strptime(topen, DATETIME_FORMAT)
            dtclose = datetime.strptime(tclose, DATETIME_FORMAT)
            programs[log[1]][1] = str(dtclose - dtopen)
            del popen[log[1]]
    #If log record not present, add to dictionary.
    else:
        programs[log[1]] = [1, ""]
