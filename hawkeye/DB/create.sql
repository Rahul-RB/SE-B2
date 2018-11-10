
DROP DATABASE Hawkeye1;
CREATE DATABASE Hawkeye1;

USE Hawkeye1;

CREATE TABLE PatientDetails (
    patientID CHAR(12) ,
    patientName VARCHAR(20),
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

-- What's these tables for?

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

-- End of question area.

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

CREATE TABLE DoctorLogin (
    email VARCHAR(100),
    password VARCHAR(100),
    FOREIGN KEY (email) REFERENCES  DoctorDetails (email),
    PRIMARY KEY(email)
);

-- no AUTO_INCREMENT in ePrescriptionID so have to manually enter random number - time is a number, best.
CREATE TABLE EPrescription (
    ePrescriptionID VARCHAR(20), 
    patientID CHAR(12) ,
    doctorID CHAR(12) ,
    -- slNo INTEGER AUTO_INCREMENT,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID) ,
    FOREIGN KEY (doctorID) REFERENCES  DoctorDetails (doctorID) ,
    -- PRIMARY KEY(ePrescriptionID ,patientID ,slNo)
    PRIMARY KEY(ePrescriptionID ,patientID)
);

CREATE TABLE MedicineDetails(
    ePrescriptionID VARCHAR(20),
    symptoms VARCHAR(100),
    medicineSuggestion VARCHAR(100),    
    timeToTake TIME,
    startDate DATE,
    endDate DATE,
    FOREIGN KEY (ePrescriptionID) REFERENCES  EPrescription (ePrescriptionID)     
);

 -- No entres requried
CREATE TABLE Prescription (
    patientID CHAR(12) NOT NULL ,
    prescriptionID INTEGER PRIMARY KEY AUTO_INCREMENT,
    dateTimeStamp DATETIME,
    fileLocation VARCHAR(100) ,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID),
    UNIQUE (patientID, prescriptionID)
);
 -- No entres requried

 -- No entres requried
CREATE TABLE LabRequestDocument(
    labRequestDocumentID INTEGER PRIMARY KEY AUTO_INCREMENT,

    patientID CHAR(12),
    doctorID CHAR(12),
    testType VARCHAR(100),
    description VARCHAR(100),
    fileLocation VARCHAR(100) ,

    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID) ,
    FOREIGN KEY (doctorID) REFERENCES  DoctorDetails (doctorID)
); 
 -- No entres requried

CREATE TABLE ELabRequestDocument(
    labRequestDocumentID INTEGER PRIMARY KEY AUTO_INCREMENT,

    doctorID CHAR(12),
    ePrescriptionID VARCHAR(20) ,
    patientID CHAR(12),

    testType VARCHAR(100),
    description VARCHAR(100),

    FOREIGN KEY (ePrescriptionID) REFERENCES  EPrescription (ePrescriptionID) ,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID) ,
    FOREIGN KEY (doctorID) REFERENCES  DoctorDetails (doctorID)
); 

CREATE TABLE LabRequest (
    labRequestDocumentID INTEGER,
    labID CHAR(12),
    dateTimeStamp DATETIME,
    isPending TINYINT,
    FOREIGN KEY (labID) REFERENCES  LabDetails (labID) ,
    FOREIGN KEY (labRequestDocumentID) REFERENCES ELabRequestDocument (labRequestDocumentID) ,
    PRIMARY KEY (labRequestDocumentID)
);

CREATE TABLE LabResponse (
    reportID INTEGER PRIMARY KEY AUTO_INCREMENT,
    labRequestID INTEGER NOT NULL,
    resultLink VARCHAR(100),
    description VARCHAR(100),
    dateTimeStamp DATETIME,
    FOREIGN KEY (labRequestID) REFERENCES LabRequest(labRequestDocumentID),
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
    -- medicineReqID INTEGER PRIMARY KEY AUTO_INCREMENT,
    ePrescriptionID VARCHAR(20),
    patientID CHAR(12),
    pharmacyID CHAR(12),
    pickupTime DATETIME ,
    isPending TINYINT,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID)  ,
    FOREIGN KEY (pharmacyID) REFERENCES  PharmacyDetails (pharmacyID)  ,
    FOREIGN KEY (ePrescriptionID) REFERENCES  EPrescription (ePrescriptionID),
    PRIMARY KEY (ePrescriptionID,patientID)
);

CREATE TABLE MedicineResponse (
    medicineResponseID INTEGER PRIMARY KEY AUTO_INCREMENT,
    ePrescriptionID VARCHAR(20) NOT NULL,
    patientID CHAR(12),
    remarks VARCHAR(100) ,
    FOREIGN KEY (ePrescriptionID,patientID) REFERENCES  MedicineRequest (ePrescriptionID,patientID) 
);

 -- No entres requried
CREATE TABLE DoctorAppointments (
    patientID CHAR(12),
    doctorID CHAR(12),
    dateStamp DATE,
    pickATime TIME,
    addedToDoctorCalendar TINYINT,
    FOREIGN KEY (patientID) REFERENCES PatientDetails (patientID)  ,
    FOREIGN KEY (doctorID) REFERENCES DoctorDetails (doctorID) ,
    PRIMARY KEY (doctorID,patientID)
);
 -- No entres requried

-- reminderDate and reminderTime for order medicines only
-- for take medicines time and dates in MedicineDetails tables.
CREATE TABLE MedicineReminder (
    ePrescriptionID VARCHAR(20) NOT NULL,
    patientID CHAR(12) NOT NULL,
    reminderDate DATE, 
    reminderTime TIME,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID),
    FOREIGN KEY (ePrescriptionID) REFERENCES  EPrescription (ePrescriptionID)
);

CREATE TABLE LabVisitReminder (
    patientID CHAR(12) NOT NULL,
    labID CHAR(12) NOT NULL,
    labRequestDocumentID INTEGER,

    reminderDate DATE,
    reminderTime TIME,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID),
    FOREIGN KEY (labID) REFERENCES  LabDetails (labID),
    FOREIGN KEY (labRequestDocumentID) REFERENCES  ELabRequestDocument (labRequestDocumentID)
);


CREATE TABLE DoctorVisitReminder (
    patientID CHAR(12) NOT NULL,
    doctorID CHAR(12) NOT NULL,

    reminderDate DATE,
    reminderTime TIME,
    message VARCHAR(100),
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID),
    FOREIGN KEY (doctorID) REFERENCES  DoctorDetails (doctorID)
);