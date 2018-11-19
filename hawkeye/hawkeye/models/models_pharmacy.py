from hawkeye import mysql
import json
import datetime
import time  
import numpy as np
import matplotlib.pyplot as plt  
# #start pharmacyViewRequest
# def getUsernameByEmail(email,acctType):
#     query = "SELECT "+ acctType.lower() + "Name from "+ acctType +"Details where email='"+email+"'"
#     print(query)
#     conn = mysql.connect()
#     cursor = mysql.get_db().cursor()
#     res = cursor.execute(query)

#     data = cursor.fetchall()
#     return data[0][0]

# def getIDByEmail(email,acctType):
#     query = "SELECT "+ acctType.lower() + "ID from "+ acctType +"Details where email='"+email+"'"
#     conn = mysql.connect()
#     cursor = mysql.get_db().cursor()
#     res = cursor.execute(query)

#     data = cursor.fetchall()
#     return data[0][0]

#     symptoms,medicineSuggestion,timeToTake,startDate,endDate,


def prescriptionRequest(pharmacyId):
    query = "SELECT mr.ePrescriptionID, mr.patientID, md.medicineSuggestion FROM MedicineRequest mr LEFT JOIN MedicineDetails md ON mr.ePrescriptionID = md.ePrescriptionID WHERE mr.ispending=1 and mr.pharmacyID='{0}'".format(pharmacyId)
    conn = mysql.connect()
    cursor = mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    res = {}
    for i,result in enumerate(data):
        if(str(result[0])+" "+str(result[1]) not in res):
            res[str(result[0])+" "+str(result[1])] = [str(result[2])]
        else:
            res[str(result[0])+" "+str(result[1])].append(str(result[2]))
    return res

def prescriptionResponseUpdate(payload,pharmacyID):
    query = "INSERT INTO MedicineResponse(ePrescriptionID, patientID, remarks) VALUES('{0}','{1}','{2}')".format(payload["prescriptionID"],payload["patientID"],payload["response"])
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    mysql.get_db().commit()
    cursor.close()
    conn.close()
	
    if queryResults==0:
        return {"Failed":True}
    query = "UPDATE MedicineRequest SET isPending=0 WHERE ePrescriptionID='{0}' AND patientID='{1}'".format(payload["prescriptionID"],payload["patientID"])	
    conn = mysql.connect()

    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    mysql.get_db().commit()
    cursor.close()
    conn.close()

#end pharmacyViewRequest
# START : Pharmacy FUNCTIONS
# Get the required details for the pharmacy
def getpharmacytitle(email):
    query="SELECT p.pharmacyName, p.address, p.phoneNO from PharmacyDetails p, PharmacyLogin  WHERE PharmacyLogin.email='"+email+"';"
    print(query)
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    res = cursor.execute(query)
    data = cursor.fetchall()
    #print("Hi in sql ###############",data)
    cursor.close()
    conn.close()
    return (data)


	
# Fetch the EPrescription for particular patient
def getpharmacyPres(email,patientID):
    query="SELECT p.slNo, p.medicineSuggestion, p.remarks from EPrescription p where p.patientID='"+patientID+"';"
    print(query)
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    res = cursor.execute(query)
    data = cursor.fetchall()
    #print("Hi in sql ###############",data)
    cursor.close()
    conn.close()
    return (data)

	
	
# fetch other details from EPrescription
def getEprescritionDetails(email,patientID):
    query="SELECT p.patientID, p.ePrescriptionID, p.doctorID from EPrescription p WHERE p.patientID='"+patientID+"'; "
    print(query)
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    res = cursor.execute(query)
    data = cursor.fetchall()
    #print("Hi in sql ###############",data)
    cursor.close()
    conn.close()
    return (data)
