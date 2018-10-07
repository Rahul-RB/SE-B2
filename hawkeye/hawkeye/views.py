from hawkeye import app
from flask import render_template
@app.route("/")
def hello():
	return render_template("Home/home.html",user="User",title="Home")