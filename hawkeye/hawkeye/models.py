from hawkeye import mysql
import json
import datetime

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
    conn = mysql.connect()
    print(mysql)
    #conn = mysql.connection
    query= "SELECT patientID, dateTimeStamp from doctorAppointments where doctorID='"+'12'+"'"
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
    if(acctType=="Patient"):
        query = "SELECT * from PatientDetails where patientID='"+ID+"'"
    elif(acctType=="Doctor"):
        query = "SELECT * from DoctorDetails where doctorID='"+ID+"'"
        
    elif(acctType=="Lab"):
        query = "SELECT * from LabDetails where labID='"+ID+"'"
        
    elif(acctType=="Pharmacy"):
        query = "SELECT * from PharmacyDetails where pharmacyID='"+ID+"'"
    else:
        return("Error")
    res = cursor.execute(query)
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

def getLabRequests(email):
	query="SELECT  a.patientID, a.doctorID , a.labRequestDocumentID FROM ELabRequestDocument a ,LabRequest lr, LabLogin lo, LabDetails ld where lo.email= '"+email+"' and ld.email = lo.email and ld.labid= lr.labid and lr.labRequestDocumentID=a.labRequestDocumentID ;"
        cursor.execute(query)
        res=cursor.fetchall()
        print(res)
        return (res)

