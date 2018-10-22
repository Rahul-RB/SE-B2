from hawkeye import mysql

conn = mysql.connect()
cursor =conn.cursor()


def loginCheck(email,password,acctType):
    query = "SELECT password from "+ acctType+"Login where email='"+email+"'"   

    cursor.execute(query)
    # conn.commit()
    data = cursor.fetchall()
    try:
        if(password!=data[0][0]):
            return False
        else:
            return True
    except Exception as e:
        return False

def isExistingUser(ID,acctType):
    query = "SELECT * from "+ acctType+"Details where " + acctType.lower() + "ID='"+ID+"'"

    res = cursor.execute(query)
    # conn.commit()

    if(res==0):
        return False
    else:
        return True

def insertNewUser(inpDict,acctType):
    if(acctType=="Patient"):
        insertDetailQuery = "INSERT INTO PatientDetails VALUES ( '" +\
                inpDict["patientID"] + "','" +\
                inpDict["name"] + "','" +\
                inpDict["email"] + "','" +\
                inpDict["dob"] + "','" +\
                inpDict["address"] + "','" +\
                inpDict["sex"] + "','" +\
                inpDict["phoneNO"] + "'" +\
            ")"
        insertLoginDetailQuery = "INSERT INTO PatientLogin VALUES('"+\
                inpDict["email"] + "','" +\
                inpDict["password"] + "'" +\
            ")"     

    elif(acctType=="Doctor"):
        insertDetailQuery = "INSERT INTO DoctorDetails VALUES ('" +\
                inpDict["doctorID"] + "','" +\
                inpDict["doctorName"] + "','" +\
                inpDict["email"] + "','" +\
                inpDict["dob"] + "','" +\
                inpDict["address"] + "','" +\
                inpDict["sex"] + "','" +\
                inpDict["phoneNO"] + "','" +\
                inpDict["designation"] + "'" +\
            ")"
        insertLoginDetailQuery = "INSERT INTO DoctorLogin VALUES ('"+\
                inpDict["email"] + "','" +\
                inpDict["password"] + "'" +\
            ")"    
        
    elif(acctType=="Lab"):
        insertDetailQuery = "INSERT INTO LabDetails VALUES ('" +\
                inpDict["labID"] + "','" +\
                inpDict["labName"] + "','" +\
                inpDict["address"] + "','" +\
                inpDict["email"] + "','" +\
                inpDict["phoneNO"] + "'" +\
            ")"
        insertLoginDetailQuery = "INSERT INTO LabLogin VALUES ('" +\
                inpDict["email"] + "','" +\
                inpDict["password"] + "'" +\
            ")" 
        
    elif(acctType=="Pharmacy"):
        insertDetailQuery = "INSERT INTO PharmacyDetails VALUES ('" +\
                inpDict["pharmacyID"] + "','" +\
                inpDict["pharmacyName"] + "','" +\
                inpDict["address"] + "','" +\
                inpDict["email"] + "','"+\
                inpDict["phoneNO"] + "'" +\
            ")"
        insertLoginDetailQuery = "INSERT INTO PharmacyLogin VALUES ('" +\
                inpDict["email"] + "','" +\
                inpDict["password"] + "'" +\
            ")" 
    else:
        return("Error")

    print(insertDetailQuery)
    print(insertLoginDetailQuery)
    res1 = cursor.execute(insertDetailQuery)
    res2 = cursor.execute(insertLoginDetailQuery)
    conn.commit()

    if(res1==1 and res2==1):
        return True
    else:
        return False


def getUsernameByEmail(email,acctType):
    query = "SELECT "+ acctType.lower() + "Name from "+ acctType +"Details where email='"+email+"'"
    print(query)
    res = cursor.execute(query)

    data = cursor.fetchall()
    return data[0][0]

def getIDByEmail(email,acctType):
    query = "SELECT "+ acctType.lower() + "ID from "+ acctType +"Details where email='"+email+"'"
    res = cursor.execute(query)

    data = cursor.fetchall()
    return data[0][0]

    symptoms,medicineSuggestion,timeToTake,startDate,endDate,

def patientMedReminderUpdate(patientID):
    res = {
        "TakeMedicine":None,
        "OrderMedicine":None
    }
    # Take Medicine updates:
    query = "SELECT symptoms,medicineSuggestion,timeToTake,startDate,endDate \
            FROM MedicineDetails \
            WHERE ePrescriptionID IN (SELECT ePrescriptionID FROM MedicineReminder WHERE patientID='"+patientID+"')"
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    takeMedicineRes = {}

    for i,result in enumerate(data):
        takeMedicineRes[i] = str(result[0])+","+str(result[1])+","+str(result[2])+","+str(result[3])+","+str(result[4])

    res["TakeMedicine"] = takeMedicineRes
    
    # Order Medicine updates:
    query = "SELECT ePrescriptionID,reminderDate,reminderTime FROM MedicineReminder WHERE patientID='"+patientID+"'"
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    orderMedicineRes = {}

    for i,result in enumerate(data):
        orderMedicineRes[i] = str(result[0])+","+str(result[1])+","+str(result[2])

    res["OrderMedicine"] = orderMedicineRes

    return res

    # patientID,labID,labRequestDocumentID,reminderDate,reminderTime
def patientLabVisitReminderUpdate(patientID):
    query = "SELECT labID,labRequestDocumentID,reminderDate,reminderTime FROM LabVisitReminder WHERE patientID='"+patientID+"'"
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    labVisitRes = {}

    for i,result in enumerate(data):
        labVisitRes[i] = str(result[0])+","+str(result[1])+","+str(result[2])+","+str(result[3])

    return labVisitRes

def patientDocVisitReminderUpdate(patientID):
    query = "SELECT doctorID,reminderDate,reminderTime FROM DoctorVisitReminder WHERE patientID='"+patientID+"'"
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    docVisitRes = {}

    for i,result in enumerate(data):
        docVisitRes[i] = str(result[0])+","+str(result[1])+","+str(result[2])

    return docVisitRes

def patientCalendarReminderUpdate(patientID):
    medReminders = patientMedReminderUpdate(patientID)
    res = {
        "TakeMedicine":medReminders["TakeMedicine"],
        "OrderMedicine":medReminders["OrderMedicine"],
        "DocVisit":patientDocVisitReminderUpdate(patientID),
        "LabVisit":patientLabVisitReminderUpdate(patientID)
    }

    return res

def patientDoctorAppointmentUpdate(patientID,doctorID,method):
    if(method=="GET"):
        query = "SELECT doctorID,dateStamp,pickATime \
                FROM DoctorAppointments \
                WHERE patientID='"+patientID+"' AND addedToDoctorCalendar=0"
        queryResults = cursor.execute(query)
        data = cursor.fetchall()
        doctorApptRes = {}

        for i,result in enumerate(data):
            doctorApptRes[i] = str(result[0])+","+str(result[1])+","+str(result[2])


        return doctorApptRes

    elif(method=="POST"):
        # get date from form
        # Check all times already input in for that date
        # return json of available times.
        query = "SELECT"