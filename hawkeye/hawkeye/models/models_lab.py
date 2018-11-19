from hawkeye import mysql
import json
import datetime
import time  
import numpy as np
import matplotlib.pyplot as plt  



# START : DEEPIKA'S FUNCTIONS
def getLabRequests(email):
    query="SELECT  a.patientID, a.doctorID , a.labRequestDocumentID FROM \
        ELabRequestDocument a ,LabRequest lr, LabLogin lo, LabDetails ld \
        where lo.email= '"+email+"' and ld.email = lo.email \
        and ld.labid= lr.labid and lr.labRequestDocumentID=a.labRequestDocumentID and lr.isPending=1;"
    
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    
    cursor.execute(query)
    res=cursor.fetchall()

    cursor.close()
    conn.close()

    print(res)
    return (res)

def getLabResponses(email):
    query="SELECT  a.patientID, a.doctorID , a.labRequestDocumentID \
           FROM ELabRequestDocument a ,LabRequest lr, LabLogin lo, LabDetails ld \
           where lo.email= '"+email+"' and ld.email = lo.email and ld.labid= lr.labid \
           and lr.labRequestDocumentID=a.labRequestDocumentID and lr.isPending=0;"

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()

    cursor.execute(query)
    res=cursor.fetchall()

    cursor.close()
    conn.close()

    print(res)
    return (res)

def getLabRequestDetails(email, reqid):
    query="SELECT  a.patientID, a.doctorID , a.labRequestDocumentID, a.testType, \
           a.description FROM ELabRequestDocument a, LabRequest lr WHERE \
           a.labRequestDocumentID='"+reqid+"' and a.labRequestDocumentID= lr.labRequestDocumentID ;"

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()

    cursor.execute(query)
    res=cursor.fetchall()

    cursor.close()
    conn.close()

    print(res)
    return (res)


def getLabPrescriptionDetails(reqid):
    query="SELECT  md.ePrescriptionID, md.symptoms, md.medicineSuggestion,\
           md.timeToTake, md.startDate, md.endDate from MedicineDetails md, \
           ELabRequestDocument elrd where elrd.labRequestDocumentID = "+reqid+ " \
           and elrd. ePrescriptionID = md.ePrescriptionID;"
    
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
    format = "%Y-%m-%d"
    now = datetime.datetime.utcnow().strftime(format)
    responseTime =now
    query1 = "INSERT INTO LabResponse (labRequestID, description , dateTimeStamp, resultLink) \
              VALUES ('{0}','{1}','{2}','{3}')".format(labRequestID,description,responseTime,resultLink)
    #print(query1)
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    res1=cursor.execute(query1)
    mysql.get_db().commit()
    cursor.close()
    conn.close()

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()
    query2 = "UPDATE LabRequest SET isPending=0 WHERE labRequestDocumentID="+labRequestID+";"
    res2=cursor.execute(query2)
    mysql.get_db().commit()
    cursor.close()
    conn.close()

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

#Function to get at max the top 4 types of LabTests
def getTop4Request(labid):
    # query1= "SELECT testType, COUNT(testType) FROM ELabRequestDocument GROUP BY testType \
    #         ORDER BY COUNT(testType) DESC LIMIT 4;"
    query1= "SELECT rd.testType, COUNT(rd.testType) FROM ELabRequestDocument rd, LabRequest lr \
            WHERE rd.labRequestDocumentID= lr.labRequestDocumentID and \
            lr.labID= '"+labid+"' GROUP BY rd.testType \
            ORDER BY COUNT(rd.testType) DESC LIMIT 4;"
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()

    cursor.execute(query1)
    res1=cursor.fetchall()

    cursor.close()
    conn.close()

    # query2= "SELECT COUNT(*) FROM ELabRequestDocument;"
    query2= "SELECT COUNT(*) FROM ELabRequestDocument rd , LabRequest lr \
             WHERE rd.labRequestDocumentID= lr.labRequestDocumentID and \
             lr.labID= '"+labid+"';"
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()

    cursor.execute(query2)
    res2=cursor.fetchall()

    cursor.close()
    conn.close()

    print(res1)
    print("==\n",res2)
    data=[]
    sum=0;
    if (res1) and (res2):
        for tuple in res1:
            data.append([str(tuple[0]),tuple[1]])
            sum+=tuple[1]
        data.append(["Other",res2[0][0]-sum])
        print(data)
    return (data);

def getNumberOfResponses(labid):
    # query="select DATE(dateTimeStamp) , COUNT(DATE(dateTimeStamp)) from LabRequest\
    #        where isPending=0 group by DATE(dateTimeStamp) order by DATE(dateTimeStamp) ;"
    query="select DATE(dateTimeStamp) , COUNT(DATE(dateTimeStamp)) from LabRequest\
           where isPending=0 and labID='"+labid+"' group by DATE(dateTimeStamp) \
           order by DATE(dateTimeStamp) ;"

    conn = mysql.connect()
    cursor =mysql.get_db().cursor()

    cursor.execute(query)
    res=cursor.fetchall()
    cursor.close()
    conn.close()
    format = "%Y-%m-%d"
    data=[]
    if(res):
        for tuple in res:
            data.append([str(tuple[0]),tuple[1]])
    print(data)

    return data

def getNumberOfRequests(labid):
    # query="select DATE(dateTimeStamp) , COUNT(DATE(dateTimeStamp)) from LabRequest \
    #        group by DATE(dateTimeStamp) order by DATE(dateTimeStamp) ;"
    query="select DATE(dateTimeStamp) , COUNT(DATE(dateTimeStamp)) from LabRequest\
           where labID='"+labid+"' group by DATE(dateTimeStamp) \
           order by DATE(dateTimeStamp) ;"
    conn = mysql.connect()
    cursor =mysql.get_db().cursor()

    cursor.execute(query)
    res=cursor.fetchall()
    cursor.close()
    conn.close()
    format = "%Y-%m-%d"
    data=[]
    if(res):
        for tuple in res:
            data.append([str(tuple[0]),tuple[1]])
    return data




# END : DEEPIKA'S FUNCTIONS
