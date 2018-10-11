from hawkeye import app
# from hawkeye.forms import SignupForm 

from hawkeye import models 
from flask import Flask,render_template,redirect,url_for,flash, redirect, request, session, abort


app.secret_key = 'secretkeyhereplease'

@app.route("/")
def home():
    if not session.get("loggedIn"):
        return redirect(url_for("login"),302)

    return render_template("Home/home.html",title="User")

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

        # Make DB query to see if User with 'email' and 'acc_type'
        # has the same password as in the DB.
        result = models.loginCheck(POST_EMAIL,POST_PASSWORD,POST_ACC_TYPE)
        if result=="Error":
            flash("Error")

        if result==True:
            session['loggedIn'] = True
            print("RESULT")
            return redirect(url_for("home"))
        else:
            flash('wrong password!')
            return redirect(url_for("login"))
    else:
        flash("Error")

@app.route("/logout")
def logout():
    if not session.get("loggedIn"):
        return redirect(url_for("login"),302)
    session['loggedIn'] = False
    return redirect(url_for("home"))

@app.route("/register")
def register():
    return redirect(url_for("register_patient"))

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
        if not models.isExistingUser(inpDict["patientID"],"Patient"): # Insert if not existing
            res = models.insertNewUser(inpDict,"Patient")
            if(res==True):
                return redirect(url_for("home"))
            else:
                flash("Error")

    else:
        flash("Error")

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
        if not models.isExistingUser(inpDict["doctorID"],"Doctor"): # Insert if not existing
            res = models.insertNewUser(inpDict,"Doctor")
            if(res==True):
                return redirect(url_for("home"))
            else:
                flash("Error")

    else:
        flash("Error")

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
        if not models.isExistingUser(inpDict["labID"],"Lab"): # Insert if not existing
            res = models.insertNewUser(inpDict,"Lab")
            if(res==True):
                return redirect(url_for("home"))
            else:
                flash("Error")

    else:
        flash("Error")

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
        if not models.isExistingUser(inpDict["pharmacyID"],"Pharmacy"): # Insert if not existing
            res = models.insertNewUser(inpDict,"Pharmacy")
            if(res==True):
                return redirect(url_for("home"))
            else:
                flash("Error")

    else:
        flash("Error")

@app.route("/patient")
def patient():
    if not session.get("loggedIn"):
        return redirect(url_for("login"),302)
    return render_template("Patient/patient.html",title="Patient",user="BABA")

@app.route("/doctor")
def doctor():
    if not session.get("loggedIn"):
        return redirect(url_for("login"),302)
    return render_template("Doctor/doctor.html",title="Doctor")

@app.route("/prescription_history")
def prescription_history():
    if not session.get("loggedIn"):
        return redirect(url_for("login"),302)
    return render_template("Doctor/prescription_history.html",title="Doctor")

@app.route("/history")
def history():
    if not session.get("loggedIn"):
        return redirect(url_for("login"),302)
    
    return render_template("Doctor/history.html",title="Doctor")

@app.route("/eprescription")
def eprescription():
    if not session.get("loggedIn"):
        return redirect(url_for("login"),302)
    
    return render_template("Doctor/eprescription.html",title="Doctor")

@app.route("/pharmacy")
def pharmacy():
    if not session.get("loggedIn"):
        return redirect(url_for("login"),302)
    
    return render_template("Pharmacy/pharmacy.html",title="Pharmacy")

@app.route("/pharmacy_prescription")
def pharmacy_prescription():
    if not session.get("loggedIn"):
        return redirect(url_for("login"),302)
    
    return render_template("Pharmacy/pharmacy_prescription.html",title="Pharmacy")
