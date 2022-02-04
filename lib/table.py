import re,os,csv,shutil
import main,data_types

datatypes={"BOOLEAN":data_types.BOOLEAN,"SET":data_types.SET,"ENUM":data_types.ENUM, "CHAR":data_types.CHAR,"VARCHAR":data_types.VARCHAR,"TINYTEXT":data_types.TINYTEXT,"TEXT":data_types.TEXT,"BLOB":data_types.BLOB,"MEDIUMBLOB":data_types.MEDIUMBLOB,"MEDIUMTEXT":data_types.MEDIUMTEXT,"LONGTEXT":data_types.LONGTEXT,"LONGBLOB":data_types.LONGBLOB,"DATE":data_types.DATE,"TIME":data_types.TIME,"TIMESTAMP":data_types.TIMESTAMP,"DATETIME":data_types.DATETIME,"YEAR":data_types.YEAR,"INT":data_types.INT,"INTEGER":data_types.INT,"TINYINT":data_types.TINYINT,"MEDIUMINT":data_types.MEDIUMINT,"BIGINT":data_types.BIGINT}

def create(command):
	if main.current_db=="":
		print("NO DATABASE SELECTED")
		return()

	command=command[13:]
	tname=command.split("(")[0].rstrip(" ")

	if os.path.exists(os.path.join(main.location,main.current_db,tname)):
		print("TABLE_ERROR: TABLE WITH THIS NAME ALREADY EXISTS IN THIS DATABASE")
		return()
	try:
		columns=re.search('\((.+)\)',command).group(1)
		columns=columns.split(',')
		
		metadata=""

		for i in range(len(columns)):
			column_name,columns[i]=columns[i].split()[0].strip(" "),"".join(columns[i].split()[1:]).upper()
			initialize_columndatatype=initialize_datatype(columns[i])
			if initialize_columndatatype!=0:
				metadata+=column_name+" "+initialize_columndatatype+"\n"
			else:
				return(0)
		else:
			os.mkdir(os.path.join(main.location,main.current_db,tname))
			with open(os.path.join(main.location,main.current_db,tname,tname+".yml"),"w") as f:
				f.write(metadata)
				print("TABLE SUCCESSFULLY CREATED.")


	except:
		print("ERROR in create: Syntax Error")
		return()


def describe(tname):
	tname=tname.split()[-1]
	if main.current_db=="":
		print("NO DATABASE SELECTED")
		return()
	try:
		with open(os.path.join(main.location,main.current_db,tname,tname+'.yml')) as f:
			data = f.readlines()
			
			if data==[]:
				print("NO COLUMNS IN TABLE.")
				return(0)
			data=[ i.strip("\n").split() for i in data  ]
			x=[ max([max([len(i[0])+2,6]) for i in data  ]) , max([ max([len(i[1])+2,6]) for i in data ]) ]	
			print("+"+"-"*x[0]+ "+" +"-"*x[1]+"-+")
			print("|{}| {}|".format("NAME".center(x[0]),"TYPE".center(x[1])))
			print("+"+"-"*x[0]+ "+" +"-"*x[1]+"-+")
			for i in data:
				print("|{}| {}|".format(i[0].ljust(x[0]),i[1].ljust(x[1])))
				print("+"+"-"*x[0]+ "+" +"-"*x[1]+"-+")
			return


	except:
		print("ERROR: '{}' not found".format(tname))
		return

def insert_into_values(command):
	tname=command.split()[2]
	if main.current_db=="":
		print("NO DATABASE SELECTED")
		return()
	try:
		with open(os.path.join(main.location,main.current_db,tname,tname+'.yml')) as f:
			columns_name=[]
			columns=[]
			data=f.readlines()
			for i in data:
				columns_name.append(i.split()[0])
				i=i.split()[-1]
				i=i.strip(')').split("(")
				if i[-1]=="":
					i[-1]==None
				columns.append(i)
	except:
		print("ERROR: '{}' not found".format(tname))
		return
	try:
		if os.path.exists(os.path.join(main.location,main.current_db,tname,tname+'.dat')):
			f=open(os.path.join(main.location,main.current_db,tname,tname+'.dat'),'a')
		else:
			f=open(os.path.join(main.location,main.current_db,tname,tname+'.dat'),'w')
		writer=csv.writer(f,quoting=csv.QUOTE_NONNUMERIC)
		data=eval( '['+re.search('\((.+)\)',command).group(1)+"]")
		if len(data)!=len(columns_name):
			print("ENTERED TUPLE DOES NOT CONTAIN REQUIRED NUMBER OF VALUES.")
			print("ERROR: DATA NOT ENTERED.")
			return 0
		
		for i in range(len(data)):
			if datatypes[columns[i][0]](columns[i][1],data[i],columns_name[i]) == 0:
				print("ERROR: DATA NOT ENTERED. CHECK SYNTAX.")
				f.close()
				return
		writer.writerow(data)
		f.close()
		print("SUCCESSFULLY ENTERED DATA.")
	except:
		print("ERROR: Invalid Syntax.")
		return 0

def initialize_datatype(command):
	''' will return attribute None if data_type or data_typr()'''
	try:
		column_datatype=command.split("(")[0].upper()
		attributes=re.search("\((.+)\)",command).group(1)
		attributes=datatypes[column_datatype](attributes)		
	except:
		column_datatype=command.upper().strip("()")
		attributes=datatypes[column_datatype]()

	if attributes==0:
		print("Invalid Syntax")
		return(0)
	else:
		return(column_datatype+"({})".format(attributes))


def drop(command):
	if main.current_db=="":
		print("NO DATABASE SELECTED")
		return()
	tname=command.split()[-1]
	path=os.path.join(main.location,main.current_db,tname)
	if os.path.exists(path):
		shutil.rmtree(path)
		print("TABLE '{}' REMOVED SUCCESSFULLY ".format(tname))
		return
	else:
		print("TABLE_ERROR: TABLE NOT FOUND")
		return





