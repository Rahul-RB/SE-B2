from hawkeye import mysql
import json
import datetime
import time  
import numpy as np
import matplotlib.pyplot as plt  

# Check if user's password matches what is in the database.
# Depending on the email, password and acctType, check the 
# appropriate table and send a bool back.
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
            return False    # Invalid password entered by user, considering the 
                            # email exists in the DB for that acctType.
        else:
            return True
    except Exception as e:
        return False        # If there's no such email in DB for that acctType.

def isExistingUser(ID,acctType):
    query = "SELECT * \
             FROM {0}Details \
             WHERE {1}ID={2}".format(acctType,acctType.lower(),ID)
    
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
        insertDetailQuery = "INSERT INTO PatientDetails \
                    VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(\
                    inpDict["patientID"],
                    inpDict["name"],
                    inpDict["email"],
                    inpDict["dob"],
                    inpDict["address"],
                    inpDict["sex"],
                    inpDict["phoneNO"]
                )

    elif(acctType=="Doctor"):
        insertDetailQuery = "INSERT INTO DoctorDetails \
                    VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(\
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
        insertDetailQuery = "INSERT INTO LabDetails \
                VALUES ('{0}','{1}','{2}','{3}','{4}')".format(\
                inpDict["labID"],
                inpDict["labName"],
                inpDict["address"],
                inpDict["email"],
                inpDict["phoneNO"]
            )
        
    elif(acctType=="Pharmacy"):
        insertDetailQuery = "INSERT INTO PharmacyDetails \
                VALUES ('{0}','{1}','{2}','{3}','{4}')".format(\
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

# Used for commonSearcg functionality.
# So get the entered name, then search the *Details table (* can be Doctor, 
# Pharmacy or Lab) to see if it has a name "like" (MySQL "like" is "ilike" in 
# PSQL) in the table.
def getDetailsByName(inpText,resType):
    query = "SELECT {0}Name,{0}ID \
             FROM {1}Details \
             WHERE {0}Name LIKE '{2}%'".format(resType.lower(),resType,inpText)
    conn = mysql.connect()

    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    res = {}
    if(queryResults!=0):
        for i,result in enumerate(data):
            res[i] = [result[0],result[1]]  # Return the Name and ID. ID will be
                                            # used to send booking later.
        print("res:",res)
        return res
    else:
        return {"data":None}

def getUsernameByEmail(email,acctType):
    # query = "SELECT "+ acctType.lower() + "Name from "+ acctType +"Details where email='"+email+"'"
    query = "SELECT {0}Name \
             FROM {1}Details \
             WHERE email='{2}'".format(acctType.lower(),acctType,email)
    print(query)
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    res = cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    conn.close()
    return data[0][0]

def getIDByEmail(email,acctType):
    # query = "SELECT "+ acctType.lower() + "ID from "+ acctType +"Details where email='"+email+"'"
    
    query = "SELECT {0}ID \
             FROM {1}Details \
             WHERE email='{2}'".format(acctType.lower(),acctType,email)

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
    elif(acctType=="Patient"):
        for i,result in enumerate(data):
            res[i] = [str(result[0]),str(result[1]),str(result[2]),str(result[3]),str(result[4]),str(result[5])]
    else:
        for i,result in enumerate(data):
            res[i] = [str(result[0]),str(result[1]),str(result[2]),str(result[3]),str(result[4])]

    return res


      


