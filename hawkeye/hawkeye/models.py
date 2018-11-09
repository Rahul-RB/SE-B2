from hawkeye import mysql
import json
import datetime
#import mysql.connector

conn = mysql.connect()
cursor =conn.cursor()


def loginCheck(email,password,acctType):
    query = "SELECT password from "+ acctType+"Login where email='"+email+"'"   

    cursor.execute(query)
    conn.commit()
    data = cursor.fetchall()
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
            json_data["ePrescriptionID"] = somedict["ePrescriptionID"]
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
    

def isExistingUser(ID,acctType):
    # query = "SELECT * from "+ acctType+"Details where patientID='"+ID+"'"
    query = "SELECT * FROM {0}Details WHERE {1}ID={2}".format(acctType,acctType.lower(),ID)

    res = cursor.execute(query)
    conn.commit()

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
    ePrescriptionRandom = (str(now.month) + str(now.day) + str(now.hour) \
    + str(now.minute) + str(now.second))

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








        



