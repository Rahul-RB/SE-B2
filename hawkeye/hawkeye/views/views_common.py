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

# Rahul's
@app.route("/")
def home():
    try:
        res = session["{0}LoggedIn".format(session["accType"])]
        return render_template("Home/home.html",title="User",userLoggedIn=True)
    except Exception as e:
        return render_template("Home/home.html",title="User",userLoggedIn=False)

# Rahul's
@app.route("/login",methods=["GET","POST"])
def login():
    if (request.method == "GET"):
        return render_template("Login/login.html")

    elif (request.method == "POST"):
        POST_EMAIL = str(request.form["email"])
        POST_PASSWORD = str(request.form["password"])
        POST_ACC_TYPE = str(request.form["accType"])
        
        print(POST_EMAIL)
        print(POST_PASSWORD)
        print(POST_ACC_TYPE)

        session["accType"] = POST_ACC_TYPE
        session["currentEmail"] = POST_EMAIL

        # Make DB query to see if User with 'email' and 'acc_type'
        # has the same password as in the DB.
        result = models_common.loginCheck(POST_EMAIL,POST_PASSWORD,POST_ACC_TYPE)
        if (result=="Error"):
            flash("Error")

        if (result==True):
            session[POST_ACC_TYPE+"LoggedIn"] = True
            print("Correct Login, redirecting to:",url_for("home"))
            return redirect(url_for("home"))
        else:
            flash('wrong password!')
            return redirect(url_for("login"))
    else:
        flash("Error")


# Rahul's
@app.route("/logout")
def logout():
    try:
        res = session.get(session.get("accType")+"LoggedIn")
    except Exception as e:
        res = None
        pass
    if not res:
        return redirect(url_for("login"),302)
    
    session[session.get("accType")+"LoggedIn"] = False
    session["accType"] = None
    session["currentEmail"] = None
    return redirect(url_for("home"))

# Rahul's
@app.route("/register")
def register():
    return redirect(url_for("register_patient"))

# Rahul's
@app.route("/register_patient",methods=["GET","POST"])
def register_patient():
    if (request.method=="GET"):
        return render_template("Register/register_patient.html",title="Patient")

    elif (request.method == "POST"):
        inpDict = {
            "patientID"  : str(request.form["patientID"]), 
            "name"       : str(request.form["patientName"]), 
            "email"      : str(request.form["email"]), 
            "dob"        : str(request.form["dob"]), 
            "address"    : str(request.form["address"]), 
            "sex"        : str(request.form["sex"]), 
            "phoneNO"    : str(request.form["phoneNo"]),
            "password"   : str(request.form["password"]), 
        }
        if not models_common.isExistingUser(inpDict["patientID"],"Patient"): # Insert if not existing
            res = models_common.insertNewUser(inpDict,"Patient")
            if(res==True):
                return redirect(url_for("home"))
            else:
                flash("Error")

    else:
        flash("Error")

# Rahul's
@app.route("/register_doctor",methods=["GET","POST"])
def register_doctor():
    if (request.method=="GET"):
        return render_template("Register/register_doctor.html",title="Doctor")

    elif (request.method == "POST"):
        inpDict = {
            "doctorID"    : str(request.form["doctorID"]), 
            "doctorName"  : str(request.form["doctorName"]), 
            "email"       : str(request.form["email"]), 
            "dob"         : str(request.form["dob"]), 
            "address"     : str(request.form["address"]), 
            "sex"         : str(request.form["sex"]), 
            "phoneNO"     : str(request.form["phoneNo"]), 
            "designation" : str(request.form["designation"]),
            "password"    : str(request.form["password"]), 
        }
        if not models_common.isExistingUser(inpDict["doctorID"],"Doctor"): # Insert if not existing
            res = models_common.insertNewUser(inpDict,"Doctor")
            if(res==True):
                return redirect(url_for("home"))
            else:
                flash("Error")

    else:
        flash("Error")

# Rahul's
@app.route("/register_lab",methods=["GET","POST"])
def register_lab():
    if (request.method=="GET"):
        return render_template("Register/register_lab.html",title="Lab")

    elif (request.method == "POST"):
        inpDict = {
            "labID"    : str(request.form["labID"]),
            "labName"  : str(request.form["labName"]),
            "address"  : str(request.form["address"]),
            "email"    : str(request.form["email"]),
            "phoneNO"  : str(request.form["phoneNo"]),
            "password" : str(request.form["password"]), 
        }
        if not models_common.isExistingUser(inpDict["labID"],"Lab"): # Insert if not existing
            res = models_common.insertNewUser(inpDict,"Lab")
            if(res==True):
                return redirect(url_for("home"))
            else:
                flash("Error")

    else:
        flash("Error")

# Rahul's
@app.route("/register_pharmacy",methods=["GET","POST"])
def register_pharmacy():
    if (request.method=="GET"):
        return render_template("Register/register_pharmacy.html",title="Pharmacy")

    elif (request.method == "POST"):
        inpDict = {
            "pharmacyID"   : str(request.form["pharmacyID"]),
            "pharmacyName" : str(request.form["pharmacyName"]),
            "address"      : str(request.form["address"]),
            "email"        : str(request.form["email"]),
            "phoneNO"      : str(request.form["phoneNo"]),
            "password"     : str(request.form["password"]),
        }
        if not models_common.isExistingUser(inpDict["pharmacyID"],"Pharmacy"): # Insert if not existing
            res = models_common.insertNewUser(inpDict,"Pharmacy")
            if(res==True):
                return redirect(url_for("home"))
            else:
                flash("Error")

    else:
        flash("Error")


# Rahul's
@app.route("/commonSearch",methods=["GET"])
def commonSearch():
    inpText = request.args.get('inpText', "", type=str)
    resType = request.args.get('resType', "", type=str)
    # print(inpText,resType)
    res = models_common.getDetailsByName(inpText,resType)
    return jsonify(res)


# Rahul's
@app.route("/getDetailsByID",methods=["GET"])
def getDetailsByID():
    ID = request.args.get("ID", "", type=str)
    accType = request.args.get("accType", "", type=str)
    res = models_common.getDetailsByID(ID,accType)
    return jsonify(res)

