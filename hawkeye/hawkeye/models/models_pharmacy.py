def graph(email):
	query=" select m.MedicineSuggestion,COUNT(m.MedicineSuggestion) from MedicineDetails m, MedicineRequest mr, Eprescription e, PharmacyDetails pd, PatientDetails p where pd.email='"+email+"'  and mr.ePrescriptionID=e.ePrescriptionID and e.ePrescriptionID=m.ePrescriptionID and mr.patientID=p.patientID and pd.pharmacyID=mr.pharmacyID GROUP BY m.MedicineSuggestion ORDER BY COUNT(m.MedicineSuggestion) DESC LIMIT 4;"
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
	query="select DATE(mr.pickupTime) , COUNT(DATE(mr.pickupTime)) from MedicineRequest mr, PharmacyDetails pd where isPending=1 and pd.pharmacyID=mr.pharmacyID and pd.email='"+email+"' group by DATE(pickupTime) order by DATE(pickupTime) ;"
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
	if(res):
		data=[]
		for tuple in res:
			data.append([str(tuple[0]),tuple[1]])
	#print(data)
	return data