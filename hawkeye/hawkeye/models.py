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
    print("data is ",data)
    if(data != ''):
        somedict = {"patientID" : [x[0] for x in data],
                    "start_datetime" : [datetime.datetime.combine(x[1],(datetime.datetime.min + x[2]).time()) for x in data],
                    "end_datetime" : [datetime.datetime.combine(x[1],(datetime.datetime.min + x[2]+datetime.timedelta(minutes=30)).time()) for x in data]
                        }
        print("somedict is ",somedict)
        print(type(somedict))
        somedict1 = json.dumps(somedict,default=myconverter)
        print("somedict1 is ",somedict1)
        if len(somedict) > 0: # ensure that the dictionary is not empty
            # print("\nInside if top\n")
            query1= "UPDATE DoctorAppointments SET  addedToDoctorCalendar=1 where addedToDoctorCalendar=0 and doctorID in (SELECT doctorID from DoctorDetails where email='" + email + "')"
            cursor1 =conn.cursor()
            cursor1.execute(query1)
            print("\nInside if\n")
        conn.commit()
        # print("Hello Hii I am inside try block\n")
        return somedict1
    else:
        somedict1 = dict()
        return somedict1

# def insertIntoPrescription():
    

def isExistingUser(ID,acctType):
    query = "SELECT * from "+ acctType+"Details where patientID='"+ID+"'"

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

