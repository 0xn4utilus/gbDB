#datatypes={"BOOLEAN":data_types.BOOLEAN,"SET":data_types.SET,"ENUM":data_types.ENUM, "CHAR":data_types.CHAR,"VARCHAR":data_types.VARCHAR,"TINYTEXT":data_types.TINYTEXT,"TEXT":data_types.TEXT,"BLOB":data_types.BLOB,"MEDIUMBLOB":data_types.MEDIUMBLOB,"MEDIUMTEXT":data_types.MEDIUMTEXT,"LONGTEXT":data_types.LONGTEXT,"LONGBLOB":data_types.LONGBLOB,"DATE":data_types.DATE,"TIME":data_types.TIME,"TIMESTAMP":data_types.TIMESTAMP,"DATETIME":data_types.DATETIME,"YEAR":data_types.YEAR}

#BOOLEAN DATA TYPE
def BOOLEAN(initializer=None,data=None,column=None):
	if data!=None:
		if data in [1,0,'True','False']:
			return(1)
		else:
			print("ERROR: BOOLEAN does accepts [0/1] or [True/False]")
			return(0)



#SET DATA TYPE
#ENUM ARE DEFINED AS ('VALUE1'|'VALUE2'|...) INSTEAD OF SQL WHICH USES ('VALUE1','VALUE2','VALUE3'...)
def SET(preset=None,data=None,column=None):
	if data != None:
		if type(data) == set:
			pass
		else:
			print("'{}' is a SET field and expects values enclosed in curly_braces".format(column))
			return(0)
		preset=eval("{"+preset+"}")
		for data_element in data:
			if data_element.upper() in preset:
				continue
			else:
				print("ERROR: {} not in {}".format(data_element,str(preset)))
				return(0)
		return(1)
	else:
		if preset==None:
			print("ERROR: No Preset defined for SET")
			return(0)
		else:
			try:
				preset=preset.replace("|",",")
				presetcheck=eval("{"+preset+"}")
				for i in presetcheck:
					if type(i)==str:
						continue
					else:
						print("SET must contain only string literals")
						return(0)
				return(preset)
			except:
				return(0)


#ENUM DATA TYPE
def ENUM(preset=None,data=None,column=None):
	if data != None:
		preset=eval("["+preset+"]")
		if data in preset:
			pass
		else:
			print("ERROR: '{}' not in {}".format(data,str(preset)))
			return(0)
		return(1)
	else:
		if preset==None:
			print("ERROR: No Preset defined for SET")
			return(0)
		else:
			try:
				preset=preset.replace("|",",")
				presetcheck=eval("["+preset+"]")
				for i in presetcheck:
					if type(i)==str:
						continue
					else:
						print("ENUM must contain only string literals")
						return(0)
				return(preset)
			except:
				return(0)
		


#NUMERIC DATA TYPE

def TINYINT(length=None,data=None,column=None):
	if data!=None:
		try:
			if type(data) != int:
				print("ERROR: Please Enter a valid integer value.")
				return(0)
			data=int(data)
			if data<=127 and data>=-128:
				return(1)
			print("ERROR: TINYINT supports value between -128 and 127 only.")
			return(0)
		except:
			print("ERROR: Please Enter a valid integer value.")
			return(0)
	else:
		if length == None:
			pass
		else:
			print("ERROR: TINYINT data-type not yet supports arguments. Please create TINYINT type column without arguments.")
			return(0)
		return('')

def MEDIUMINT(length=None,data=None,column=None):
	if data!=None:
		try:
			if type(data) != int:
				print("ERROR: Please Enter a valid integer value.")
				return(0)
			data=int(data)
			if data<=8388607 and data>=-8388608:
				return(1)
			print("ERROR: MEDIUMINT supports value between -8388608 and 8388607 only.")
			return(0)
		except:
			print("ERROR: Please Enter a valid integer value.")
			return(0)
	else:
		if length == None:
			pass
		else:
			print("ERROR: MEDIUMINT data-type not yet supports arguments.Please create MEDIUMINT type column without arguments.")
			return(0)
		return('')

def INT(length=None,data=None,column=None):
	if data!=None:
		try:
			if type(data) != int:
				print("ERROR: Please Enter a valid integer value.")
				return(0)
			data=int(data)
			if data<=2147483647 and data>=-2147483648:
				return(1)
			print("ERROR: INT supports value between -2147483648 and 2147483647 only.")
			return(0)
		except:
			print("ERROR: Please Enter a valid integer value.")
			return(0)
	else:
		if length == None:
			pass
		else:
			print("ERROR: INT data-type not yet supports arguments.Please create INT type column without arguments.")
			return(0)
		return('')

def BIGINT(length=None,data=None,column=None):
	if data!=None:
		try:
			if type(data) != int:
				print("ERROR: Please Enter a valid integer value.")
				return(0)
			data=int(data)
			if data<=2**63 -1 and data>=-2**63:
				return(1)
			print("ERROR: BIGINT supports value between -2**63 and 2**63 -1 only.")
			return(0)
		except:
			print("ERROR: Please Enter a valid integer value.")
			return(0)
	else:
		if length == None:
			pass
		else:
			print("ERROR: BIGINT data-type not yet supports arguments.Please create BIGINT type column without arguments.")
			return(0)
		return('')



#FLOAT DATA TYPES


#STRING DATA TYPES
def CHAR(length=255,data=None,column=None):
	if data!=None:
		length=int(length)
		if type(data)== str:
			pass
		else:
			print("PLEASE ENTER VALID STRING VALUE FOR COLUMN '{}'.".format(column))
		if len(data)>length:
			print("ERROR: Maxium allowed length for {} is {}, entered data is of length {}".format(column,length,len(data)))
			return(0)
		return(1)
	else:
		try:
			if int(length)<=255 and int(length)>0:
				return(length)
			else:
				print("ERROR: Maxium length of CHAR is 255")
				return(0)
		except:
			return(0)


def VARCHAR(length=255,data=None,column=None):
	if data!=None:
		if type(data)== str:
			pass
		else:
			print("PLEASE ENTER VALID STRING VALUE FOR COLUMN '{}'.".format(column))
			return 0
		length=int(length)
		if len(data)>length:
			print("ERROR: Maxium allowed length for {} is {}, entered data is of length {}".format(column,length,len(data)))
			return(0)
		return(1)
	else:
		try:
			if int(length)<=255 and int(length)>0:
				return(length)
			else:
				print("ERROR: Maxium length of VARCHAR is 255")
				return(0)
		except:
			return(0)


def TINYTEXT(length=255,data=None,column=None):
	if data!=None:
		if type(data)== str:
			pass
		else:
			print("PLEASE ENTER VALID STRING VALUE FOR COLUMN '{}'.".format(column))
			return 0
		length=int(length)
		if len(data)>length:
			print("ERROR: Maxium allowed length for {} is {}, entered data is of length {}".format(column,length,len(data)))
			return(0)
		return(1)
	else:
		try:
			if int(length)<=255 and int(length)>0:
				return(length)
			else:
				print("ERROR: Maxium length of TINYTEXT is 255")
				return(0)
		except:
			return(0)

def TEXT(length=65535,data=None,column=None):
	if data!=None:
		if type(data)== str:
			pass
		else:
			print("PLEASE ENTER VALID STRING VALUE FOR COLUMN '{}'.".format(column))
			return 0
		length=int(length)
		if len(data)>length:
			print("ERROR: Maxium allowed length for {} is {}, entered data is of length {}".format(column,length,len(data)))
			return(0)
		return(1)
	else:
		try:
			if int(length)<=65535 and int(length)>0:
				return(length)
			else:
				print("ERROR: Maxium length of TEXT is 65535")
				return(0)
		except:
			return(0)

#BLOB AND TEXT HAVE SAME DEFINATION,WILL FIX LATTER
def BLOB(length=65535,data=None,column=None):
	if data!=None:
		if type(data)== str:
			pass
		else:
			print("PLEASE ENTER VALID STRING VALUE FOR COLUMN '{}'.".format(column))
			return 0
		length=int(length)
		if len(data)>length:
			print("ERROR: Maxium allowed length for {} is {}, entered data is of length {}".format(column,length,len(data)))
			return(0)
		return(1)
	else:
		try:
			if int(length)<=65535 and int(length)>0:
				return(length)
			else:
				print("ERROR: Maxium length of BLOB is 65535")
				return(0)
		except:
			return(0)

def MEDIUMBLOB(length=16777215,data=None,column=None):
	if data!=None:
		if type(data)== str:
			pass
		else:
			print("PLEASE ENTER VALID STRING VALUE FOR COLUMN '{}'.".format(column))
			return 0
		length=int(length)
		if len(data)>length:
			print("ERROR: Maxium allowed length for {} is {}, entered data is of length {}".format(column,length,len(data)))
			return(0)
		return(1)
	else:
		try:
			if int(length)<=16777215 and int(length)>0:
				return(length)
			else:
				print("ERROR: Maxium length of MEDIUMBLOB is 16777215")
				return(0)
		except:
			return(0)

def MEDIUMTEXT(length=16777215,data=None,column=None):
	if data!=None:
		if type(data)== str:
			pass
		else:
			print("PLEASE ENTER VALID STRING VALUE FOR COLUMN '{}'.".format(column))
			return 0
		length=int(length)
		if len(data)>length:
			print("ERROR: Maxium allowed length for {} is {}, entered data is of length {}".format(column,length,len(data)))
			return(0)
		return(1)
	else:
		try:
			if int(length)<=16777215 and int(length)>0:
				return(length)
			else:
				print("ERROR: Maxium length of MEDIUMTEXT is 16777215")
				return(0)
		except:
			return(0)


def LONGTEXT(length=4294967295,data=None,column=None):
	if data!=None:
		if type(data)== str:
			pass
		else:
			print("PLEASE ENTER VALID STRING VALUE FOR COLUMN '{}'.".format(column))
			return 0
		length=int(length)
		if len(data)>length:
			print("ERROR: Maxium allowed length for {} is {}, entered data is of length {}".format(column,length,len(data)))
			return(0)
		return(1)
	else:
		try:
			if int(length)<=4294967295 and int(length)>0:
				return(length)
			else:
				print("ERROR: Maxium length of LONGTEXT is 4294967295")
				return(0)
		except:
			return(0)

def LONGBLOB(length=4294967295,data=None,column=None):
	if data!=None:
		if type(data)== str:
			pass
		else:
			print("PLEASE ENTER VALID STRING VALUE FOR COLUMN '{}'.".format(column))
			return 0
		length=int(length)
		if len(data)>length:
			print("ERROR: Maxium allowed length for {} is {}, entered data is of length {}".format(column,length,len(data)))
			return(0)
		return(1)
	else:
		try:
			if int(length)<=4294967295 and int(length)>0:
				return(length)
			else:
				print("ERROR: Maxium length of LONGBLOB is 4294967295")
				return(0)
		except:
			return(0)


#DATE AND TIME DATA TYPES
import datetime
def DATE(initializer=None,data=None,column=None):
	if data!=None:
		data=data.split('-')
		if len(data[0])==4 and len(data[1])==2 and len(data[2])==2:
			if data[0].isnumeric() and data[1].isnumeric() and data[2].isnumeric():
				try:
					date=datetime.datetime(int(data[0]),int(data[1]),int(data[2]) )
					return(1)
				except ValueError:
					print("ERROR: Please enter a valid date in 'YYYY-MM-DD'for '{}'".format(column))
					return(0)
		print("ERROR: Please enter a valid date in 'YYYY-MM-DD' for '{}'".format(column))
		return(0)
	else:
		return("")


def TIME(initializer=None,data=None,column=None):
	if data!=None:
		try:
			validtime=datetime.datetime.strptime(data,"%H:%M:%S")
			return(1)
		except ValueError:
			print("ERROR: Enter valid TIME in 'HH:MM:SS' for '{}'".format(column))
			return(0)
	else:
		return("")


#TIMESTAMP AND DATETIME HAS SAME DEFINATION WILL FIX LATTER
def TIMESTAMP(initializer=None,data=None,column=None):
	if data!=None:
		try:
			data,data1=data.split()
			validtime=datetime.datetime.strptime(data1,"%H:%M:%S")
			data=data.split('-')
			if len(data1)== 8:
				pass
			else:
				print("ERROR: Please enter a valid DATETIME in 'YYYY-MM-DD HH:MM:SS' for '{}'".format(column))
				return(0)
			if len(data[0])==4 and len(data[1])==2 and len(data[2])==2:
				if data[0].isnumeric() and data[1].isnumeric() and data[2].isnumeric():
					try:
						date=datetime.datetime(int(data[0]),int(data[1]),int(data[2]) )
						return(1)
					except ValueError:
						print("ERROR: Please enter a valid TIMESTAMP in 'YYYY-MM-DD HH:MM:SS' for '{}'".format(column))
						return(0)
		except:
			print("ERROR: Please enter a valid TIMESTAMP in 'YYYY-MM-DD HH:MM:SS' for '{}'".format(column))
			return(0)
	else:
		return("")

def DATETIME(initializer=None,data=None,column=None):
	if data!=None:
		try:
			data,data1=data.split()
			validtime=datetime.datetime.strptime(data1,"%H:%M:%S")
			data=data.split('-')
			if len(data1)== 8:
				pass
			else:
				print("ERROR: Please enter a valid DATETIME in 'YYYY-MM-DD HH:MM:SS' for '{}'".format(column))
				return(0)

			if len(data[0])==4 and len(data[1])==2 and len(data[2])==2:
				if data[0].isnumeric() and data[1].isnumeric() and data[2].isnumeric():
					try:
						date=datetime.datetime(int(data[0]),int(data[1]),int(data[2]) )
						return(1)
					except ValueError:
						print("ERROR: Please enter a valid DATETIME in 'YYYY-MM-DD HH:MM:SS' for '{}'".format(column))
						return(0)
		except:
			print("ERROR: Please enter a valid DATETIME in 'YYYY-MM-DD HH:MM:SS' for '{}'".format(column))
			return(0)
	else:
		return("")	

def YEAR(initializer=None,data=None,column=None):
	if data!=None:
		if len(data) in [2,4] and data.isnumeric():
			return(1)
		print("ERROR: Please enter a valid YEAR in 'YYYY' or 'YY' for {}".format(column))		
		return(0)
	else:
		return("")












