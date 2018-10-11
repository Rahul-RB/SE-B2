from hawkeye import mysql

conn = mysql.connect()
cursor =conn.cursor()

def loginCheck(email,password):
	query = "SELECT password from PatientLogin where email='"+email+"'"
	print(query)
	cursor.execute(query)
	data = cursor.fetchall()
	print("data:",data)
	if(password!=data[0][0]):
		return False
	else:
		return True