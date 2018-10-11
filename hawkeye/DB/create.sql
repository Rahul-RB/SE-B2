DROP DATABASE Hawkeye;
CREATE DATABASE Hawkeye;

USE Hawkeye;

CREATE TABLE PatientDetails (
    patientID CHAR(12) ,
    name VARCHAR(20),
    email VARCHAR(100) UNIQUE NOT NULL,
    dob DATE,
    address VARCHAR(100),
    sex CHAR(1),
    phoneNO VARCHAR(10),
    PRIMARY KEY (patientID)
);

CREATE TABLE DoctorDetails (
    doctorID CHAR(12),
    doctorName VARCHAR(20),
    email VARCHAR(100) UNIQUE NOT NULL,
    dob DATE,
    address VARCHAR(100),
    sex CHAR(1),
    phoneNO VARCHAR(10),
    designation VARCHAR(100),
    PRIMARY KEY(doctorID)
);

CREATE TABLE LabDetails (
    labID CHAR(12),
    labName VARCHAR(20),
    address VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    phoneNO VARCHAR(10),
    PRIMARY KEY(labID)    
);

CREATE TABLE PharmacyDetails (
    pharmacyID CHAR(12),
    pharmacyName VARCHAR(20),
    address VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    phoneNO VARCHAR(10),
    PRIMARY KEY(pharmacyID)    
);


CREATE TABLE Consultation (
    patientID CHAR(12),
    doctorID CHAR(12),
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID),
    FOREIGN KEY (doctorID) REFERENCES  DoctorDetails (doctorID),
    PRIMARY KEY (patientID ,doctorID)
);

CREATE TABLE PatientLab (
    patientID CHAR(12),
    labID CHAR(12),
    accessRight TINYINT,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID) ,
    FOREIGN KEY (labID) REFERENCES  LabDetails (labID),
    PRIMARY KEY (patientID ,labID )
);

CREATE TABLE PatientPharmacy (
    patientID CHAR(12) ,
    pharmacyID CHAR(12) ,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID) ,
    FOREIGN KEY (pharmacyID) REFERENCES  PharmacyDetails (pharmacyID),
    PRIMARY KEY( patientID,pharmacyID )
);

CREATE TABLE PatientLogin (
    email VARCHAR(100),
    password VARCHAR(100),
    FOREIGN KEY (email) REFERENCES  PatientDetails (email),
    PRIMARY KEY (email)
);

-- Should be split for "Analysis"
CREATE TABLE GenPatientHistory (
    patientID CHAR(12) ,
    bloodGroup CHAR(2),
    allergies VARCHAR(100),
    hereditaryProblems VARCHAR(100),
    dietAdvice VARCHAR(100),
    injectionHistory VARCHAR(100) ,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID),
    PRIMARY KEY( patientID)
);

CREATE TABLE MedicineReminder (
    patientID CHAR(12) NOT NULL,
    medReminderID INTEGER PRIMARY KEY AUTO_INCREMENT,
    medicineName VARCHAR(50),
    description VARCHAR(100),
    alarmDate DATETIME,
    alarmDuration INTEGER,
    noOfDoses INTEGER ,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID),
    UNIQUE( patientID,medReminderID)
);

CREATE TABLE VisitReminder (
    patientID CHAR(12) NOT NULL,
    visitReminderID INTEGER PRIMARY KEY AUTO_INCREMENT,
    docName VARCHAR(20),
    description VARCHAR(100),
    alarmDate DATETIME,
    alarmDuration INTEGER ,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID),
    UNIQUE(patientID,visitReminderID)
);

CREATE TABLE DoctorLogin (
    email VARCHAR(100),
    password VARCHAR(100),
    FOREIGN KEY (email) REFERENCES  DoctorDetails (email),
    PRIMARY KEY(email)
);
CREATE TABLE EPrescription (
    ePrescriptionID INTEGER,
    patientID CHAR(12) ,
    slNo INTEGER,
    symptoms VARCHAR(100),
    medicineSuggestion VARCHAR(100),
    remarks VARCHAR(100),
    doctorID CHAR(12) ,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID) ,
    FOREIGN KEY (doctorID) REFERENCES  DoctorDetails (doctorID) ,
    PRIMARY KEY(ePrescriptionID ,patientID ,slNo)
);

CREATE TABLE Prescription (
    patientID CHAR(12) NOT NULL ,
    prescriptionID INTEGER PRIMARY KEY AUTO_INCREMENT,
    dateTimeStamp DATETIME,
    fileLocation VARCHAR(100) ,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID),
    UNIQUE (patientID, prescriptionID)
);

CREATE TABLE LabRequest (
    labRequestID INTEGER PRIMARY KEY AUTO_INCREMENT,
    prescriptionID INTEGER ,
    erescriptionID INTEGER ,
    labID CHAR(12),
    patientID CHAR(12),
    doctorID CHAR(12),
    testType VARCHAR(100),
    description VARCHAR(100),
    dateTimeStamp DATETIME,
    isPending INTEGER,
    FOREIGN KEY (labID) REFERENCES  LabDetails (labID) ,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID) ,
    FOREIGN KEY (doctorID) REFERENCES  DoctorDetails (doctorID)
);

CREATE TABLE LabResponse (
    labRequestID INTEGER NOT NULL ,
    resultLink VARCHAR(100),
    reportID INTEGER PRIMARY KEY AUTO_INCREMENT,
    description VARCHAR(100),
    dateTimeStamp DATETIME,
    FOREIGN KEY(labRequestID) REFERENCES LabRequest(labRequestID),
    UNIQUE(labRequestID,reportID)
);

CREATE TABLE DoctorFeedback (
    reportID INTEGER ,
    prescriptionID INTEGER,
    patientID CHAR(12),
    doctorID CHAR(12),
    suggestions VARCHAR(100),
    FOREIGN KEY (doctorID) REFERENCES  DoctorDetails (doctorID) ,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID),
    FOREIGN KEY (reportID) REFERENCES LabResponse(reportID),
    PRIMARY KEY(reportID,prescriptionID)
);


CREATE TABLE LabLogin (
    email VARCHAR(100),
    password VARCHAR(100),
    FOREIGN KEY (email) REFERENCES  LabDetails (email),
    PRIMARY KEY( email)
);



CREATE TABLE PharmacyLogin (
    email VARCHAR(100) ,
    password VARCHAR(100),
    FOREIGN KEY (email) REFERENCES  PharmacyDetails (email) ,
    PRIMARY KEY(email)
);

CREATE TABLE MedicineRequest (
    medicineReqID INTEGER PRIMARY KEY AUTO_INCREMENT,
    patientID CHAR(12),
    pharmacyID CHAR(12),
    ePrescriptionID INTEGER NOT NULL,
    pickupTime DATETIME ,
    FOREIGN KEY (pharmacyID) REFERENCES  PharmacyDetails (pharmacyID)  ,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID)  ,
    FOREIGN KEY (ePrescriptionID) REFERENCES  EPrescription (ePrescriptionID)
);

CREATE TABLE MedicineResponse (
    medicineResponseID INTEGER PRIMARY KEY AUTO_INCREMENT,
    medicineReqID INTEGER NOT NULL,
    remarks VARCHAR(100) ,
    FOREIGN KEY (medicineReqID) REFERENCES  MedicineRequest (medicineReqID) 
);