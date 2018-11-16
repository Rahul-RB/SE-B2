from hawkeye import mysql
import json
import datetime
import time  
import numpy as np
import matplotlib.pyplot as plt  



# START : DEEPIKA'S FUNCTIONS
def getLabRequests(email):
    query="SELECT  a.patientID, a.doctorID , a.labRequestDocumentID FROM ELabRequestDocument a ,LabRequest lr, LabLogin lo, LabDetails ld where lo.email= '"+email+"' and ld.email = lo.email and ld.labid= lr.labid and lr.labRequestDocumentID=a.labRequestDocumentID and lr.isPending=1;"
    
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    
    cursor.execute(query)
    res=cursor.fetchall()

    cursor.close()
    conn.close()

    print(res)
    return (res)

def getLabResponses(email):
    query="SELECT  a.patientID, a.doctorID , a.labRequestDocumentID FROM ELabRequestDocument a ,LabRequest lr, LabLogin lo, LabDetails ld where lo.email= '"+email+"' and ld.email = lo.email and ld.labid= lr.labid and lr.labRequestDocumentID=a.labRequestDocumentID and lr.isPending=0;"

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()

    cursor.execute(query)
    res=cursor.fetchall()

    cursor.close()
    conn.close()

    print(res)
    return (res)

def getLabRequestDetails(email, reqid):
    query="SELECT  a.patientID, a.doctorID , a.labRequestDocumentID, a.testType, a.description FROM ELabRequestDocument a, LabRequest lr WHERE a.labRequestDocumentID='"+reqid+"' and a.labRequestDocumentID= lr.labRequestDocumentID ;"

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()

    cursor.execute(query)
    res=cursor.fetchall()

    cursor.close()
    conn.close()

    print(res)
    return (res)


def getLabPrescriptionDetails(reqid):
    query="SELECT  md.ePrescriptionID, md.symptoms, md.medicineSuggestion, md.timeToTake, md.startDate, md.endDate from MedicineDetails md, ELabRequestDocument elrd where elrd.labRequestDocumentID = "+reqid+ " and elrd. ePrescriptionID = md.ePrescriptionID;"
    
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()

    cursor.execute(query)
    res=cursor.fetchall()

    cursor.close()
    conn.close()
    
    print(res)
    return res

def getLabId(email) :
    query = "SELECT labID FROM LabDetails WHERE email ='"+email+"';"

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()

    cursor.execute(query)
    res = cursor.fetchall()

    cursor.close()
    conn.close()

    print(res)
    return (res)

def putLabReponse(labRequestID,resultLink, description):
    #responseTime = datetime.datetime.strptime(str(datetime.datetime.now()), "%Y-%m-%d %H:%M:%S")
    format = "%Y-%m-%d"
    now = datetime.datetime.utcnow().strftime(format)
    responseTime =now
    print(responseTime)
    print(labRequestID)
    print(resultLink)
    #query = "INSERT INTO LabResponse ('labRequestID','resultLink', 'description','dateTimeStamp') VALUES  ('"+ labRequestID+"','"+(resultLink)+"','"+description+"','"+ responseTime+"';"
    #query = "INSERT INTO LabResponse ('labRequestID', 'description','dateTimeStamp') VALUES  (%s,%s,%s)"
    #query = "INSERT INTO Files Values ('"+resultLink+"');"
    query = "INSERT INTO LabResponse (labRequestID, description , dateTimeStamp, resultLink) VALUES ('{0}','{1}','{2}','{3}')".format(labRequestID,description,responseTime,resultLink)
    print("----------------------query:---------------\n",query)
    # res=cursor.execute("INSERT INTO LabResponse ('labRequestID', 'description') VALUES  (%s,%s)",(labRequestID,description))

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()

    res=cursor.execute(query)
    conn.commit()

    query = "UPDATE LabRequest SET isPending=0 WHERE labRequestDocumentID="+labRequestID+";"
    res2=cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()
    #res=1
    if ((res1) and(res2)):
        print("Successful entry")
    return True

def getLabReportFilename(reqid):
    query= "SELECT resultLink FROM LabResponse WHERE labRequestID = "+reqid+";"
    
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()

    cursor.execute(query)
    res=cursor.fetchall()

    cursor.close()
    conn.close()
    
    print(res[0][0])
    return res[0][0]



# END : DEEPIKA'S FUNCTIONS
