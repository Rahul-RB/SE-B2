from hawkeye import app
# from hawkeye.forms import SignupForm 

from hawkeye import models 
from flask import Flask,render_template,redirect,url_for,flash, redirect, request, session, abort, jsonify
from werkzeug import secure_filename
from flask import send_from_directory, send_file
import os
import datetime
UPLOAD_FOLDER = './hawkeye/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'secretkeyhereplease'

@app.route("/")
def home():
    try:
        res = session["{0}LoggedIn".format(session["accType"])]
        return render_template("Home/home.html",title="User",userLoggedIn=True)
    except Exception as e:
        return render_template("Home/home.html",title="User",userLoggedIn=False)

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
        result = models.loginCheck(POST_EMAIL,POST_PASSWORD,POST_ACC_TYPE)
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

@app.route("/eprescription",methods=["GET","POST"])
def eprescription():
    if((not session["accType"]=="Doctor") or (not session.get(session["accType"]+"LoggedIn"))):
        return redirect(url_for("login"),302)

    if(request.method == "GET"):
        return render_template("Doctor/eprescription.html",title="Doctor")

    elif(request.method == "POST"):
        POST_NAME = str(request.form["name"])
        POST_EMAIL = session["currentEmail"]
        # POST_SYMPTOMS = str(request.form["customSymptomName[]"])
        # print(POST_NAME)
        # POST_SYMPTOMS = request.POST.getall('customSymptomName[]')
        # POST_MEDICINES = request.POST.getall('customMedicineValue[]')
        lengthOfList=len(request.form.getlist('customSymptomName'))
        # print("length is ",lengthOfList)
        # print("request.form.getlist(customSymptomName):", POST_NAME,request.form.getlist('customSymptomName'))
        # print("request.form.getlist(customMedicineValue):",request.form.getlist('customMedicineValue'))
        # print("request.form.getlist(labTestTypeName):",request.form.getlist('labTestTypeName'))
        # print("request.form.getlist(timing1):",request.form.getlist('timing1'))
        # print("request.form.getlist(timing2):",request.form.getlist('timing2'))
        POST_SYMPTOMS = request.form.getlist('customSymptomName')
        POST_MEDICINES = request.form.getlist('customMedicineValue')
        POST_LABTEST_TYPE = request.form.getlist('labTestTypeName')
        POST_LABTEST_DESCRIPTION = request.form.getlist('labTestDescriptionValue')
        POST_MEDICINE_FREQUENCY = []
        for i in range(1,lengthOfList+1):
            # print("request.form.getlist(timing%c) is ",str(i))
            # print(request.form.getlist('timing'+str(i)))
            POST_MEDICINE_FREQUENCY.append(request.form.getlist('timing'+str(i)))
        # print(session["currentEmail"])
        # print(session["accType"])
        # print("POST_MEDICINE_FREQUENCY is ", POST_MEDICINE_FREQUENCY)

        res = models.insertNewPrescription(POST_EMAIL,POST_NAME,POST_SYMPTOMS,POST_MEDICINES,\
            POST_MEDICINE_FREQUENCY,POST_LABTEST_TYPE,POST_LABTEST_DESCRIPTION)

        if(res == True):
            return render_template("Doctor/eprescription.html",title="Doctor")

        # print("request.form.getlist('timing2):",request.form.getlist('timing2))
        # print("length jus ", request.form.getlist('customSymptomName'))

        # print(POST_NAME, POST_SYMPTOMS, POST_MEDICINES)

        # for symptoms, medicines in zip(request.form.getlist('customSymptomName[]'),request.form.getlist('customMedicineValue[]')):
        #     print(symptoms,medicines)

        # for labTestType, labTestDescription in zip(request.form.getlist('labTestTypeName[]'),request.form.getlist('labTestDescriptionValue[]')):
        #     print(labTestType,labTestDescription)

    else:
        flash("Error")


    
    # return render_template("Doctor/eprescription.html",title="Doctor")

@app.route("/logout")
def logout():
    if not session.get(session.get("accType")+"LoggedIn"):
        return redirect(url_for("login"),302)
    session[session.get("accType")+"LoggedIn"] = False
    session["accType"] = None
    session["currentEmail"] = None
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
    if ((not session.get("accType")=="Patient") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    return render_template("Patient/patient.html",title="Patient",user=models.getUsernameByEmail(session.get("currentEmail"),session.get("accType")), userLoggedIn=True)

@app.route("/ctime",methods=['GET'])
def ctime():
    result = models.checkForAppointments(session["currentEmail"])
    # print("result is: ", result)
    # print("In ctime:",session["currentEmail"])
    return jsonify(result=result)

@app.route("/doctor")
def doctor():
    if((not session.get("accType")=="Doctor") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    print("Doctor:",session["currentEmail"])
    
    return render_template("Doctor/doctor.html",title="Doctor", userLoggedIn=True)

@app.route("/prescription_history")
def prescription_history():
    if((not session.get("accType")=="Doctor") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    return render_template("Doctor/prescription_history.html",title="Doctor", userLoggedIn=True)

@app.route("/history")
def history():
    if((not session.get("accType")=="Doctor") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    
    return render_template("Doctor/history.html",title="Doctor", userLoggedIn=True)

@app.route("/pharmacy")
def pharmacy():
    if ((not session.get("accType")=="Pharmacy") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    
    return render_template("Pharmacy/pharmacy.html",title="Pharmacy", userLoggedIn=True)

@app.route("/pharmacy_prescription")
def pharmacy_prescription():
    if ((not session.get("accType")=="Pharmacy") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    
    return render_template("Pharmacy/pharmacy_prescription.html",title="Pharmacy", userLoggedIn=True)

@app.route("/lab")
def lab():
    if ((not session.get("accType")=="Lab") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    email=session["currentEmail"]
    session["user_id"]= models.getLabId(email)[0][0];
    print(session["user_id"])
    return render_template("Lab/lab.html",title="Lab", useremail=email,labReqData=models.getLabRequests(email), labResData= models.getLabResponses(email))

@app.route("/labResponse")
def labResponse():
    if ((not session.get("accType")=="Lab") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    reqid=request.args.get('reqdata')
    email=session["currentEmail"]
    return render_template("Lab/labResponse.html",title="Lab", useremail=email,userid= session["user_id"],labReqData=models.getLabRequestDetails(email,reqid),labPresData= models.getLabPrescriptionDetails(reqid))
   
@app.route("/searchPatientHistory", methods=["GET","POST"])
def searchPatientHistory():
    if(request.method=="GET"):
        patientID = request.args.get('patientID',"",type=str)
        # inpText = request.args.get('inpText', "", type=str)
        print("patientID is ",patientID)
        res = models.searchPatientHistory(patientID)
        # return render_template("Doctor/searchPatientHistory.html",title="Doctor")
        return jsonify(res)

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
          format = "%Y-%m-%dT%H:%M:%S"
          now = datetime.datetime.utcnow().strftime(format)
          filename = now + '_' +str(session["user_id"]) + '_' + file.filename
          filename = secure_filename(filename)
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          models.putLabReponse(labRequestId, str(filename), description)
          return redirect(url_for("lab")) 
      return redirect( url_for("lab"))

@app.route("/labExistingResponse")
def labExistingResponse():
    if ((not session.get("accType")=="Lab") or (not session.get(session.get("accType")+"LoggedIn"))):
        return redirect(url_for("login"),302)
    reqid=request.args.get('reqdata')
    email=session["currentEmail"]
    return render_template("Lab/labExistingResponse.html",title="Lab",
        useremail=email,userid= session["user_id"],labReqData=models.getLabRequestDetails(email,reqid),
        labPresData= models.getLabPrescriptionDetails(reqid), filename= models.getLabReportFilename(reqid))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    print("---------------------",str(filename),"---------------")
    #filename = str(filename)
    return send_file('uploads/'+str(filename),as_attachment=True)

@app.route("/patientCalendarReminderUpdate")
def patientCalendarReminderUpdate():
    patientID = models.getIDByEmail(session.get("currentEmail"),session.get("accType"))
    res = models.patientCalendarReminderUpdate(patientID)
    return jsonify(res)

@app.route("/patientDoctorAppointment",methods=["GET","POST"])
def patientDoctorAppointment():
    if(request.method=="GET"): #GET all appointment
        patientID = models.getIDByEmail(session.get("currentEmail"),session.get("accType"))
        res = models.patientDoctorAppointment(patientID,None,"GET")
        return jsonify(res)

    elif(request.method=="POST"):#POST a new appointment
        patientID = models.getIDByEmail(session.get("currentEmail"),session.get("accType"))
        doctorID = request.form["doctorID"]
        res = models.patientDoctorAppointment(patientID,doctorID,"POST")
        return jsonify(res)
