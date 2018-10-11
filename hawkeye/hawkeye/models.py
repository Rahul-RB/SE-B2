from hawkeye import mysql

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