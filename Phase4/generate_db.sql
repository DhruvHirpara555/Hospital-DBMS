DROP DATABASE IF EXISTS `HOSPITAL_CLI`;
CREATE SCHEMA `HOSPITAL_CLI`;
USE `HOSPITAL_CLI`;

CREATE TABLE `PATIENT` (
    `PID` INT NOT NULL AUTO_INCREMENT,
    `FName` VARCHAR(255) NOT NULL, 
    `LName` VARCHAR(255) NOT NULL DEFAULT '',
    `Gender` CHAR(1) NOT NULL CHECK(`Gender` IN ('M', 'F', 'O')),
    `DOB` DATE NOT NULL,
    `Email` VARCHAR(255) NOT NULL UNIQUE,
    `PhoneNo` INT UNIQUE,
    `EMContactName` VARCHAR(255) NOT NULL,
    `EMContactPhNo` INT NOT NULL,
    `EMContactAge` INT NOT NULL DEFAULT 18 CHECK(`EMContactAge` > 17),
    `EMContactRel` VARCHAR(255),

    PRIMARY KEY(`PID`)

);

CREATE TABLE `ROOM` (
    `RoomNo` INT NOT NULL UNIQUE,
    `Floor` INT NOT NULL, 
    `Type` VARCHAR(255) , 

    PRIMARY KEY(`RoomNo`)

);

CREATE TABLE `BED` (
    `BedNo` INT NOT NULL,
    `RoomNo` INT NOT NULL,
    `Cost` INT NOT NULL, 
    `IsVacant` BOOLEAN DEFAULT 1, 

    FOREIGN KEY(`RoomNo`) 
        REFERENCES `ROOM`(`RoomNo`)
        ON UPDATE CASCADE 
        ON DELETE CASCADE,
    PRIMARY KEY(`RoomNo`, `BedNo`)

);
CREATE TABLE `EMPLOYEE` (
    `EID` INT NOT NULL AUTO_INCREMENT,
    `FName` VARCHAR(255) NOT NULL, 
    `LName` VARCHAR(255) NOT NULL DEFAULT '',
    `Gender` CHAR(1) NOT NULL CHECK(`Gender` IN ('M', 'F', 'O')),
    `DOB` DATE NOT NULL,
    `Email` VARCHAR(255) NOT NULL UNIQUE,
    `PhoneNo` INT UNIQUE,
    `Emp_Type` CHAR(1) NOT NULL CHECK(`Emp_Type` IN ('D', 'M', 'A', 'O')), 
    `Office` INT DEFAULT NULL,
    `Supervisor` INT,

    FOREIGN KEY(`Supervisor`) 
        REFERENCES `EMPLOYEE`(`EID`)
        ON UPDATE CASCADE 
        ON DELETE SET NULL,

    FOREIGN KEY(`Office`) 
        REFERENCES `ROOM`(`RoomNo`)
        ON UPDATE CASCADE 
        ON DELETE SET NULL,
    
    PRIMARY KEY(`EID`)

);

CREATE TABLE `QUALIFICATIONS` (
    `EID` INT NOT NULL,
    `Qual` VARCHAR(255),
    
    FOREIGN KEY(`EID`) 
        REFERENCES `EMPLOYEE`(`EID`)
        ON UPDATE CASCADE 
        ON DELETE CASCADE,

    PRIMARY KEY(`EID`, `Qual`)

);

CREATE TABLE `SPECIALIZATIONS` (
    `EID` INT NOT NULL,
    `Spec` VARCHAR(255),
    
    FOREIGN KEY(`EID`) 
        REFERENCES `EMPLOYEE`(`EID`)
        ON UPDATE CASCADE 
        ON DELETE CASCADE,

    PRIMARY KEY(`EID`, `Spec`)

);

CREATE TABLE `DEPARTMENT` (
    `DID` INT NOT NULL AUTO_INCREMENT,
    `DName` VARCHAR(255) NOT NULL, 
    `Head` INT ,

    FOREIGN KEY(`Head`) 
        REFERENCES `EMPLOYEE`(`EID`)
        ON UPDATE CASCADE 
        ON DELETE SET NULL,
    PRIMARY KEY(`DID`)

);

CREATE TABLE `MEMBER_OF` (
    `EID` INT NOT NULL,
    `DID` INT NOT NULL,

    FOREIGN KEY(`EID`) 
        REFERENCES `EMPLOYEE`(`EID`)
        ON UPDATE CASCADE 
        ON DELETE CASCADE,

    FOREIGN KEY(`DID`) 
        REFERENCES `DEPARTMENT`(`DID`)
        ON UPDATE CASCADE 
        ON DELETE CASCADE,

    PRIMARY KEY(`EID`, `DID`)

);

CREATE TABLE `TREATMENT` (
    `TID` INT AUTO_INCREMENT,
    `Name` VARCHAR(255) NOT NULL, 
    `Cost` VARCHAR(255) NOT NULL, 
    `Type` VARCHAR(255) , 

    PRIMARY KEY(`TID`)

);

CREATE TABLE `VISIT` (
    `PID` INT NOT NULL,
    `VID` INT NOT NULL, 
    `Diagnosis` VARCHAR(255),
    `Report` TEXT,

    FOREIGN KEY(`PID`) 
        REFERENCES `PATIENT`(`PID`) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE,

    PRIMARY KEY(`PID`, `VID`)

);

CREATE TABLE `INPATIENT` (
    `PID` INT NOT NULL,
    `VID` INT NOT NULL, 
    `InDate` DATE NOT NULL,
    `InTime` TIME NOT NULL,
    `OutDate` DATE,
    `OutTime` TIME,
    `RoomNo` INT,
    `Bed` INT,

    FOREIGN KEY(`PID`,`VID`) 
        REFERENCES `VISIT`(`PID`, `VID`) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE,

    FOREIGN KEY(`RoomNo`, `Bed`) 
        REFERENCES `BED`(`RoomNo`, `BedNo`)
        ON UPDATE CASCADE 
        ON DELETE SET NULL,

    PRIMARY KEY(`PID`, `VID`)

);

CREATE TABLE `OUTPATIENT` (
    `PID` INT NOT NULL,
    `VID` INT NOT NULL, 
    `InDate` DATE NOT NULL,
    `InTime` TIME NOT NULL,

    FOREIGN KEY(`PID`,`VID`) 
        REFERENCES `VISIT`(`PID`, `VID`)  
        ON UPDATE CASCADE 
        ON DELETE CASCADE,

    PRIMARY KEY(`PID`, `VID`)

);

CREATE TABLE `TREATS` (
    `Patient` INT,
    `Visit` INT, 
    `Doctor` INT,
    `GivenBy` INT,
    `Treatment` INT,
    `Date` DATE,
    `Time` TIME,
    
    FOREIGN KEY(`Patient`, `Visit`) 
        REFERENCES VISIT(`PID`, `VID`)
        ON UPDATE NO ACTION 
        ON DELETE NO ACTION,
    FOREIGN KEY(`Doctor`) REFERENCES `EMPLOYEE`(`EID`)
        ON UPDATE NO ACTION 
        ON DELETE NO ACTION,
    FOREIGN KEY(`GivenBy`) REFERENCES `EMPLOYEE`(`EID`)
        ON UPDATE NO ACTION 
        ON DELETE NO ACTION,
    FOREIGN KEY(`Treatment`) REFERENCES `TREATMENT`(`TID`)
        ON UPDATE NO ACTION 
        ON DELETE NO ACTION,
    PRIMARY KEY(`Patient`, `Visit`, `Doctor`, `GivenBy`, `Treatment`, `Date`, `Time`)

);



INSERT INTO PATIENT (PID, FName, LName, Gender, DOB, Email, PhoneNo, EMContactName, EMContactPhNo, EMContactAge, EMContactRel)
VALUES
    (1, "Dhruv", "Hirpara", 'M', DATE("2002-06-24"), "a@gmail.com", 816037212, "aaaa", 111111111, 19, "Friend"),
    (2, "Shreya", "Patil", 'M', DATE("2002-06-23"), "b@gmail.com", 816037211, "bbbb", 111111111, 19, "Brother"),
    (3, "Srija", "Narra", 'F', DATE("2003-04-02"), "c@gmail.com", 816037213, "cccc", 111111110, 23, "Brother"),
    (4, "Harry", "Potter", 'M', DATE("2000-05-19"), "harry@gmail.com", 816037215, "Hagrid", 111111116, 40, "Friend"),
    (5, "Ronald", "Weasly", 'M', DATE("2000-01-07"), "ron@gmail.com", 816037216, "Arthur", 111111117, 50, "Father"),
    (6, "Hermione", "Granger", 'F', DATE("2000-03-28"), "hermione@gmail.com", 816037217, "Ginny", 111111118, 20, "Friend"),
    (7, "Magnus", "Chase", 'M', DATE("2002-01-07"), "magnus@gmail.com", 816037318, "Annabeth", 111111119, 19, "Sister"),
    (8, "Alex", "Fierro", 'o', DATE("2002-04-28"), "alex@gmail.com", 816037319, "Samirah", 111111120, 19, "Sister"),
    (9, "Samirah", "Al-Abbas", 'F', DATE("2002-09-11"), "sam@gmail.com", 816037320, "Amir", 111111121, 21, "Friend"),
    (10, "Jake", "Peralta", 'M', DATE("1981-06-07"), "jake@gmail.com", 816037321, "Amy", 111111122, 40, "Wife"),
    (11, "Charles", "Boyle", 'M', DATE("1978-05-19"), "boyle@gmail.com", 816037322, "Genevieve", 111111123, 44, "Wife"),
    (12, "Amy", "Santiago", 'F', DATE("1982-02-03"), "amy@gmail.com", 816037323, "Jake", 111111124, 41, "Husband"),
    (13, "Raymond", "Holt", 'M', DATE("1955-05-03"), "ray@gmail.com", 816037324, "Kevin", 111111125, 65, "Husband"),
    (14, "Terrence", "Jeffords", 'M', DATE("1972-10-09"), "terry@gmail.com", 816037325, "Sharon", 111111126, 47, "Wife"),
    (15, "Rosa", "Diaz", 'F', DATE("1985-12-30"), "rosa@gmail.com", 816037326, "Oscar", 111111127, 58, "Father"),
    (16, "Gina", "Linetti", 'F', DATE("1981-01-01"), "gina@gmail.com", 816037327, "Darlene", 111111128, 67, "Mother");


INSERT INTO ROOM (RoomNo, Floor, Type)
VALUES
    (101,1,"Bedroom"),
    (201,2,"Bedroom"),
    (202,2,"Bedroom"),
    (102,1,"Office"),
    (104,1,"Bedroom"),
    (203,2,"Office"),
    (105,1,"Bedroom"),
    (103,1,"Bedroom"),
    (204,2,"Office"),
    (206,2,"Bedroom"),
    (109,1,"Office"),
    (208,2,"Bedroom"),
    (106,1,"Office"),
    (205,2,"Bedroom"),
    (210,2,"Bedroom");

INSERT INTO BED (BedNo, RoomNo, Cost, IsVacant)
VALUES
    (10,101, 1000,0),
    (11,101, 1000,0),
    (12,101, 1000,0),
    (13,101, 1000,0),
    (14,101, 1000,0),
    (10,201, 3000,0),
    (10,202, 2000,0),
    (10,203, 3000,0),
    (11,202, 2000,0),
    (12,201, 2000,0);


INSERT INTO EMPLOYEE (EID, FName, LName, Gender, DOB, Email, PhoneNo, Emp_Type, Office, Supervisor)
VALUES
    (1, "Chaitra", "Chenaboina", 'F', DATE("2003-04-03"), "c@gmail.com", 962627000, 'A',204, 1),
    (2, "Praksh", "Hirpara", 'M', DATE("1970-06-24"), "a@gmail.com", 997804443, 'D',102, 2),
    (3, "Vilas", "Hirpara", 'F', DATE("1976-10-22"), "v@gmail.com", 962627626, 'M',102, 2),
    (4, "Amara", "Narra", 'F', DATE("1976-10-29"), "n@gmail.com", 997808123, 'O',203, 1),
    (5, "Suraj", "Narra", 'M', DATE("1999-04-02"), "s@gmail.com", 962627909, 'M',203, 2),
    (6, "Divya", "Mekapothu", 'F', DATE("2003-08-18"), "d@gmail.com", 997804575, 'O',106, 1),
    (7, "Keerthana", "Patchava", 'F', DATE("2002-10-26"), "f@gmail.com", 997808883, 'D',109, 7),
    (8, "Nitin", "Shrinivas", 'M', DATE("2001-12-02"), "k@gmail.com", 962627717, 'M',106, 7);


INSERT INTO `DEPARTMENT` VALUES 
    (1, "Finance", 6),
    (2, "Administration", 1),
    (3, "Maintainance", 4),
    (4, "Pediatrics", 2),
    (5, "General Medicine", 7),
    (6, "Cardiology", 1);

INSERT INTO `MEMBER_OF` VALUES
    (1, 2),
    (2, 4),
    (3, 4),
    (4, 3),
    (5, 2),
    (6, 1),
    (7, 5),
    (8, 5);


INSERT INTO TREATMENT (TID, Name, Cost, Type)
VALUES
    (1234, "Medicine 1", 100,"MED"),
    (1239, "Medicine 2", 100,"MED"),
    (1235, "Surgery 1", 200, "SUR"),
    (1236, "Surgery 2", 200, "SUR"),
    (1237, "Surgery 3", 200, "SUR"),
    (1240, "Surgery 4", 200, "SUR"),
    (1241, "Surgery 5", 200, "SUR"),
    (1238, "Therapy 1", 300,"THR"),
    (1242, "Therapy 2", 300,"THR");

INSERT INTO VISIT (PID,VID,Diagnosis,Report)
VALUES
    (1, 1, "MADMAN", "YOU are dumb"),
    (1, 2, "MADMAN", "YOU are getting more dumb"),
    (2, 1, "FEVER", "General Fever"),
    (2, 2, "FEVER", "needs to be admitted"),
    (3, 1, "Cavities", "Need Surgery"),
    (4, 1, "Fracture", "100 broken bones"),
    (5, 1, "aaaa", "aaaaa bbbbb cccc"),
    (6, 1, "abcd", "abcd abcd abcd"),
    (7, 1, "Something bad", "no Fever"),
    (8, 1, "iiii", "aaa bbb"),
    (9, 1, "regular check", "no Fever"),
    (10, 1, "Lichen Planus", "medication required"),
    (11, 1, "Covid", "should be admitted"),
    (12, 1, "depression", "therapy needed"),
    (13, 1, "abcd", "abcd abcdr"),
    (14, 1, "aaaa", "aaaa bbb vvvv"),
    (15, 1, "bbbb", "aaaa bcdbcd"),
    (16, 1, "ccccc", "abcd abcd");




INSERT INTO INPATIENT (PID, VID, InDate, InTime, OutDate, OutTime, RoomNo, Bed)
VALUES
    (1, 1,DATE("2021-10-23"), TIME("19:30:10"), DATE("2021-10-30"),TIME("19:30:10"),202, 10),
    (2, 2,DATE("2021-10-13"), TIME("16:30:00"), DATE("2021-10-20"),TIME("10:36:10"),101, 11),
    (3, 1,DATE("2021-10-01"), TIME("13:30:40"), DATE("2021-10-09"),TIME("9:30:00"),202, 11),
    (4, 1,DATE("2021-09-20"), TIME("09:28:00"), DATE("2021-10-01"),TIME("20:00:40"),101, 10),
    (5, 1,DATE("2021-12-03"), TIME("10:40:18"), DATE("2021-12-04"),TIME("06:50:50"),201, 10),
    (6, 1,DATE("2021-11-02"), TIME("12:30:00"), DATE("2021-11-17"),TIME("13:30:00"),101, 14),
    (7, 1,DATE("2021-12-18"), TIME("20:30:00"), DATE("2021-12-31"),TIME("16:20:00"),101, 12),
    (11, 1,DATE("2021-12-18"), TIME("20:30:00"), DATE("2021-12-31"),TIME("16:20:00"),101, 13);

INSERT INTO OUTPATIENT (PID,VID,InDate, InTime) VALUES
    (2, 1,DATE("2021-11-23"), TIME("19:30:10")),
    (13, 1,DATE("2021-10-13"), TIME("14:40:00")),
    (14, 1,DATE("2021-11-18"), TIME("09:30:00")),
    (15, 1,DATE("2021-12-30"), TIME("11:50:15")),
    (16, 1,DATE("2021-11-10"), TIME("08:30:00")),
    (10, 1,DATE("2021-10-15"), TIME("12:30:50")),
    (8, 1,DATE("2021-12-12"), TIME("17:50:10")),
    (9, 1,DATE("2021-11-06"), TIME("22:00:00")),
    (12, 1,DATE("2021-11-06"), TIME("22:00:00"));

INSERT INTO TREATS (Patient, Visit, Doctor, GivenBy, Treatment, Date, Time)
VALUES
    (1, 1, 2, 3, 1234,DATE("2021-10-23"),TIME("19:30:10")),
    (1, 1, 2, 3, 1235,DATE("2021-10-26"),TIME("19:30:10")),
    (1, 1, 2, 5, 1236,DATE("2021-10-28"),TIME("19:30:10")),
    (2, 1, 7, 8, 1239,DATE("2021-10-16"),TIME("19:30:10")),
    (2, 1, 7, 8, 1235,DATE("2021-10-17"),TIME("19:30:10")),
    (3, 1, 7, 8, 1239,DATE("2021-10-04"),TIME("19:30:10")),
    (4, 1, 7, 8, 1234,DATE("2021-09-23"),TIME("19:30:10")),
    (5, 1, 2, 5, 1235,DATE("2021-12-03"),TIME("19:30:10")),
    (6, 1, 2, 3, 1239,DATE("2021-11-13"),TIME("19:30:10")),
    (7, 1, 2, 5, 1240,DATE("2021-12-23"),TIME("19:30:10")),
    (7, 1, 2, 3, 1241,DATE("2021-12-25"),TIME("19:30:10")),
    (8, 1, 7, 8, 1238,DATE("2021-12-12"),TIME("17:50:10")),
    (8, 1, 7, 8, 1242,DATE("2021-11-23"),TIME("19:30:10")),
    (9, 1, 7, 8, 1239,DATE("2021-11-06"),TIME("22:30:10")),
    (10, 1, 2, 3, 1234,DATE("2021-10-15"),TIME("12:30:10")),
    (11, 1, 2, 5, 1235,DATE("2021-12-23"),TIME("19:30:10")),
    (12, 1, 7, 8, 1239,DATE("2021-11-06"),TIME("22:30:10")),
    (13, 1, 2, 5, 1234,DATE("2021-10-13"),TIME("14:50:10"));