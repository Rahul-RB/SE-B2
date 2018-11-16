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
def getEprescitionDetails(email,patientID):
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