from hawkeye import app
from flask import Flask,render_template,redirect,url_for

@app.route("/base")
def base():
	return render_template("Base/base.html",title="User")

@app.route("/")
def home():
	return render_template("Home/home.html",title="User")

@app.route("/login")
def login():
	return render_template("Login/login.html")

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