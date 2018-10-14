from hawkeye import mysql

conn = mysql.connect()
cursor =conn.cursor()


def loginCheck(email,password,acctType):
    query = "SELECT password from "+ acctType+"Login where email='"+email+"'"   

    cursor.execute(query)
    # conn.commit()
    data = cursor.fetchall()
    try:
        if(password!=data[0][0]):
            return False
        else:
            return True
    except Exception as e:
        return False

def isExistingUser(ID,acctType):
    query = "SELECT * from "+ acctType+"Details where patientID='"+ID+"'"

    res = cursor.execute(query)
    # conn.commit()

    if(res==0):
        return False
    else:
        return True

def insertNewUser(inpDict,acctType):
    if(acctType=="Patient"):
        insertDetailQuery = "INSERT INTO PatientDetails VALUES ( '" +\
                inpDict["patientID"] + "','" +\
                inpDict["name"] + "','" +\
                inpDict["email"] + "','" +\
                inpDict["dob"] + "','" +\
                inpDict["address"] + "','" +\
                inpDict["sex"] + "','" +\
                inpDict["phoneNO"] + "'" +\
            ")"
        insertLoginDetailQuery = "INSERT INTO PatientLogin VALUES('"+\
                inpDict["email"] + "','" +\
                inpDict["password"] + "'" +\
            ")"     

    elif(acctType=="Doctor"):
        insertDetailQuery = "INSERT INTO DoctorDetails VALUES ('" +\
                inpDict["doctorID"] + "','" +\
                inpDict["doctorName"] + "','" +\
                inpDict["email"] + "','" +\
                inpDict["dob"] + "','" +\
                inpDict["address"] + "','" +\
                inpDict["sex"] + "','" +\
                inpDict["phoneNO"] + "','" +\
                inpDict["designation"] + "'" +\
            ")"
        insertLoginDetailQuery = "INSERT INTO DoctorLogin VALUES ('"+\
                inpDict["email"] + "','" +\
                inpDict["password"] + "'" +\
            ")"    
        
    elif(acctType=="Lab"):
        insertDetailQuery = "INSERT INTO LabDetails VALUES ('" +\
                inpDict["labID"] + "','" +\
                inpDict["labName"] + "','" +\
                inpDict["address"] + "','" +\
                inpDict["email"] + "','" +\
                inpDict["phoneNO"] + "'" +\
            ")"
        insertLoginDetailQuery = "INSERT INTO LabLogin VALUES ('" +\
                inpDict["email"] + "','" +\
                inpDict["password"] + "'" +\
            ")" 
        
    elif(acctType=="Pharmacy"):
        insertDetailQuery = "INSERT INTO PharmacyDetails VALUES ('" +\
                inpDict["pharmacyID"] + "','" +\
                inpDict["pharmacyName"] + "','" +\
                inpDict["address"] + "','" +\
                inpDict["email"] + "','"+\
                inpDict["phoneNO"] + "'" +\
            ")"
        insertLoginDetailQuery = "INSERT INTO PharmacyLogin VALUES ('" +\
                inpDict["email"] + "','" +\
                inpDict["password"] + "'" +\
            ")" 
    else:
        return("Error")

    print(insertDetailQuery)
    print(insertLoginDetailQuery)
    res1 = cursor.execute(insertDetailQuery)
    res2 = cursor.execute(insertLoginDetailQuery)
    conn.commit()

    if(res1==1 and res2==1):
        return True
    else:
        return False


def getUsername(email,acctType):
    query = "SELECT "+ acctType.lower() + "Name from "+ acctType+"Details where email='"+email+"'"
    if(acctType=="Patient"):
        query = "SELECT name from "+ acctType+"Details where email='"+email+"'"

    res = cursor.execute(query)

    data = cursor.fetchall()
    return data[0][0]