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


# used for updation of eprescription form which is filled by doctor
@app.route("/eprescription",methods=["GET","POST"])
def eprescription():
    if((not session["accType"]=="Doctor") or (not session.get(session["accType"]+"LoggedIn"))):
        return redirect(url_for("login"),302)

    if(request.method == "GET"):
        return render_template("Doctor/eprescription.html",title="Doctor")

    elif(request.method == "POST"):
        POST_NAME = str(request.form["name"])
        POST_EMAIL = session["currentEmail"]
    
        lengthOfList=len(request.form.getlist('customSymptomName'))
     
        POST_SYMPTOMS = request.form.getlist('customSymptomName')
        POST_MEDICINES = request.form.getlist('customMedicineValue')
        POST_LABTEST_TYPE = request.form.getlist('labTestTypeName')
        POST_LABTEST_DESCRIPTION = request.form.getlist('labTestDescriptionValue')
        POST_MEDICINE_FREQUENCY = []
        for i in range(1,lengthOfList+1):
            
            POST_MEDICINE_FREQUENCY.append(request.form.getlist('timing'+str(i)))
        

        res = models_doctor.insertNewPrescription(POST_EMAIL,POST_NAME,POST_SYMPTOMS,POST_MEDICINES,\
            POST_MEDICINE_FREQUENCY,POST_LABTEST_TYPE,POST_LABTEST_DESCRIPTION)

        if(res == True):
            return render_template("Doctor/eprescription.html",title="Doctor")

      
    else:
        flash("Error")


# updating the calendar for the first time
@app.route("/ctime/firstupdate",methods=['GET'])
def ctime_firstupdate():
    result = models_doctor.firstAppointmentUpdate(session["currentEmail"])

    return jsonify(result=result)

# used for periodic refresh for calendar updates
@app.route("/ctime",methods=['GET'])
def ctime():
    result = models_doctor.checkForAppointments(session["currentEmail"])

    return jsonify(result=result)

# used for home page of doctor
@app.route("/doctor")
def doctor():
    if((not session.get("accType")=="Doctor") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    print("Doctor:",session["currentEmail"])
    
    return render_template("Doctor/doctor.html",
                            title="Doctor", 
                            userLoggedIn=True,
                            docName=models_common.getUsernameByEmail(session.get("currentEmail"),session.get("accType")))


@app.route("/prescription_history")
def prescription_history():
    if((not session.get("accType")=="Doctor") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    return render_template("Doctor/prescription_history.html",title="Doctor", userLoggedIn=True)

@app.route("/history")
def history():
    if((not session.get("accType")=="Doctor") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    
    return render_template("Doctor/history.html",title="Doctor", userLoggedIn=True)

# used for checking the history of patients in search bar by displaying prescription history   
@app.route("/searchPatientHistory", methods=["GET","POST"])
def searchPatientHistory():
    if(request.method=="GET"):
        patientID = request.args.get('patientID',"",type=str)
        # inpText = request.args.get('inpText', "", type=str)
        print("patientID is ",patientID)
        res = models_doctor.searchPatientHistory(patientID)
        print("res in views file is ", res)
        # return render_template("Doctor/searchPatientHistory.html",title="Doctor")
        return jsonify(res)

# used for checking the history of number of patients seen by doctor
@app.route("/checkDoctorsHistory", methods=["GET","POST"])
def checkDoctorsHistory():
    if(request.method=="GET"):
        searchBy = request.args.get('searchBy',"",type=str)
        print("searchBy is ", searchBy)
        POST_EMAIL = session["currentEmail"]
        
        res = models_doctor.checkDoctorsHistory(POST_EMAIL, searchBy)

        return jsonify(res)
