from hawkeye import mysql
import json
import datetime

conn = mysql.connect()
cursor =conn.cursor()

def loginCheck(email,password,acctType):

    if(acctType=="Patient"):
        query = "SELECT password from PatientLogin where email='"+email+"'"

    elif(acctType=="Doctor"):
        query = "SELECT password from DoctorLogin where email='"+email+"'"
        
    elif(acctType=="Lab"):
        query = "SELECT password from LabLogin where email='"+email+"'"
        
    elif(acctType=="Pharmacy"):
        query = "SELECT password from PharmacyLogin where email='"+email+"'"
        
    else :
        return ("Error")

    cursor.execute(query)
    data = cursor.fetchall()
    try:
        if(password!=data[0][0]):
            return False
        else:
            return True
    except Exception as e:
        return False

# def myconverter(o):
#     if isinstance(o, datetime.datetime):
#         return o.__str__()

# def checkForAppointments(email):
#     conn = mysql.connect()
#     print(mysql)
#     #conn = mysql.connection
#     query= "SELECT patientID, dateTimeStamp from doctorAppointments where doctorID='"+'12'+"'"
#     cursor =conn.cursor()
#     cursor.execute(query)
#     data = cursor.fetchall()
#     somedict = {"patientID" : [x[0] for x in data],
#                 "dateTimeStamp" : [x[1] for x in data]}
#     print("somedict is ",somedict)
#     print(type(somedict))
#     somedict1 = json.dumps(somedict,default=myconverter)
#     #print("somedict1 is ",somedict1)

#     return somedict1

