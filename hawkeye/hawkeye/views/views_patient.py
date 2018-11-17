from hawkeye import app
# from hawkeye.forms import SignupForm 

from hawkeye.models import models_common 
from hawkeye.models import models_patient
from hawkeye.models import models_doctor
from hawkeye.models import models_pharmacy
from hawkeye.models import models_lab

from flask import Flask,render_template,redirect,url_for,flash, redirect, request, session, abort, jsonify, Response
from werkzeug import secure_filename
from flask import send_from_directory
import os
import datetime

app.secret_key = 'secretkeyhereplease'


@app.route("/patient")
def patient():
    if ((not session.get("accType")=="Patient") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    return render_template("Patient/patient.html",title="Patient",user=models_common.getUsernameByEmail(session.get("currentEmail"),session.get("accType")), userLoggedIn=True)

@app.route("/patientCalendarReminderUpdate")
def patientCalendarReminderUpdate():
    patientID = models_common.getIDByEmail(session.get("currentEmail"),session.get("accType"))
    res = models_patient.patientCalendarReminderUpdate(patientID)
    return jsonify(res)
    
@app.route("/patientDoctorAppointment",methods=["GET","POST"])
def patientDoctorAppointment():
    if(request.method=="GET"): #GET all appointment
        patientID = models_common.getIDByEmail(session.get("currentEmail"),session.get("accType"))
        res = models_patient.patientDoctorAppointment(patientID,None,"GET")
        return jsonify(res)

    elif(request.method=="POST"):#POST a new appointment
        patientID = models_common.getIDByEmail(session.get("currentEmail"),session.get("accType"))
        payload = request.get_json() #Converts incoming JSON into Python Dictionary
        print("--------------------------------")
        print(payload)
        res = models_patient.patientDoctorAppointment(patientID,payload,"POST")
        return jsonify(res)

@app.route("/patientLabRequest",methods=["GET","POST"])
def patientLabRequest():
    if (request.method == "GET"): #GET all appointments
        patientID = models_common.getIDByEmail(session.get("currentEmail"),session.get("accType"))
        res = models_patient.patientLabRequest(patientID,None,"GET")
        return jsonify(res)

    elif(request.method=="POST"):#POST a new appointment
        labID = models_common.getIDByEmail(session.get("currentEmail"),session.get("accType"))
        payload = request.get_json() #Converts incoming JSON into Python Dictionary
        print("--------------------------------")
        print(payload)
        res = models_patient.patientLabRequest(labID,payload,"POST")
        return jsonify(res)

@app.route("/patientMedicineRequest",methods=["GET","POST"])
def patientMedicineRequest():
    if(request.method=="GET"): #GET all requests
        patientID = models_common.getIDByEmail(session.get("currentEmail"),session.get("accType"))
        res = models_patient.patientMedicineRequest(patientID,None,"GET") #None is no payload
        return jsonify(res)

    elif(request.method=="POST"):#POST a new request
        labID = models_common.getIDByEmail(session.get("currentEmail"),session.get("accType"))
        payload = request.get_json() #Converts incoming JSON into Python Dictionary
        print("--------------------------------")
        print(payload)
        res = models_patient.patientMedicineRequest(labID,payload,"POST")
        return jsonify(res)

@app.route("/getAvailableTimeSlots",methods=["GET"])
def getAvailableTimeSlots():
    doctorID = request.args.get("doctorID", "", type=str)
    inpDate = request.args.get("inpDate", "", type=str)
    res = models_patient.getAvailableTimeSlots(doctorID,inpDate)
    return jsonify(res)

@app.route("/patientFetchPrescriptions",methods=["GET"])
def patientFetchPrescriptions():
    patientID = models_common.getIDByEmail(session.get("currentEmail"),session.get("accType"))
    res = models_patient.patientFetchPrescriptions(patientID)
    return jsonify(res)


@app.route("/patientLabResponse",methods=["GET"])
def patientLabResponse():
    patientID = models_common.getIDByEmail(session.get("currentEmail"),session.get("accType"))
    res = models_patient.patientLabResponse(patientID)
    return jsonify(res)

@app.route("/patientMedicineResponse",methods=["GET"])
def patientMedicineResponse():
    patientID = models_common.getIDByEmail(session.get("currentEmail"),session.get("accType"))
    res = models_patient.patientMedicineResponse(patientID)
    return jsonify(res)

@app.route("/getMedicineDetailsByEPrescriptionID",methods=["GET"])
def getMedicineDetailsByEPrescriptionID():
    ID = request.args.get("ID", "", type=str)
    print("---------ID-----------",ID)
    res = models_patient.getMedicineDetailsByEPrescriptionID(ID)
    return jsonify(res)

