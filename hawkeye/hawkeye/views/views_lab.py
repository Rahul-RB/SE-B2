from hawkeye import app
# from hawkeye.forms import SignupForm 

from hawkeye.models import models_common 
from hawkeye.models import models_patient
from hawkeye.models import models_doctor
from hawkeye.models import models_pharmacy
from hawkeye.models import models_lab

from flask import Flask,render_template,redirect,url_for,flash, redirect, request, session, abort, jsonify, Response
from werkzeug import secure_filename
from flask import send_from_directory, send_file
import os
import datetime

app.secret_key = 'secretkeyhereplease'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc'])

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      if 'file' not in request.files:
          return redirect(url_for("lab"))
      file = request.files['file']
      if file.filename == '':
          return redirect( url_for("lab"))
      if file and allowed_file(file.filename):
          labRequestId=str(request.form["labReqId"])
          description=str(request.form["message"])
          print(labRequestId, description)
          format = "%Y%m%d%H%M%S"
          now = datetime.datetime.utcnow().strftime(format)
          filename = now + '_' +str(session["user_id"]) + '_' + file.filename
          filename = secure_filename(filename)
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          models_lab.putLabReponse(labRequestId, str(filename), description)
          return redirect(url_for("lab")) 
      return redirect( url_for("lab"))

@app.route("/labExistingResponse")
def labExistingResponse():
    if ((not session.get("accType")=="Lab") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    reqid=request.args.get('reqdata')
    email=session["currentEmail"]
    return render_template("Lab/labExistingResponse.html",
                            title="Lab",
                            useremail=email,
                            userid= session["user_id"],
                            labReqData=models_lab.getLabRequestDetails(email,reqid),
                            labPresData= models_lab.getLabPrescriptionDetails(reqid), 
                            filename= models_lab.getLabReportFilename(reqid),
                            userLoggedIn=True)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    print("---------------------",str(filename),"---------------")
    return send_file('uploads/'+str(filename),as_attachment=True)

@app.route("/lab")
def lab():
    if ((not session.get("accType")=="Lab") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    email=session["currentEmail"]
    session["user_id"]= models_lab.getLabId(email)[0][0];
    print(session["user_id"])
    return render_template("Lab/lab.html",
                            title="Lab", 
                            useremail=email,
                            labReqData=models_lab.getLabRequests(email), 
                            labResData= models_lab.getLabResponses(email),
                            labPieData= models_lab.getTop4Request(session["user_id"]),
                            lablineReqData= models_lab.getNumberOfRequests(session["user_id"]),
                            lablineRespData= models_lab.getNumberOfResponses(session["user_id"]),
                            userLoggedIn=True
                            )

@app.route("/labResponse")
def labResponse():
    if ((not session.get("accType")=="Lab") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    reqid=request.args.get('reqdata')
    email=session["currentEmail"]
    return render_template("Lab/labResponse.html",
                            title="Lab", 
                            useremail=email,
                            userid= session["user_id"],
                            labReqData=models_lab.getLabRequestDetails(email,reqid),
                            labPresData= models_lab.getLabPrescriptionDetails(reqid),
                            userLoggedIn=True
                            )
