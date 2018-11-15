from hawkeye import mysql
import json
import datetime
import time  
import numpy as np
import matplotlib.pyplot as plt  

# conn = mysql.connect()

def loginCheck(email,password,acctType): 
    query = "SELECT password FROM {0}Login WHERE email='{1}'".format(acctType,email)   
    
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    cursor.execute(query)
    # conn.commit()
    data = cursor.fetchall()

    # mysql.get_db().commit()
    # data = cursor.fetchall()
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

def firstAppointmentUpdate(email):
    conn = mysql.connect()
    print(mysql)
    #conn = mysql.connection
    query= "SELECT patientID, dateStamp, pickATime from DoctorAppointments where addedToDoctorCalendar=1 and doctorID in (SELECT doctorID from DoctorDetails where email='" + email + "') for update"
    cursor =conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    # print("data is ",data)
    if(data != ''):
        somedict = {"patientID" : [x[0] for x in data],
                    "start_datetime" : [datetime.datetime.combine(x[1],(datetime.datetime.min + x[2]).time()) for x in data],
                    "end_datetime" : [datetime.datetime.combine(x[1],(datetime.datetime.min + x[2]+datetime.timedelta(minutes=30)).time()) for x in data]
                    }
        print(somedict)
        return json.dumps(somedict,default=myconverter)
    return {}


def checkForAppointments(email):
    # conn = mysql.connect()
    # print(mysql)
    # #conn = mysql.connection
    # query= "SELECT patientID, dateTimeStamp from doctorAppointments where doctorID='"+'12'+"'"
    # cursor =conn.cursor()
    # cursor.execute(query)
    # data = cursor.fetchall()
    # somedict = {"patientID" : [x[0] for x in data],
    #             "dateTimeStamp" : [x[1] for x in data]}
    # print("somedict is ",somedict)
    # print(type(somedict))
    # somedict1 = json.dumps(somedict,default=myconverter)
    # print("somedict1 is ",somedict1)

    # return somedict1
    #try:
    conn = mysql.connect()
    conn.autocommit = False
    print(mysql)
    #conn = mysql.connection
    query= "SELECT patientID, dateStamp, pickATime from DoctorAppointments where addedToDoctorCalendar=0 and doctorID in (SELECT doctorID from DoctorDetails where email='" + email + "') for update"
    cursor =conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    # print("data is ",data)
    if(data != ''):
        somedict = {"patientID" : [x[0] for x in data],
                    "start_datetime" : [datetime.datetime.combine(x[1],(datetime.datetime.min + x[2]).time()) for x in data],
                    "end_datetime" : [datetime.datetime.combine(x[1],(datetime.datetime.min + x[2]+datetime.timedelta(minutes=30)).time()) for x in data]
                    }
        # print("somedict is ",somedict)
        # print(type(somedict))
        somedict1 = json.dumps(somedict,default=myconverter)
        # print("somedict1 is ",somedict1)
        if len(somedict) > 0: # ensure that the dictionary is not empty
            # print("\nInside if top\n")
            query1= "UPDATE DoctorAppointments SET  addedToDoctorCalendar=1 where addedToDoctorCalendar=0 and doctorID in (SELECT doctorID from DoctorDetails where email='" + email + "')"
            cursor1 =conn.cursor()
            cursor1.execute(query1)
            # print("\nInside if\n")
        conn.commit()
        # print("Hello Hii I am inside try block\n")
        return somedict1
    else:
        somedict1 = dict()
        return somedict1

# def insertIntoPrescription():




def searchPatientHistory(patientID):
    conn = mysql.connect()
    conn.autocommit = False
    query = "SELECT ePrescriptionID, doctorID from EPrescription where patientID='" + patientID + "'"
    cursor =conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    global_dict=dict(dict())
    if(data != ''):
        somedict = {"ePrescriptionID": [x[0] for x in data],
                    "doctorID": [x[1] for x in data]
                    }
        print("somedict of search is ", somedict)
        for i in range(len(somedict["ePrescriptionID"])):
            json_data = {}
            json_data["ePrescriptionID"] = somedict["ePrescriptionID"][i]
            query1 = "SELECT symptoms, medicineSuggestion from MedicineDetails where ePrescriptionID='" + str(somedict["ePrescriptionID"][i]) + "'"
            cursor.execute(query1)
            data = cursor.fetchall()
            json_data["symptoms"] = []
            json_data["medicineSuggestion"] = []
            for j in range(len(data)):
                json_data["symptoms"].append(data[j][0])
                json_data["medicineSuggestion"].append(data[j][1])

            query2 = "SELECT testType, description FROM ELabRequestDocument where ePrescriptionID='" + str(somedict["ePrescriptionID"][i]) + "'"
            cursor.execute(query2)
            data2 = cursor.fetchall()
            json_data["testType"] = []
            json_data["description"] = []
            for j in range(len(data2)):
                json_data["testType"].append(data2[j][0])
                json_data["description"].append(data2[j][1])
            print(json_data)
            print(type(json_data))
            global_dict[i] = json_data
            # print(data2)
        print("global_dict is ", global_dict)

        return global_dict 


def checkDoctorsHistory(doctorsEmail,searchBy):
    conn = mysql.connect()
    conn.autocommit = False
    # if searchBy=="month":
    splitSearchBy = searchBy.split("-")
    splitByYear = splitSearchBy[0]
    splitByMonth = splitSearchBy[1]
    now = datetime.datetime.now()
    cur_month = str(now.month)
    cur_day = str(now.day)
    countPatientsMonth=0
    countPatientsYear=0
    countPatientsToday=0
    query = "SELECT doctorID from DoctorDetails where email='" + doctorsEmail + "'"
    cursor =conn.cursor()
    cursor.execute(query)
    doctorIDquery = cursor.fetchall()
    doctorID = str(doctorIDquery[0][0])
    query2 = "SELECT ePrescriptionID from EPrescription where doctorID='" + doctorID + "'"
    cursor.execute(query2)
    ePrescriptionquery = cursor.fetchall()
    for i in range(len(ePrescriptionquery)):
        monthsSplitList = ePrescriptionquery[i][0].split("-")
        if(monthsSplitList[1] == splitByMonth):
            countPatientsMonth += 1
        if(monthsSplitList[2] == cur_day):
            countPatientsToday += 1
        if(monthsSplitList[0] == splitByYear):
            countPatientsYear += 1

    results = computeDaysMonthwise(ePrescriptionquery,splitByYear)
    # plotBarChart(results)
    print("countPatientsToday is ", countPatientsToday)
    print("countPatientsMonth is ", countPatientsMonth)
    print("countPatientsYear is ", countPatientsYear)
    return {"countPatientsYear" : countPatientsYear,"countPatientsToday" : countPatientsToday, "countPatientsMonth": countPatientsMonth, "monthWiseDataThatYear": results}
        # print("eprescriptions are ", ePrescriptionquery)
    # elif searchBy=="year":
    #     now = datetime.datetime.now()
    #     cur_year = str(now.year)
    #     cur_day = str(now.day)
    #     countPatientsMonth=0
    #     countPatientsToday=0
    #     query = "SELECT doctorID from DoctorDetails where email='" + doctorsEmail + "'"
    #     cursor =conn.cursor()
    #     cursor.execute(query)
    #     doctorIDquery = cursor.fetchall()
    #     doctorID = str(doctorIDquery[0][0])
    #     query2 = "SELECT ePrescriptionID from EPrescription where doctorID='" + doctorID + "'"
    #     cursor.execute(query2)
    #     ePrescriptionquery = cursor.fetchall()
    #     for i in range(len(ePrescriptionquery)):
    #         monthsSplitList = ePrescriptionquery[i][0].split("-")
    #         if(monthsSplitList[1] == cur_year):
    #             countPatientsMonth += 1
    #         if(monthsSplitList[2] == cur_day):
    #             countPatientsToday += 1
    #     print("countPatientsToday is ", countPatientsToday)
    #     print("countPatientsMonth is ", countPatientsMonth)
    #     return {"countPatientsToday" : countPatientsToday, "countPatientsMonth": countPatientsMonth}
def computeDaysMonthwise(ePrescriptionquery, splitByYear):
    print("eprescription quer is ", ePrescriptionquery)
    print("splitByYear is ", splitByYear)

    monthsList = [0 for i in range(12)]
    print("monthslist before is is ", monthsList)

    for i in range(len(ePrescriptionquery)):
        monthsSplitList = ePrescriptionquery[i][0].split("-")
        if(monthsSplitList[1] == '1' and monthsSplitList[0] == splitByYear):
            monthsList[0] += 1
        elif(monthsSplitList[1] == '2' and monthsSplitList[0] == splitByYear):
            monthsList[1] += 1
        elif(monthsSplitList[1] == '3' and monthsSplitList[0] == splitByYear):
            monthsList[2] += 1
        elif(monthsSplitList[1] == '4' and monthsSplitList[0] == splitByYear):
            monthsList[3] += 1
        elif(monthsSplitList[1] == '5' and monthsSplitList[0] == splitByYear):
            monthsList[4] += 1
        elif(monthsSplitList[1] == '6' and monthsSplitList[0] == splitByYear):
            monthsList[5] += 1
        elif(monthsSplitList[1] == '7' and monthsSplitList[0] == splitByYear):
            monthsList[6] += 1
        elif(monthsSplitList[1] == '8' and monthsSplitList[0] == splitByYear):
            monthsList[7] += 1
        elif(monthsSplitList[1] == '9' and monthsSplitList[0] == splitByYear):
            monthsList[8] += 1
        elif(monthsSplitList[1] == '10' and monthsSplitList[0] == splitByYear):
            monthsList[9] += 1
        elif(monthsSplitList[1] == '11' and monthsSplitList[0] == splitByYear):
            monthsList[10] += 1
        elif(monthsSplitList[1] == '12' and monthsSplitList[0] == splitByYear):
            monthsList[11] += 1
    print("monthslist is ", monthsList)
    return monthsList
            
def plotBarChart(monthsList):
    months = ("Jan","Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug","Sept", "Oct", "Nov", "Dec")
    y_pos = np.arange(len(months))
    plt.bar(y_pos,monthsList,align='center',alpha=0.5)
    plt.xticks(y_pos,months)
    plt.ylabel('Number of Patients seen')
    plt.show()

    
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


def insertNewPrescription(doctorsEmail, patientName, symptoms, medicines, medFrequency, testType, testDescription) :

    conn = mysql.connect()
    conn.autocommit = False
    query = "SELECT doctorID from DoctorDetails where email='" + doctorsEmail + "'"
    cursor =conn.cursor()
    cursor.execute(query)
    doctorIDquery = cursor.fetchall()
    doctorID = str(doctorIDquery[0][0])
    # print("doctor ID in models file is ",str(doctorID[0][0]))
    query1 = "SELECT patientID from PatientDetails where patientName='" + patientName + "'"
    cursor1 = conn.cursor()
    cursor1.execute(query1)
    patientIDquery = cursor1.fetchall()
    patientID = str(patientIDquery[0][0])
    # print("patient ID in models file is ",patientID)

    now = datetime.datetime.now()
    ePrescriptionRandom = (str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '-' + str(now.hour) \
    + '-' + str(now.minute)  + '-' + str(now.second))

    print("ePrescription random ID is ", ePrescriptionRandom)

    insertIntoEprescription = "INSERT INTO EPrescription VALUES ('" + ePrescriptionRandom + "', '" +\
        patientID + "','" +\
        doctorID + "'" +\
        ")"

    cursor1.execute(insertIntoEprescription)
    conn.commit()

    print("querystring is ",insertIntoEprescription)
    today = datetime.datetime.today()
    nextdate = today + datetime.timedelta(days=10)
    currentDate = today.strftime("%d/%m/%y")
    endDate = nextdate.strftime("%d/%m/%y")

    for num_symptms in range(len(medFrequency)):
        print("num_symptms is ", num_symptms)
        for freq in range(len(medFrequency[num_symptms])):
            print("freq is ", freq)
            insertIntoMedicineDetails = "INSERT INTO MedicineDetails VALUES ('" + ePrescriptionRandom + "', '" +\
            symptoms[num_symptms] + "','" +\
            medicines[num_symptms] + "','" +\
            medFrequency[num_symptms][freq] + "','" +\
            currentDate + "','" +\
            endDate + "'" +\
            ")"
           
            print("insertIntoMedicineDetails is ",insertIntoMedicineDetails)
            cursor1.execute(insertIntoMedicineDetails)
            conn.commit()


    for num_testType in range(len(testType)):
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        insertIntoELabRequest = "INSERT INTO ELabRequestDocument (doctorID, ePrescriptionID, patientID, testType, description) VALUES ('" + doctorID + "','" +\
        ePrescriptionRandom + "','" +\
        patientID + "','" +\
        testType[num_testType] + "','" +\
        testDescription[num_testType] + "'" +\
        ")"

        print(insertIntoELabRequest)
        cursor1.execute(insertIntoELabRequest)
        conn.commit()


    return True

# START : DEEPIKA'S FUNCTIONS
def getLabRequests(email):
    query="SELECT  a.patientID, a.doctorID , a.labRequestDocumentID FROM ELabRequestDocument a ,LabRequest lr, LabLogin lo, LabDetails ld where lo.email= '"+email+"' and ld.email = lo.email and ld.labid= lr.labid and lr.labRequestDocumentID=a.labRequestDocumentID ;"
    cursor.execute(query)
    res=cursor.fetchall()
    print(res)
    return (res)

def getLabRequestDetails(email, reqid):
    query="SELECT  a.patientID, a.doctorID , a.labRequestDocumentID FROM ELabRequestDocument a WHERE a.labRequestDocumentID='"+reqid+"';"
    cursor.execute(query)
    res=cursor.fetchall()
    print(res)
    return (res)

def getLabPrescriptionDetails(reqid):
    return True

def getLabId(email) :
    query = "SELECT labID FROM LabDetails WHERE email ='"+email+"';"
    cursor.execute(query)
    res = cursor.fetchall()
    print(res)
    return (res)

def putLabReponse(labRequestID,resultLink, description):
    #responseTime = datetime.datetime.strptime(str(datetime.datetime.now()), "%Y-%m-%d %H:%M:%S")
    format = "%Y-%m-%d"
    now = datetime.datetime.utcnow().strftime(format)
    responseTime =now
    print(responseTime)
    print(labRequestID)
    print(resultLink)
    #query = "INSERT INTO LabResponse ('labRequestID','resultLink', 'description','dateTimeStamp') VALUES  ('"+ labRequestID+"','"+(resultLink)+"','"+description+"','"+ responseTime+"';"
    #query = "INSERT INTO LabResponse ('labRequestID', 'description','dateTimeStamp') VALUES  (%s,%s,%s)"
    #query = "INSERT INTO Files Values ('"+resultLink+"');"
    query = "INSERT INTO LabResponse (labRequestID, description , dateTimeStamp, resultLink) VALUES ('{0}','{1}','{2}','{3}')".format(labRequestID,description,responseTime,resultLink)
    print("----------------------query:---------------\n",query)
    # res=cursor.execute("INSERT INTO LabResponse ('labRequestID', 'description') VALUES  (%s,%s)",(labRequestID,description))
    res=cursor.execute(query)
    conn.commit()
    #res=1
    if (res==1):
        print("Successful entry")
    return True
# END : DEEPIKA'S FUNCTIONS

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
        takeMedicineRes[i] = [str(result[0]),str(result[1]),str(result[2]),str(result[3]),str(result[4])]

    res["TakeMedicine"] = takeMedicineRes
    
    # Order Medicine updates:
    query = "SELECT ePrescriptionID,reminderDate,reminderTime FROM MedicineReminder WHERE patientID='{0}'".format(patientID)
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    conn.close()
    orderMedicineRes = {}

    for i,result in enumerate(data):
        orderMedicineRes[i] = [str(result[0]),str(result[1]),str(result[2])]

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
        labVisitRes[i] = [str(result[0]),str(result[1]),str(result[2]),str(result[3])]

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
        docVisitRes[i] = [str(result[0]),str(result[1]),str(result[2])]

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
            doctorApptRes[i] = [str(result[0]),str(result[1]),str(result[2])]

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

def patientLabRequest(ID,payload,method): #ID is labID if POST, patientID if GET
    if(method=="GET"):
        query = "SELECT doctorID,ePrescriptionID,testType,description FROM ELabRequestDocument WHERE patientID='{0}' AND labRequestDocumentID IN (\
                 SELECT labRequestDocumentID FROM LabRequest WHERE isPending=1\
                )".format(ID)

        conn = mysql.connect()
        cursor =mysql.get_db().cursor()
        queryResults = cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        conn.close()
        
        labReqRes = {}

        for i,result in enumerate(data):
            labReqRes[i] = [result[0],result[1],result[2],result[3]]

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




def patientMedicineRequest(ID,payload,method):
    if(method=="GET"):

        queryGetAllPrescriptions = "SELECT * FROM MedicineRequest WHERE patientID={0}".format(ID);
        
        # queryPrescriptionDetails = "SELECT MedicineDetails.symptoms,MedicineDetails.medicineSuggestion,MedicineDetails.timeToTake,MedicineDetails.startDate,MedicineDetails.endDate\
        #                             FROM MedicineRequest,MedicineDetails \
        #                             WHERE MedicineDetails.ePrescriptionID <=> MedicineRequest.ePrescriptionID \
        #                             AND MedicineRequest.patientID<=>'{0}'".format(ID);
        queryPrescriptionDetails = "SELECT * FROM MedicineDetails \
                                    WHERE ePrescriptionID IN (SELECT ePrescriptionID FROM MedicineRequest WHERE \
                                    patientID = {0} \
                                    )".format(ID)
        conn = mysql.connect()
        cursor =mysql.get_db().cursor()
        queryGetAllPrescriptionsRes = cursor.execute(queryGetAllPrescriptions)
        data1 = cursor.fetchall()
        queryPrescriptionDetailsRes = cursor.execute(queryPrescriptionDetails)
        data2 = cursor.fetchall()
        cursor.close()

        conn.close()
        res = {}
        # for i,result in enumerate(data1):

        return res

    elif(method=="POST"):
        # get date from form
        # return json of available times.

        query = "INSERT INTO MedicineRequest VALUES ('{0}','{1}','{2}','{3}')".format(\
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
    # print("------------------data------------------\n",data)
    for i,result in enumerate(data):
        # print(i,result)
        res[i] = str(result[0]) # str to convert datetime.timedelta to a time representation

    cursor.close()
    conn.close()

    return res

def patientFetchPrescriptions(patientID):
    query = "SELECT * FROM MedicineDetails WHERE ePrescriptionID IN (\
             SELECT ePrescriptionID FROM EPrescription WHERE patientID = {0}\
            )".format(patientID)

    conn = mysql.connect()

    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    res = {}
    
    for i,result in enumerate(data):
        res[i] = [str(result[0]),str(result[1]),str(result[2]),str(result[3]),str(result[4])]

    cursor.close()
    conn.close()

    return res

def patientLabResponse(patientID): 
    query = "SELECT doctorID,ePrescriptionID,testType,description FROM ELabRequestDocument WHERE patientID='{0}' AND labRequestDocumentID IN (\
             SELECT labRequestDocumentID FROM LabResponse\
            )".format(patientID)

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    conn.close()
    
    labReqRes = {}

    for i,result in enumerate(data):
        labReqRes[i] = [result[0],result[1],result[2],result[3]]

    return labReqRes

def patientMedicineResponse(ID):
    # query = ""
    # conn = mysql.connect()
    # cursor =mysql.get_db().cursor()
    # res = cursor.execute(query)
    # data = cursor.fetchall()
    # cursor.close()

    # conn.close()
    res = {}
    # for i,result in enumerate(data1):

    return res

def getDetailsByID(ID,acctType):
    query = "SELECT * FROM {0}Details WHERE {0}ID='{1}'".format(acctType,ID);

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    conn.close()
    
    res = {}

    if(acctType=="Doctor"):
        for i,result in enumerate(data):
            res[i] = [str(result[0]),str(result[1]),str(result[2]),str(result[3]),str(result[4]),str(result[5]),str(result[6]),str(result[7])]
    else:
        for i,result in enumerate(data):
            res[i] = [str(result[0]),str(result[1]),str(result[2]),str(result[3]),str(result[4])]

    return res

def getMedicineDetailsByEPrescriptionID(ID):
    query = "SELECT symptoms,medicineSuggestion\
            FROM MedicineDetails \
            WHERE ePrescriptionID='{0}'".format(ID)

    print("---------query-----------",query)
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    res = {}

    for i,result in enumerate(data):
        res[i] = [str(result[0]),str(result[1])]
    print("---------res-----------",res)
    return res
