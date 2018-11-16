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

#pharmacy
@app.route("/pharmacy")
def pharmacy():
    if ((not session.get("accType")=="Pharmacy") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    email=session["currentEmail"]
    #session["user_id"] = models.getpharmacyID(email)[0][0];
    #print(session["user_id"])
    #print("-----------------",models.getpharmacytitle(email)[0])
    return render_template("Pharmacy/pharmacy.html",title="Pharmacy", data=models.getpharmacytitle(email))
	
	
#pharmacy_prescription
@app.route("/pharmacy_prescription",methods=["POST"])
def pharmacy_prescription():
    if ((not session.get("accType")=="Pharmacy") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    email=session["currentEmail"]
    patid=request.form.get('patID')
    #email=session["currentEmail"]
    #print(patid)
    print(models.getpharmacyPres(email,patid), models.getEprescitionDetails(email,patid))
	return render_template("Pharmacy/pharmacy_prescription.html",title="Pharmacy",data=models.getpharmacytitle(email), pharPresData=models.getpharmacyPres(email,patid),details= models.getEprescitionDetails(email,patid),userLoggedIn=True)
	
#end function