from hawkeye import mysql
import json
import datetime

conn = mysql.connect()
cursor =conn.cursor()


def loginCheck(email,password,acctType): 
    query = "SELECT password FROM {0}Login WHERE email='{1}'".format(acctType,email)   

    cursor.execute(query)
    # conn.commit()
    data = cursor.fetchall()
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
    conn = mysql.connect()
    print(mysql)
    #conn = mysql.connection
    query= "SELECT patientID, dateTimeStamp FROM doctorAppointments WHERE doctorID='{0}'".format("12")
    cursor =conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    somedict = {"patientID" : [x[0] for x in data],
                "dateTimeStamp" : [x[1] for x in data]}
    print("somedict is ",somedict)
    print(type(somedict))
    somedict1 = json.dumps(somedict,default=myconverter)
    print("somedict1 is ",somedict1)

    return somedict1

def isExistingUser(ID,acctType):
    query = "SELECT * FROM {0}Details WHERE {1}ID={2}".format(acctType,acctType.lower(),ID)


    res = cursor.execute(query)
    # conn.commit()

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
    insertDetailRes = cursor.execute(insertDetailQuery)
    insertLoginDetailRes = cursor.execute(insertLoginDetailQuery)
    conn.commit()

    if(insertDetailRes==1 and insertLoginDetailRes==1):
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