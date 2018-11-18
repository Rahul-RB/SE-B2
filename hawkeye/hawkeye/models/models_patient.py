from hawkeye import mysql
import json
import datetime
import time  
import numpy as np
import matplotlib.pyplot as plt  

# from hawkeye import models 


def patientMedReminderUpdate(patientID):
    res = {
        "TakeMedicine":None,
        "OrderMedicine":None
    }
    # Take Medicine updates:
    query = "SELECT symptoms,medicineSuggestion,timeToTake,startDate,endDate \
            FROM MedicineDetails \
            WHERE ePrescriptionID IN (SELECT ePrescriptionID FROM MedicineReminder WHERE patientID='{0}')".format(patientID)
    
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    takeMedicineRes = {}

    for i,result in enumerate(data):
        takeMedicineRes[i] = [str(result[0]),str(result[1]),str(result[2]),str(result[3]),str(result[4])]

    res["TakeMedicine"] = takeMedicineRes
    
    # Order Medicine updates:
    query = "SELECT ePrescriptionID,reminderDate,reminderTime FROM MedicineReminder WHERE patientID='{0}'".format(patientID)
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    conn.close()
    orderMedicineRes = {}

    for i,result in enumerate(data):
        orderMedicineRes[i] = [str(result[0]),str(result[1]),str(result[2])]

    res["OrderMedicine"] = orderMedicineRes

    return res

    # patientID,labID,labRequestDocumentID,reminderDate,reminderTime
def patientLabVisitReminderUpdate(patientID):
    query = "SELECT labID,labRequestDocumentID,reminderDate,reminderTime FROM LabVisitReminder WHERE patientID='{0}'".format(patientID)

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    conn.close()
    labVisitRes = {}

    for i,result in enumerate(data):
        labVisitRes[i] = [str(result[0]),str(result[1]),str(result[2]),str(result[3])]

    return labVisitRes

def patientDocVisitReminderUpdate(patientID):
    query = "SELECT doctorID,reminderDate,reminderTime FROM DoctorVisitReminder WHERE patientID='{0}'".format(patientID)

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    conn.close()
    docVisitRes = {}

    for i,result in enumerate(data):
        docVisitRes[i] = [str(result[0]),str(result[1]),str(result[2])]

    return docVisitRes

def patientCalendarReminderUpdate(patientID):
    medReminders = patientMedReminderUpdate(patientID)
    res = {
        "TakeMedicine":medReminders["TakeMedicine"],
        "OrderMedicine":medReminders["OrderMedicine"],
        "DocVisit":patientDocVisitReminderUpdate(patientID),
        "LabVisit":patientLabVisitReminderUpdate(patientID)
    }

    return res


def patientDoctorAppointment(patientID,payload,method):
    if(method=="GET"):
        query = "SELECT doctorID,dateStamp,pickATime FROM DoctorAppointments WHERE patientID='{0}'".format(\
                patientID
            )

        conn = mysql.connect()
        cursor =mysql.get_db().cursor()
        queryResults = cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        conn.close()
        doctorApptRes = {}

        for i,result in enumerate(data):
            doctorApptRes[i] = [str(result[0]),str(result[1]),str(result[2])]

        return doctorApptRes

    elif(method=="POST"):
        # get date from form
        # Check all times already input in for that date
        # return json of available times.
        # query = "SELECT"

        query = "INSERT INTO DoctorAppointments VALUES ('{0}','{1}','{2}','{3}','{4}')".format(\
                patientID,
                payload["doctorID"],
                payload["apptDate"],
                payload["apptTime"],
                1
            )
        conn = mysql.connect()

        cursor =mysql.get_db().cursor()
        queryResults = cursor.execute(query)
        data = cursor.fetchall()

        mysql.get_db().commit()

        cursor.close()
        conn.close()

        if queryResults==1:
            return {"Success":True}
        else:
            return {"Failed":True}



def patientLabRequest(ID,payload,method): #ID is labID if POST, patientID if GET
    if(method=="GET"):
        query = "SELECT doctorID,ePrescriptionID,testType,description FROM ELabRequestDocument WHERE patientID='{0}' AND labRequestDocumentID IN (\
                 SELECT labRequestDocumentID FROM LabRequest WHERE isPending=1\
                )".format(ID)

        conn = mysql.connect()
        cursor =mysql.get_db().cursor()
        queryResults = cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()

        conn.close()
        
        labReqRes = {}

        for i,result in enumerate(data):
            labReqRes[i] = [result[0],result[1],result[2],result[3]]

        return labReqRes

    elif(method=="POST"):
        # get date from form
        # return json of available times.

        query = "INSERT INTO LabRequest VALUES ('{0}','{1}','{2}','{3}')".format(\
                payload["labRequestDocumentID"],
                payload["labID"],
                payload["apptDate"],
                1
            )
        conn = mysql.connect()

        cursor =mysql.get_db().cursor()
        queryResults = cursor.execute(query)
        data = cursor.fetchall()

        mysql.get_db().commit()

        cursor.close()
        conn.close()

        if queryResults==1:
            return {"Success":True}
        else:
            return {"Failed":True}




def patientMedicineRequest(ID,payload,method):
    if(method=="GET"):

        queryGetAllPrescriptions = "SELECT * FROM MedicineRequest WHERE patientID={0} AND isPending=1".format(ID);
        
        # queryPrescriptionDetails = "SELECT MedicineDetails.symptoms,MedicineDetails.medicineSuggestion,MedicineDetails.timeToTake,MedicineDetails.startDate,MedicineDetails.endDate\
        #                             FROM MedicineRequest,MedicineDetails \
        #                             WHERE MedicineDetails.ePrescriptionID <=> MedicineRequest.ePrescriptionID \
        #                             AND MedicineRequest.patientID<=>'{0}'".format(ID);
        # queryPrescriptionDetails = "SELECT * FROM MedicineDetails \
        #                             WHERE ePrescriptionID IN (SELECT ePrescriptionID FROM MedicineRequest WHERE \
        #                             patientID = {0} \
        #                             )".format(ID)
        conn = mysql.connect()
        cursor =mysql.get_db().cursor()

        queryGetAllPrescriptionsRes = cursor.execute(queryGetAllPrescriptions)
        data1 = cursor.fetchall()

        # queryPrescriptionDetailsRes = cursor.execute(queryPrescriptionDetails)
        # data2 = cursor.fetchall()

        cursor.close()
        conn.close()
        res = {}

        for i,result in enumerate(data1):
            res[i] = [str(result[0]),str(result[1]),str(result[2]),str(result[3]),str(result[4])]

        print("---------------data1---------------------\n",data1)
        # print("---------------data2---------------------\n",data2)
        # for i,result in enumerate(data1):

        return res

    elif(method=="POST"):
        # get date from form
        # return json of available times.

        query = "INSERT INTO MedicineRequest VALUES ('{0}','{1}','{2}','{3}','{4}')".format(\
                payload["ePrescriptionID"],
                ID,
                payload["pharmacyID"],
                payload["pickupTime"],
                1
            )
        conn = mysql.connect()

        cursor =mysql.get_db().cursor()
        queryResults = cursor.execute(query)
        data = cursor.fetchall()

        mysql.get_db().commit()

        cursor.close()
        conn.close()

        if queryResults==1:
            return {"Success":True}
        else:
            return {"Failed":True}

def getAvailableTimeSlots(doctorID,inpDate):
    query = "SELECT pickATime FROM DoctorAppointments WHERE doctorID='{0}' AND dateStamp='{1}'".format(\
                doctorID,
                inpDate
            )

    conn = mysql.connect()

    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    res = {}
    # print("------------------data------------------\n",data)
    for i,result in enumerate(data):
        # print(i,result)
        res[i] = str(result[0]) # str to convert datetime.timedelta to a time representation

    cursor.close()
    conn.close()

    return res

def patientFetchPrescriptions(patientID):
    query = "SELECT * FROM MedicineDetails WHERE ePrescriptionID IN (\
             SELECT ePrescriptionID FROM EPrescription WHERE patientID = {0}\
            )".format(patientID)

    conn = mysql.connect()

    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    res = {}
    
    for i,result in enumerate(data):
        res[i] = [str(result[0]),str(result[1]),str(result[2]),str(result[3]),str(result[4])]

    cursor.close()
    conn.close()

    return res

def patientLabResponse(patientID): 
    # query = "SELECT doctorID,ePrescriptionID,testType,description FROM ELabRequestDocument WHERE patientID='{0}' AND labRequestDocumentID IN (\
    #          SELECT labRequestDocumentID FROM LabResponse\
    #         )".format(patientID)

    query = "SELECT * FROM LabResponse WHERE labRequestID IN \
    (SELECT labRequestDocumentID FROM ELabRequestDocument WHERE patientID='{0}')".format(patientID)
    
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    conn.close()
    
    labReqRes = {}

    for i,result in enumerate(data):
        labReqRes[i] = [str(result[0]),str(result[1]),str(result[2]),str(result[3]),str(result[4])]

    return labReqRes

def patientMedicineResponse(ID):
    query = "SELECT * FROM MedicineResponse WHERE patientID='{0}'".format(ID)
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    res = cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    # conn.close()
    res = {}
    for i,result in enumerate(data):
        res[i] = [str(result[0]),str(result[1]),str(result[2]),str(result[3])];

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

def getELabRequestDocumentByID(ID):
    query = "SELECT * FROM ELabRequestDocument \
            WHERE labRequestDocumentID='{0}'".format(ID)

    print("---------query-----------",query)
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    res = {}

    for i,result in enumerate(data):
        res[i] = [str(result[0]),str(result[1]),str(result[2]),str(result[3]),str(result[4])]
    print("---------res-----------",res)
    return res

def patientFetchLabDocs(patientID):
    query = "SELECT * FROM ELabRequestDocument WHERE patientID='{0}'".format(patientID)

    conn = mysql.connect()

    cursor =mysql.get_db().cursor()
    queryResults = cursor.execute(query)
    data = cursor.fetchall()
    res = {}
    
    for i,result in enumerate(data):
        res[i] = [str(result[0]),str(result[1]),str(result[2]),str(result[3]),str(result[4]),str(result[5])]

    cursor.close()
    conn.close()

    return res
