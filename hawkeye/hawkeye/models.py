from hawkeye import mysql
import json
import datetime

conn = mysql.connect()
cursor =conn.cursor()


def loginCheck(email,password,acctType): 
    query = "SELECT password FROM {0}Login WHERE email='{1}'".format(acctType,email)   

    cursor.execute(query)
    conn.commit()
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
    conn.commit()

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

