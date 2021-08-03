PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE employee (Name varchar(20),Dept varchar(20),jobTitle varchar(20));
INSERT INTO "employee" VALUES('Fred Flinstone','Quarry Worker','Rock Digger');
INSERT INTO "employee" VALUES('Wilma Flinstone','Finance','Analyst');
INSERT INTO "employee" VALUES('Barney Rubble','Sales','Neighbor');
INSERT INTO "employee" VALUES('Betty Rubble','IT','Neighbor');
INSERT INTO "employee" VALUES('Jeff Goldbloom','Sales','Field Worker');
COMMIT;
