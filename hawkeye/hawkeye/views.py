from hawkeye import app
from flask import render_template

@app.route("/")
def home():
	return render_template("Home/home.html",title="User")

@app.route("/login")
def login():
	return render_template("Login/login.html")
