from hawkeye import mysql
import json
import datetime

# conn = mysql.connect()



def loginCheck(email,password,acctType): 
    query = "SELECT password FROM {0}Login WHERE email='{1}'".format(acctType,email)   
    
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    cursor.execute(query)
    # mysql.get_db().commit()
    data = cursor.fetchall()
    cursor.close()

    conn.close()
    print("loginCheck data:",data)
    try:
        if(password!=data[0][0]):
            return False
        else:
            return True
    except Exception as e:
        return False
      
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def checkForAppointments(email):
    # conn = mysql.connect()
    # print(mysql)
    #conn = mysql.connection
    query= "SELECT patientID, dateTimeStamp FROM doctorAppointments WHERE doctorID='{0}'".format("12")
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    conn.close()
    somedict = {"patientID" : [x[0] for x in data],
                "dateTimeStamp" : [x[1] for x in data]}
    print("somedict is ",somedict)
    print(type(somedict))
    somedict1 = json.dumps(somedict,default=myconverter)
    print("somedict1 is ",somedict1)

    return somedict1

def isExistingUser(ID,acctType):
    query = "SELECT * FROM {0}Details WHERE {1}ID={2}".format(acctType,acctType.lower(),ID)

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    res = cursor.execute(query)
    cursor.close()

    conn.close()

    if(res==0):
        return False
    else:
        return True

def insertNewUser(inpDict,acctType):
    if(acctType=="Patient"):
        insertDetailQuery = "INSERT INTO PatientDetails VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(\
                    inpDict["patientID"],
                    inpDict["name"],
                    inpDict["email"],
                    inpDict["dob"],
                    inpDict["address"],
                    inpDict["sex"],
                    inpDict["phoneNO"]
                )

    elif(acctType=="Doctor"):
        insertDetailQuery = "INSERT INTO DoctorDetails VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(\
                    inpDict["doctorID"],
                    inpDict["doctorName"],
                    inpDict["email"],
                    inpDict["dob"],
                    inpDict["address"],
                    inpDict["sex"],
                    inpDict["phoneNO"],
                    inpDict["designation"]
                )

    elif(acctType=="Lab"):
        insertDetailQuery = "INSERT INTO LabDetails VALUES ('{0}','{1}','{2}','{3}','{4}')".format(\
                inpDict["labID"],
                inpDict["labName"],
                inpDict["address"],
                inpDict["email"],
                inpDict["phoneNO"]
            )
        
    elif(acctType=="Pharmacy"):
        insertDetailQuery = "INSERT INTO PharmacyDetails VALUES ('{0}','{1}','{2}','{3}','{4}')".format(\
                inpDict["pharmacyID"],
                inpDict["pharmacyName"],
                inpDict["address"],
                inpDict["email"],
                inpDict["phoneNO"]
            )
    else:
        return("Error")
    
    insertLoginDetailQuery = "INSERT INTO {0}Login VALUES('{1}','{2}')".format(\
            acctType,
            inpDict["email"],
            inpDict["password"]
        )

    print(insertDetailQuery)
    print(insertLoginDetailQuery)
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    insertDetailRes = cursor.execute(insertDetailQuery)
    insertLoginDetailRes = cursor.execute(insertLoginDetailQuery)
    mysql.get_db().commit()
    cursor.close()

    conn.close()
    if(insertDetailRes==1 and insertLoginDetailRes==1):
        return True
    else:
        return False


def getUsernameByEmail(email,acctType):
    query = "SELECT "+ acctType.lower() + "Name from "+ acctType +"Details where email='"+email+"'"
    print(query)
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    res = cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    conn.close()
    return data[0][0]

def getIDByEmail(email,acctType):
    query = "SELECT "+ acctType.lower() + "ID from "+ acctType +"Details where email='"+email+"'"

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    res = cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    conn.close()

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
            WHERE ePrescriptionID IN (SELECT ePrescriptionID FROM MedicineReminder WHERE patientID='{0}')".format(patientID)
    
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    takeMedicineRes = {}

    for i,result in enumerate(data):
        takeMedicineRes[i] = str(result[0])+","+str(result[1])+","+str(result[2])+","+str(result[3])+","+str(result[4])

    res["TakeMedicine"] = takeMedicineRes
    
    # Order Medicine updates:
    query = "SELECT ePrescriptionID,reminderDate,reminderTime FROM MedicineReminder WHERE patientID='{0}'".format(patientID)
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    conn.close()
    orderMedicineRes = {}

    for i,result in enumerate(data):
        orderMedicineRes[i] = str(result[0])+","+str(result[1])+","+str(result[2])

    res["OrderMedicine"] = orderMedicineRes

    return res

    # patientID,labID,labRequestDocumentID,reminderDate,reminderTime
def patientLabVisitReminderUpdate(patientID):
    query = "SELECT labID,labRequestDocumentID,reminderDate,reminderTime FROM LabVisitReminder WHERE patientID='{0}'".format(patientID)

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    conn.close()
    labVisitRes = {}

    for i,result in enumerate(data):
        labVisitRes[i] = str(result[0])+","+str(result[1])+","+str(result[2])+","+str(result[3])

    return labVisitRes

def patientDocVisitReminderUpdate(patientID):
    query = "SELECT doctorID,reminderDate,reminderTime FROM DoctorVisitReminder WHERE patientID='{0}'".format(patientID)

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    conn.close()
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

def patientDoctorAppointment(patientID,payload,method):
    if(method=="GET"):
        query = "SELECT doctorID,dateStamp,pickATime FROM DoctorAppointments WHERE patientID='{0}' AND addedToDoctorCalendar=0".format(\
                patientID
            )

        conn = mysql.connect()
        cursor =mysql.get_db().cursor()
        queryResults = cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        conn.close()
        
        doctorApptRes = {}

        for i,result in enumerate(data):
            doctorApptRes[i] = str(result[0])+","+str(result[1])+","+str(result[2])

        return doctorApptRes

    elif(method=="POST"):
        # get date from form
        # Check all times already input in for that date
        # return json of available times.
        # query = "SELECT"

        query = "INSERT INTO DoctorAppointments VALUES ('{0}','{1}','{2}','{3}','{4}')".format(\
                patientID,
                payload["doctorID"],
                payload["apptDate"],
                payload["apptTime"],
                1
            )
        conn = mysql.connect()

        cursor =mysql.get_db().cursor()
        queryResults = cursor.execute(query)
        data = cursor.fetchall()

        mysql.get_db().commit()

        cursor.close()
        conn.close()

        if queryResults==1:
            return {"Success":True}
        else:
            return {"Failed":True}

def getDetailsByName(inpText,resType):
    query = "SELECT {0}Name,{0}ID FROM {1}Details WHERE {0}Name LIKE '{2}%'".format(resType.lower(),resType,inpText)
    conn = mysql.connect()

    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    res = {}
    if(queryResults!=0):
        for i,result in enumerate(data):
            res[i] = [result[0],result[1]]
        print("res:",res)
        return res
    else:
        return {"data":None}

def patientLabRequest(labID,payload,method):
    if(method=="GET"):
        query = "SELECT labID,dateStamp FROM LabRequest WHERE labID='{0}' AND isPending=1".format(\
                labID
            )

        conn = mysql.connect()
        cursor =mysql.get_db().cursor()
        queryResults = cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        conn.close()
        
        labReqRes = {}

        for i,result in enumerate(data):
            labReqRes[i] = str(result[0])+","+str(result[1])+","+str(result[2])

        return labReqRes

    elif(method=="POST"):
        # get date from form
        # return json of available times.

        query = "INSERT INTO LabRequest VALUES ('{0}','{1}','{2}','{3}')".format(\
                payload["labDocID"],
                labID,
                payload["apptDate"],
                1
            )
        conn = mysql.connect()

        cursor =mysql.get_db().cursor()
        queryResults = cursor.execute(query)
        data = cursor.fetchall()

        mysql.get_db().commit()

        cursor.close()
        conn.close()

        if queryResults==1:
            return {"Success":True}
        else:
            return {"Failed":True}

def getAvailableTimeSlots(doctorID,inpDate):
    query = "SELECT pickATime FROM DoctorAppointments WHERE doctorID='{0}' AND dateStamp='{1}'".format(\
                doctorID,
                inpDate
            )

    conn = mysql.connect()

    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    res = {}

    for i,result in enumerate(data):
        res[i] = str(result[i]) # str to convert datetime.timedelta to a time representation

    cursor.close()
    conn.close()

    return res