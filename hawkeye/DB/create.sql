DROP DATABASE test;
CREATE DATABASE test;

USE test;

CREATE TABLE Patient_details (
    patient_id integer ,
    name text,
    email varchar,
    dob datetime,
    address varchar(100),
    sex text(1),
    phone_no integer ,
    PRIMARY KEY (patient_id )
);

CREATE TABLE Doctor_details (
    doctor_id integer,
    doctor_name text,
    email varchar,
    dob datetime,
    address varchar(100),
    sex text(1),
    phone_no integer,
    designation varchar(100),
    PRIMARY KEY(doctor_id)
);

CREATE TABLE Lab_details (
    lab_id integer PRIMARY KEY AUTO_INCREMENT,
    lab_name varchar(100),
    address varchar(100),
    email varchar(100),
    phone_no integer    
);

CREATE TABLE Pharmacy_details (
    pharmacy_id integer PRIMARY KEY AUTO_INCREMENT,
    pharmacy_name text(1),
    address varchar(100),
    email varchar(100),
    phone_no integer
);


CREATE TABLE Consultation (
    patient_id integer ,
    doctor_id integer ,
    FOREIGN KEY (patient_id) REFERENCES  Patient_details (patient_id),
    FOREIGN KEY (doctor_id) REFERENCES  Doctor_details (doctor_id),
    PRIMARY KEY (patient_id ,doctor_id )
);

CREATE TABLE Patient_lab (
    patient_id integer ,
    lab_id integer ,
    access_right integer(1) ,
    FOREIGN KEY (patient_id) REFERENCES  Patient_details (patient_id) ,
    FOREIGN KEY (lab_id) REFERENCES  Lab_details (lab_id),
    PRIMARY KEY (patient_id ,lab_id )
);

CREATE TABLE Patient_pharmacy (
    patient_id integer ,
    pharmacy_id integer ,
    FOREIGN KEY (patient_id) REFERENCES  Patient_details (patient_id) ,
    FOREIGN KEY (pharmacy_id) REFERENCES  Pharmacy_details (pharmacy_id),
    PRIMARY KEY( patient_id,pharmacy_id )
);

CREATE TABLE Patient_login (
    patient_id integer,
    password varchar(100),
    hint_question varchar(100),
    hint_answer varchar(100) ,
    FOREIGN KEY (patient_id) REFERENCES  Patient_details (patient_id) ,
    PRIMARY KEY (patient_id)
);


CREATE TABLE Gen_patient_history (
    patient_id integer ,
    blood_group varchar(100),
    allergies varchar(100),
    hereditary_problems varchar(100),
    diet_advice varchar(100),
    injection_history varchar(100) ,
    FOREIGN KEY (patient_id) REFERENCES  Patient_details (patient_id),
    PRIMARY KEY( patient_id)
);

CREATE TABLE Medicine_reminder (
    patient_id integer NOT NULL,
    med_reminder_id integer PRIMARY KEY AUTO_INCREMENT,
    medicine_name varchar(100),
    description varchar(100),
    alarm_date datetime,
    alarm_duration integer,
    no_of_doses integer ,
    FOREIGN KEY (patient_id) REFERENCES  Patient_details (patient_id),
    UNIQUE( patient_id,med_reminder_id)
);

CREATE TABLE Visit_reminder (
    patient_id integer NOT NULL,
    visit_reminder_id integer PRIMARY KEY AUTO_INCREMENT,
    doc_name text,
    description varchar(100),
    alarm_date datetime,
    alarm_duration integer ,
    FOREIGN KEY (patient_id) REFERENCES  Patient_details (patient_id),
    UNIQUE(patient_id,visit_reminder_id)
);

CREATE TABLE Doctor_login (
    doctor_id integer PRIMARY KEY ,
    password varchar(100),
    hint_question varchar(100),
    hint_answer varchar(100) ,
    FOREIGN KEY (doctor_id) REFERENCES  Doctor_details (doctor_id)
);

CREATE TABLE E_prescription (
    eprescription_id integer,
    patient_id integer ,
    sl_no integer,
    symptoms varchar(100),
    medicine_suggestion varchar(100),
    remarks varchar(100),
    doctor_id integer ,
    FOREIGN KEY (patient_id) REFERENCES  Patient_details (patient_id) ,
    FOREIGN KEY (doctor_id) REFERENCES  Doctor_details (doctor_id) ,
    PRIMARY KEY(eprescription_id ,patient_id ,sl_no)
);

CREATE TABLE Prescription (
    patient_id integer NOT NULL ,
    prescription_id integer PRIMARY KEY AUTO_INCREMENT,
    time_stamp datetime,
    file_location varchar(100) ,
    FOREIGN KEY (patient_id) REFERENCES  Patient_details (patient_id),
    UNIQUE (patient_id, prescription_id)
);

CREATE TABLE Doctor_feedback (
    report_id integer ,
    prescription_id integer,
    patient_id integer,
    doctor_id integer,
    suggestions varchar(100),
    FOREIGN KEY (doctor_id) REFERENCES  Doctor_details (doctor_id) ,
    FOREIGN KEY (patient_id) REFERENCES  Patient_details (patient_id),
    PRIMARY KEY(report_id,prescription_id)
    
);



CREATE TABLE Lab_login (
    lab_id integer,
    password varchar(100),
    hint_question varchar(100),
    hint_answer varchar(100) ,
    FOREIGN KEY (lab_id) REFERENCES  Lab_details (lab_id),
    PRIMARY KEY( lab_id)
);


CREATE TABLE Lab_request (
    lab_request_id integer PRIMARY KEY AUTO_INCREMENT,
    prescription_id integer ,
    lab_id integer,
    patient_id integer,
    doctor_id integer,
    test_type varchar(100),
    description varchar(100),
    time_stamp datetime,
    isPending integer ,
    FOREIGN KEY (lab_id) REFERENCES  Lab_details (lab_id) ,
    FOREIGN KEY (patient_id) REFERENCES  Patient_details (patient_id) ,
    FOREIGN KEY (doctor_id) REFERENCES  Doctor_details (doctor_id)
);

CREATE TABLE Lab_response (
    lab_request_id integer NOT NULL ,
    result_link integer,
    report_id integer PRIMARY KEY AUTO_INCREMENT,
    description varchar(100),
    time_stamp datetime,
    FOREIGN KEY(lab_request_id) REFERENCES Lab_request(lab_request_id),
    UNIQUE(lab_request_id,report_id)
);

CREATE TABLE Pharmacy_login (
    pharmacy_id integer ,
    password varchar(100),
    hint_question varchar(100),
    hint_answer varchar(100) ,
    FOREIGN KEY (pharmacy_id) REFERENCES  Pharmacy_details (pharmacy_id) ,
    PRIMARY KEY(pharmacy_id)

);

CREATE TABLE Medicine_request (
    medicine_req_id integer PRIMARY KEY AUTO_INCREMENT,
    patient_id integer,
    pharmacy_id integer,
    eprescription_id integer,
    pickup_time datetime ,
    FOREIGN KEY (pharmacy_id) REFERENCES  Pharmacy_details (pharmacy_id)  ,
    FOREIGN KEY (patient_id) REFERENCES  Patient_details (patient_id)  ,
    FOREIGN KEY (eprescription_id) REFERENCES  E_prescription (eprescription_id)
);

CREATE TABLE Medicine_response (
    medicine_response_id integer PRIMARY KEY AUTO_INCREMENT,
    medicine_req_id integer,
    remarks varchar(100) ,
    FOREIGN KEY (medicine_req_id) REFERENCES  Medicine_request (medicine_req_id) 
);




