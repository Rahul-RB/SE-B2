from hawkeye import app
from flask import render_template

@app.route("/")
def home():
	return render_template("Home/home.html",title="User")

@app.route("/login")
def login():
	return render_template("Login/login.html")

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
