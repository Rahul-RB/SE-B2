from hawkeye import mysql
import json
import datetime
import time  
import numpy as np
import matplotlib.pyplot as plt  

# utility converter for converting datetime object to string
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


# for updating calendar for appointment for the first time
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


# check for pending appointments for a particular doctor
def checkForAppointments(email):
    
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


# utility function for searching the patient history given the patientID
def searchPatientHistory(patientID):
    conn = mysql.connect()
    conn.autocommit = False
    cursor =conn.cursor()
    global_dict=dict(dict())

    query = "SELECT ePrescriptionID, doctorID from EPrescription where patientID='" + patientID + "'"
    cursor.execute(query)
    data = cursor.fetchall()

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

# utility function for checking the number of patients visited to a particular year in that particular day, month and year
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


# computes the number of patients monthwise
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

    
# used for inserting a new ePrescription into the database

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


