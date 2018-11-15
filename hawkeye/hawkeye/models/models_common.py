from hawkeye import mysql
import json
import datetime
import time  
import numpy as np
import matplotlib.pyplot as plt  


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

      


