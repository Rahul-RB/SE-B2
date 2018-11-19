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

@app.route("/eprescription",methods=["GET","POST"])
def eprescription():
    if((not session["accType"]=="Doctor") or (not session.get(session["accType"]+"LoggedIn"))):
        return redirect(url_for("login"),302)

    if(request.method == "GET"):
        return render_template("Doctor/eprescription.html",title="Doctor")

    elif(request.method == "POST"):
        POST_NAME = str(request.form["name"])
        POST_EMAIL = session["currentEmail"]
        # POST_SYMPTOMS = str(request.form["customSymptomName[]"])
        # print(POST_NAME)
        # POST_SYMPTOMS = request.POST.getall('customSymptomName[]')
        # POST_MEDICINES = request.POST.getall('customMedicineValue[]')
        lengthOfList=len(request.form.getlist('customSymptomName'))
        # print("length is ",lengthOfList)
        # print("request.form.getlist(customSymptomName):", POST_NAME,request.form.getlist('customSymptomName'))
        # print("request.form.getlist(customMedicineValue):",request.form.getlist('customMedicineValue'))
        # print("request.form.getlist(labTestTypeName):",request.form.getlist('labTestTypeName'))
        # print("request.form.getlist(timing1):",request.form.getlist('timing1'))
        # print("request.form.getlist(timing2):",request.form.getlist('timing2'))
        POST_SYMPTOMS = request.form.getlist('customSymptomName')
        POST_MEDICINES = request.form.getlist('customMedicineValue')
        POST_LABTEST_TYPE = request.form.getlist('labTestTypeName')
        POST_LABTEST_DESCRIPTION = request.form.getlist('labTestDescriptionValue')
        POST_MEDICINE_FREQUENCY = []
        for i in range(1,lengthOfList+1):
            # print("request.form.getlist(timing%c) is ",str(i))
            # print(request.form.getlist('timing'+str(i)))
            POST_MEDICINE_FREQUENCY.append(request.form.getlist('timing'+str(i)))
        # print(session["currentEmail"])
        # print(session["accType"])
        # print("POST_MEDICINE_FREQUENCY is ", POST_MEDICINE_FREQUENCY)

        res = models_doctor.insertNewPrescription(POST_EMAIL,POST_NAME,POST_SYMPTOMS,POST_MEDICINES,\
            POST_MEDICINE_FREQUENCY,POST_LABTEST_TYPE,POST_LABTEST_DESCRIPTION)

        if(res == True):
            return render_template("Doctor/eprescription.html",title="Doctor")

        # print("request.form.getlist('timing2):",request.form.getlist('timing2))
        # print("length jus ", request.form.getlist('customSymptomName'))

        # print(POST_NAME, POST_SYMPTOMS, POST_MEDICINES)

        # for symptoms, medicines in zip(request.form.getlist('customSymptomName[]'),request.form.getlist('customMedicineValue[]')):
        #     print(symptoms,medicines)

        # for labTestType, labTestDescription in zip(request.form.getlist('labTestTypeName[]'),request.form.getlist('labTestDescriptionValue[]')):
        #     print(labTestType,labTestDescription)

    else:
        flash("Error")

    # return render_template("Doctor/eprescription.html",title="Doctor")

@app.route("/ctime/firstupdate",methods=['GET'])
def ctime_firstupdate():
    result = models_doctor.firstAppointmentUpdate(session["currentEmail"])
    # print("result is: ", result)
    # print("In ctime:",session["currentEmail"])
    return jsonify(result=result)


@app.route("/ctime",methods=['GET'])
def ctime():
    result = models_doctor.checkForAppointments(session["currentEmail"])
    # print("result is: ", result)
    # print("In ctime:",session["currentEmail"])
    return jsonify(result=result)

@app.route("/doctor")
def doctor():
    if((not session.get("accType")=="Doctor") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    print("Doctor:",session["currentEmail"])
    
    return render_template("Doctor/doctor.html",title="Doctor", userLoggedIn=True)

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

@app.route("/checkDoctorsHistory", methods=["GET","POST"])
def checkDoctorsHistory():
    if(request.method=="GET"):
        searchBy = request.args.get('searchBy',"",type=str)
        print("searchBy is ", searchBy)
        POST_EMAIL = session["currentEmail"]
        
        res = models_doctor.checkDoctorsHistory(POST_EMAIL, searchBy)

        return jsonify(res)
