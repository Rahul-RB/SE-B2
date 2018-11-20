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
    query= "SELECT pharmacyName,address,phoneNO \
            FROM PharmacyDetails \
            WHERE email in (SELECT email FROM PharmacyLogin WHERE email='{0}')".format(email)
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
def graph(email):
    query=" select m.MedicineSuggestion,COUNT(m.MedicineSuggestion) from MedicineDetails m, MedicineRequest mr, EPrescription e, PharmacyDetails pd, PatientDetails p where pd.email='"+email+"'  and mr.ePrescriptionID=e.ePrescriptionID and e.ePrescriptionID=m.ePrescriptionID and mr.patientID=p.patientID and pd.pharmacyID=mr.pharmacyID GROUP BY m.MedicineSuggestion ORDER BY COUNT(m.MedicineSuggestion) DESC LIMIT 4;"
    print(query)
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    #print("Hiiii",(jsonify(data)))
    print(res)
    #print("==\n",res2)
    data1=[]
    sum=0;
    med=dict();
    if (res):
        for tuple in res:
            items= tuple[0].split(', ')
            for item in items:
                if item in med.keys():
                    med[item]+=tuple[1]
                else:
                    med.update({item:tuple[1]})
    print(med)
    medarray=[]
    for k, v in med.items():
        medarray.append([k,v])
        print(k,v)
    print(medarray)
            #    data1.append([tuple[0],tuple[1]])
            #sum+=tuple[1]
        #data1.append(["Other",res1[0][0]-sum])
        #print(data1)
    return (medarray);
def getNumberOfRequests(email):
    query="SELECT DATE(mr.pickupTime) , COUNT(DATE(mr.pickupTime))\
           FROM MedicineRequest mr, PharmacyDetails pd \
           WHERE isPending=1 AND pd.pharmacyID=mr.pharmacyID AND pd.email='{0}'\
           GROUP BY DATE(pickupTime) ORDER BY DATE(pickupTime)".format(email)
           
    # query="select DATE(dateTimeStamp) , COUNT(DATE(dateTimeStamp)) from LabRequest\
    #        where isPending=1 and labID='"+labid+"' group by DATE(dateTimeStamp) order by DATE(dateTimeStamp) ;"
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    cursor.execute(query)
    res=cursor.fetchall()
    print("YO-----------",res)
    cursor.close()
    conn.close()
    format = "%Y-%m-%d"
    data = []
    if(res):
        data=[]
        for tuple in res:
            data.append([str(tuple[0]),tuple[1]])
    #print(data)
    return data