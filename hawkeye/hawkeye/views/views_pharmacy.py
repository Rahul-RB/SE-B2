from hawkeye import app
from hawkeye import mysql
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

#start pharmacyViewRequest
@app.route("/pharmacyViewRequest")
def pharmacyViewRequest():
    if ((not session.get("accType")=="Pharmacy") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    return render_template("Pharmacy/pharmacyViewRequest.html",title="Pharmacy",user=models_pharmacy.getUsernameByEmail(session.get("currentEmail"),session.get("accType")), userLoggedIn=True)


@app.route("/prescriptionRequest",methods=['GET'])
def prescriptionRequest():
    ID = models_pharmacy.getIDByEmail(session.get("currentEmail"),session.get("accType"))
    res = models_pharmacy.prescriptionRequest(ID)
    return jsonify(res)

@app.route("/prescriptionResponseUpdate",methods=["POST"])
def prescriptionResponseUpdate():
    payload = request.get_json()
    ID = models_pharmacy.getIDByEmail(session.get("currentEmail"),session.get("accType"))
    res = models_pharmacy.prescriptionResponseUpdate(payload,ID)
    return jsonify(res)

#end pharmacyViewRequest
