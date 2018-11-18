DROP DATABASE HawkeyeWithData;
CREATE DATABASE HawkeyeWithData;

USE HawkeyeWithData;

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

-- CREATE TABLE Consultation (
--     patientID CHAR(12),
--     doctorID CHAR(12),
--     FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID),
--     FOREIGN KEY (doctorID) REFERENCES  DoctorDetails (doctorID),
--     PRIMARY KEY (patientID ,doctorID)
-- );

-- CREATE TABLE PatientLab (
--     patientID CHAR(12),
--     labID CHAR(12),
--     accessRight TINYINT,
--     FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID) ,
--     FOREIGN KEY (labID) REFERENCES  LabDetails (labID),
--     PRIMARY KEY (patientID ,labID )
-- );

-- CREATE TABLE PatientPharmacy (
--     patientID CHAR(12) ,
--     pharmacyID CHAR(12) ,
--     FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID) ,
--     FOREIGN KEY (pharmacyID) REFERENCES  PharmacyDetails (pharmacyID),
--     PRIMARY KEY( patientID,pharmacyID )
-- );

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
    bloodGroup CHAR(3),
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
    ePrescriptionID INTEGER, 
    patientID CHAR(12) ,
    doctorID CHAR(12) ,
    -- slNo INTEGER AUTO_INCREMENT,
    FOREIGN KEY (patientID) REFERENCES  PatientDetails (patientID) ,
    FOREIGN KEY (doctorID) REFERENCES  DoctorDetails (doctorID) ,
    -- PRIMARY KEY(ePrescriptionID ,patientID ,slNo)
    PRIMARY KEY(ePrescriptionID ,patientID)
);

CREATE TABLE MedicineDetails(
    ePrescriptionID INTEGER,
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
    ePrescriptionID INTEGER ,
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
    ePrescriptionID INTEGER,
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
    ePrescriptionID INTEGER NOT NULL,
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
    ePrescriptionID INTEGER NOT NULL,
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



INSERT INTO `PatientDetails` VALUES('1111','John Wayne','wayne@heye.com','1991-01-01','1, New Residency, 1st main, Indiranagar, Bangalore - 560093','M','826-016-17'),
('2222','Jane Doe','doe@heye.com','1976-02-02','2, New Residency, 1st main, Indiranagar, Bangalore - 560093','F','826-016-17'),
('3333','Ram Mohan','mohan@heye.com','1976-03-03','3, New Residency, 1st main, Indiranagar, Bangalore - 560093','M','826-016-17'),
('4444','Kelly Kapoor','kapoor@heye.com','1976-04-04','4, New Residency, 1st main, Indiranagar, Bangalore - 560093','F','826-016-17'); 






INSERT INTO DoctorDetails VALUES ('55555','Dwight Schrute','schrute@heye.com','1995-05-05','5, Old Residency, 5th Main, Jayanagar, Bangalore - 560043','M','5823663258','Physician'),
('66666','Michael Scott','scott@heye.com','1996-06-06','6, Old Residency, 6th Main, Jayanagar, Bangalore - 560043','M','5824544789','Cardiologist'),
('77777','Jim Halpert','halpert@heye.com','1997-07-07','7, Old Residency, 7th Main, Jayanagar, Bangalore - 560043','M','5823665658','Physician'),
('88888','Angela martin','martin@heye.com','1998-08-08','8, Old Residency, 8th Main, Jayanagar, Bangalore - 560043','F','5878663258','Surgeon'); 



INSERT INTO `LabDetails` VALUES ('123456','Clumax','Jayanagar 4th Block, Bangalore - 560054','clumaxjayanagar@clumax.com','25244248'),
('13579','Aarti Diagnostics','100 Ft road Indiranagar, Bangalore - 560094','adiagindiranagar@adiag.com','25244265'),
('654321','MedSol','JP Nagar 4th Block, Bangalore - 560054','msjpnagar@medsol.com','56934687'),
('97531','Lotus','100 Ft road Indiranagar, Bangalore - 560094','lotusindiranagar@lotus.com','25278948'); 




INSERT INTO `PharmacyDetails` VALUES ('111','KL Pharma','Jayanagar 4th Block, Bangalore - 560054','klpharma@yahoo.com','25288657'),
('222','SLN Pharma','100 Ft road Indiranagar, Bangalore - 560094','slnpharma@pharmacy.com','9865412365'),
('333','QWE Pharma','JP Nagar 4th Block, Bangalore - 560054','qwepharma@gmail.com','9852456558'),
('444','FP Pharma','Jayanagar 4th Block, Bangalore - 560054','fppharma@yahoo.com','45147584'); 



INSERT INTO `PatientLogin` VALUES 
('wayne@heye.com','blue'),
('doe@heye.com','red'),
('mohan@heye.com','yellow'),
('kapoor@heye.com','pink'); 

INSERT INTO `GenPatientHistory` VALUES('1111','O+','Pollen, Dust','Diabetes','Control Sugars','None Pending'),
('2222','B-','None','Breast Cancer','Increase protein intake','None Pending'),
('3333','AB+','Peanuts','None','None','None Pending'),
('4444','B+','Duct, Pollen','High Blood Pressure','None','None Pending'); 



INSERT INTO `DoctorLogin` VALUES 
('schrute@heye.com','maroon'),
('scott@heye.com','black'),
('halpert@heye.com','white'),
('martin@heye.com','green'); 



INSERT INTO `EPrescription` VALUES ('333','1111','55555'),
('930','1111','55555'),
('931','1111','77777'),
('932','1111','88888'),
('111','1111','77777'),
('543','2222','55555'),
('234','2222','88888'),
('345','3333','77777'),
('678','3333','66666'),
('301','3333','55555'),
('302','4444','88888'),
('174','4444','88888'),
('270','4444','88888'),
('950','4444','77777'),
('890','4444','66666'); 




INSERT INTO `MedicineDetails` VALUES ('333','cold, cough, fever','Calpol, Azithral, Cetzine','08:00:00','2001-04-09','2015-12-04'),
('930','sore throat, cold','Calpol, Azithral, Cetzine','08:00:00','2001-04-09','2015-12-04'),
('931','cold, cough, fever','Calpol, Azithral, Cetzine','08:00:00','2001-04-09','2015-12-04'),
('932','Possible fracture in ankle','Calpol, Azithral, Cetzine','08:00:00','2001-04-09','2015-12-04'),
('111','cold, fever','Calpol, Azithral, Cetzine','08:00:00','2001-04-09','2015-12-04'),
('543','dizziness, nausea','Cetaphil, ranzine','08:00:00','2001-04-09','2015-12-04'),
('234','stomach pain','Cetaphil, ranzine','08:00:00','2001-04-09','2015-12-04'),
('345','cold, fever','Calpol, Azithral, Cetzine','08:00:00','2001-04-09','2015-12-04'),
('678','chest pain','Cetaphil, ranzine','08:00:00','2001-04-09','2015-12-04'),
('301','Sprain in ankle','Cetaphil, ranzine','08:00:00','2001-04-09','2015-12-04'),
('302','back pain','Calpol, Azithral, Cetzine','08:00:00','2001-04-09','2015-12-04'),
('174','stomach pain','Calpol, Azithral, Cetzine','08:00:00','2001-04-09','2015-12-04'),
('270','Sprain in ankle','Cetaphil, ranzine','08:00:00','2001-04-09','2015-12-04'),
('950','cold, fever','Calpol, Azithral, Cetzine','08:00:00','2001-04-09','2015-12-04'),
('890','chest pain','Cetaphil, ranzine','08:00:00','2001-04-09','2015-12-04'); 


INSERT INTO `ELabRequestDocument` VALUES ('100','55555','301','3333','test type 2','Qui rerum ab sequi quidem eligendi. Nesciunt ut consequatur quasi adipisci enim omnis pariatur. Iste'),
('101','55555','543','2222','test type 1','Qui rerum ab sequi quidem eligendi. Nesciunt ut consequatur quasi adipisci enim omnis pariatur. Iste'),
('102','77777','111','1111','test type 2.','Qui rerum ab sequi quidem eligendi. Nesciunt ut consequatur quasi adipisci enim omnis pariatur. Iste'),
('103','88888','932','1111','test type 3','Qui rerum ab sequi quidem eligendi. Nesciunt ut consequatur quasi adipisci enim omnis pariatur. Iste'),
('104','88888','302','4444','test type 4','Qui rerum ab sequi quidem eligendi. Nesciunt ut consequatur quasi adipisci enim omnis pariatur. Iste'),
('105','88888','234','2222','test type 5','Qui rerum ab sequi quidem eligendi. Nesciunt ut consequatur quasi adipisci enim omnis pariatur. Iste'); 


INSERT INTO `LabRequest` VALUES 
('101','123456','1982-03-02','0'),
('102','13579','1982-03-02','0'),
('103','123456','1982-03-02','0'),
('104','654321','1982-03-02','0'),
('105','97531','1982-03-02','0'),
('100','123456','1982-03-02','0'); 


INSERT INTO `LabResponse` VALUES ('100','100','http://xyz.com/','All good, no problems','1999-08-31 17:28:06'),
('101','101','http://pqr.com/','All good, no problems','1999-08-31 17:28:06'),
('102','102','http://weisthiel.com/','All good, no problems','1999-08-31 17:28:06'),
('103','103','http://snatthiel.com/','All good, no problems','1999-08-31 17:28:06'),
('104','104','http://wthiel.com/','All good, no problems','1999-08-31 17:28:06'),
('105','105','http://ssnatiel.com/','All good, no problems','1999-08-31 17:28:06'); 


INSERT INTO `DoctorFeedback` VALUES ('100','10055','3333','55555','All good, no problems'),
('101','10145','2222','55555','All good, no problems'),
('102','10289','1111','77777','All good, no problems'),
('103','10345','1111','88888','All good, no problems'),
('104','10484','4444','88888','All good, no problems'),
('105','10545','2222','88888','All good, no problems'); 



INSERT INTO `LabLogin` VALUES 
('clumaxjayanagar@clumax.com','yellow'),
('adiagindiranagar@adiag.com','blue'),
('msjpnagar@medsol.com','olive'),
('lotusindiranagar@lotus.com','black'); 




INSERT INTO `PharmacyLogin` VALUES 
('klpharma@yahoo.com','green'),
('slnpharma@pharmacy.com','blue'),
('qwepharma@gmail.com','red'),
('fppharma@yahoo.com','pink'); 



INSERT INTO `MedicineRequest` VALUES 
('333','1111','222','2002-03-13 04:38:38','1'),
('930','1111','222','2002-03-13 04:38:38','1'),
('543','2222','111','2002-03-13 04:38:38','1'),
('345','3333','444','2002-03-13 04:38:38','1'),
('301','3333','444','2002-03-13 04:38:38','1'),
('302','4444','333','2002-03-13 04:38:38','1'),
('270','4444','333','2002-03-13 04:38:38','1'),
('174','4444','333','2002-03-13 04:38:38','1'); 




INSERT INTO `MedicineResponse` VALUES 
('100','333','1111','No comments'),
('101','930','1111','No comments'),
('102','543','2222','No comments'),
('103','345','3333','No comments'),
('104','301','3333','No comments'),
('105','302','4444','No comments'),
('106','270','4444','No comments'),
('107','174','4444','No comments'); 



INSERT INTO `DoctorAppointments` VALUES 
('333','1111','1988-05-13','17:36:46'),
('930','1111','1988-05-13','17:36:46'),
('543','2222','1988-05-13','17:36:46'),
('345','3333','1988-05-13','17:36:46'),
('301','3333','1988-05-13','17:36:46'),
('302','4444','1988-05-13','17:36:46'),
('270','4444','1988-05-13','17:36:46'),
('174','4444','1988-05-13','17:36:46'); 

INSERT INTO `MedicineReminder` VALUES 
('333','1111','1988-05-13','17:36:46'),
('930','1111','1988-05-13','17:36:46'),
('543','2222','1988-05-13','17:36:46'),
('345','3333','1988-05-13','17:36:46'),
('301','3333','1988-05-13','17:36:46'),
('302','4444','1988-05-13','17:36:46'),
('270','4444','1988-05-13','17:36:46'),
('174','4444','1988-05-13','17:36:46'); 



INSERT INTO `LabVisitReminder` VALUES ('3333','123456','100','1988-05-13','17:36:46'),
('1111','13579','102','1988-05-13','17:36:46'),
('1111','123456','103','1988-05-13','17:36:46'),
('4444','654321','104','1988-05-13','17:36:46'),
('2222','97531','105','1988-05-13','17:36:46');



INSERT INTO `DoctorVisitReminder` VALUES ('3333','55555','1988-05-13','17:36:46','no message'),
('1111','66666','1988-05-13','17:36:46','no message'),
('1111','77777','1988-05-13','17:36:46','no message'),
('4444','88888','1988-05-13','17:36:46','no message'),
('2222','55555','1988-05-13','17:36:46','no message');


