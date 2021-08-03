PRAGMA foreign_keys = 1;
CREATE TABLE Programs (
    ProgramName varchar(31) PRIMARY KEY,
    TimesRun int,
    TotalRunTime datetime
);

CREATE TABLE ProgramCommands (
    ProgramCMD varchar(63) PRIMARY KEY,
    ProgramName varchar(31),
    FOREIGN KEY(ProgramName) REFERENCES Programs(ProgramName)
);

CREATE TABLE ProgramLogs (
    ProgramName varchar(31),
    PID int(6),
    DateTime datetime,
    OpenClose boolean,
    PRIMARY KEY(ProgramName, PID, DateTime, OpenClose),
    FOREIGN KEY(ProgramName) REFERENCES Programs(ProgramName)
);
