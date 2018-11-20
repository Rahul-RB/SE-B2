@app.route("/pharmacy")
def pharmacy():
	if ((not session.get("accType")=="Pharmacy") or (not session.get(session.get("accType")+"LoggedIn"))):
		return redirect(url_for("login"),302)
	email=session["currentEmail"]
	#session["user_id"] = models.getpharmacyID(email)[0][0];
	#print(session["user_id"])
	print(email)
	#print("hi in views",models.graph(email))
	#print("Yo in in views",models.getNumberOfRequests(email))
	#print("-----------------",models.getpharmacytitle(email)[0])
	return render_template("Pharmacy/pharmacy.html",title="Pharmacy", data=models_pharmacy.getpharmacytitle(email),pharmacyReqData=models_pharmacy.getNumberOfRequests(email),pie=models_pharmacy.graph(email),userLoggedIn=True)