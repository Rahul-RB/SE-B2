from hawkeye import app
# from hawkeye.forms import SignupForm 

from hawkeye import models 
from flask import Flask,render_template,redirect,url_for,flash, redirect, request, session, abort


app.secret_key = 'secretkeyhereplease'

@app.route("/")
def home():
    print(session.get("loggedIn"))
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
        result = models.loginCheck(POST_EMAIL,POST_PASSWORD)
        if result:
            session['loggedIn'] = True
            print("RESULT")
            return redirect(url_for("home"))
        else:
            flash('wrong password!')
        return redirect(url_for("home"))
    else:
        flash("Error")

@app.route("/logout")
def logout():
    session['loggedIn'] = False
    return redirect(url_for("home"))

@app.route("/register")
def register():
    return redirect(url_for("register_patient"))

@app.route("/register_patient")
def register_patient():
    return render_template("Register/register_patient.html",title="Patient")

@app.route("/register_doctor")
def register_doctor():
    return render_template("Register/register_doctor.html",title="Doctor")

@app.route("/register_lab")
def register_lab():
    return render_template("Register/register_lab.html",title="Lab")

@app.route("/register_pharmacy")
def register_pharmacy():
    return render_template("Register/register_pharmacy.html",title="Pharmacy")

@app.route("/patient")
def patient():
    return render_template("Patient/patient.html",title="Patient",user="BABA")

@app.route("/doctor")
def doctor():
    return render_template("Doctor/doctor.html",title="Doctor")

@app.route("/prescription_history")
def prescription_history():
    return render_template("Doctor/prescription_history.html",title="Doctor")

@app.route("/history")
def history():
    return render_template("Doctor/history.html",title="Doctor")

@app.route("/eprescription")
def eprescription():
    return render_template("Doctor/eprescription.html",title="Doctor")

@app.route("/pharmacy")
def pharmacy():
    return render_template("Pharmacy/pharmacy.html",title="Pharmacy")

@app.route("/pharmacy_prescription")
def pharmacy_prescription():
    return render_template("Pharmacy/pharmacy_prescription.html",title="Pharmacy")
