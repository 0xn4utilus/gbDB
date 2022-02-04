import main,table,database
import os,csv,re

keywords=["ALL","DISTINCT","DISTINCTROW","FROM","WHERE","INSERT","IS NULL","IS NOT NULL","LIKE","OR","MIN","MAX","AVG","ORDER BY","SUM","UPDATE","AND","AS","COUNT","DELETE"]
def virtual_table(tname=None):
	with open(os.path.join(main.location,"_virtual_table.dat")) as f:
		data=[]
		reader = csv.reader(f)
		for row in reader:
			if row!=[]:
				data.append(row)
	column_lengths,column_type,column_headings=list( int(x) for x in data[-1] ),data[0],data[1]
	total_columns=len(column_lengths)
	topline,heading='+','| '
	for i in range(total_columns):
		topline+="-"*(column_lengths[i]+2)+"+"
		heading+= column_headings[i].center(column_lengths[i])+' | '
	print(topline,heading,topline,sep="\n")
	for i in range(len(data)-1):
		if i in [0,1]:
			continue
		row="| "
		for x in range(total_columns):
			if column_type[x]=="i":
				row+=data[i][x].rjust(column_lengths[x])+" | "
				continue	
			row+=data[i][x].ljust(column_lengths[x])+" | "
		print(row)
	print(topline)
	os.remove(os.path.join(main.location,"_virtual_table.dat"))

def select(command):
	if main.current_db=="":
		print("DATABASE_ERROR: NO DATABASE SELECTED")
		return(0)
	dummy_cmd=command.lower().split()
	command=command.split()
	try:
		tname=command[dummy_cmd.index("from")+1]
	except:
		print("NO TABLE SELECTED OR TABLE NOT FOUND.KINDLY CHECK.")
		return
		
	grabbed_tables=database.grab_tables(1,"no")
	if grabbed_tables != 0:
		if tname in grabbed_tables:
			pass
		else:
			print("TABLE_ERROR: Table '{}' not found in database.".format(tname))
			return(0)
	else:
		print("DATABASE_ERROR: No tables in selected database")
		return(0)


	
	columns_in_table,columns_in_table_type=[],[]
	with open(os.path.join(main.location,main.current_db,tname,tname+".yml")) as f:
		data=f.readlines()
		for i in data:
			columns_in_table.append(i.split()[0].lower())
			for k in ['numeric','int','tinyint','bigint','smallint','decimal','numeric','float','real']:
				if i.split()[1].lower().strip("\n").startswith(k):
					columns_in_table_type.append('i')
					break
			else:
				columns_in_table_type.append('s')

	conditions=[]
	if "where" in dummy_cmd:
		where_index=dummy_cmd.index("where")
		dummy_cmd[where_index + 1]=re.sub(r"\s+", "", dummy_cmd[where_index + 1])
		conditions=dummy_cmd[where_index + 1].split(",")
		if where(tname,columns_in_table_type,conditions) == 0:
			return 0

	select_columns,original_column_index=[],[]
	if dummy_cmd[1]=="*":
		expected_tables=list(columns_in_table)
		original_column_index=[ x for x in range(len(columns_in_table))]
	else:
		expected_tables= [ x.lower() for x in "".join(command[1].rstrip(")").lstrip("(").split()).split(",")  ]
		for i in expected_tables:
			if i in columns_in_table:
				original_column_index.append(columns_in_table.index(i))
			else:
				print("COLUMN_ERROR: Entered column '{}' is not in '{}'".format(i,tname))
				return(0)
	select_columns=list(expected_tables)
	if conditions==[]:
		make_virtual_table(columns_in_table_type,select_columns,original_column_index,tname,True)		
	else:
		make_virtual_table(columns_in_table_type,select_columns,original_column_index,tname,True,True)
		os.remove(os.path.join(main.location,"temp_where_clause.dat"))
		os.remove(os.path.join(main.location,"temp_where_clause_index.dat"))


def make_virtual_table(column_types,columnnames_to_display,original_column_index,tname,virtual_table_display=None,where=None):
	with open(os.path.join(main.location,"_virtual_table.dat"),'w') as f:
		writer=csv.writer(f,quoting=csv.QUOTE_ALL)		
		try:
			if where==None:
				with open(os.path.join(main.location,main.current_db,tname,tname+".dat")) as datafile:
					data=[]
					reader = csv.reader(datafile)
					for row in reader:
						data.append(row)
					max_size_of_columns=[len(x) for x in columnnames_to_display]
					writer.writerow(column_types)
					writer.writerow(columnnames_to_display)
					for i in data:
						row=[]
						for index in range(len(original_column_index)):
							row.append(i[original_column_index[index]])
							if len(row[-1])>max_size_of_columns[index]:
								max_size_of_columns[index]=len(row[-1])
						writer.writerow(row)
					writer.writerow(max_size_of_columns)
			else:
				with open(os.path.join(main.location,"temp_where_clause.dat")) as datafile:
					data=[]
					reader = csv.reader(datafile)
					for row in reader:
						data.append(row)
					if data==[['--empty--']]:
						print("...EMPTY SET...")
						return()
					max_size_of_columns=[len(x) for x in columnnames_to_display]
					writer.writerow(column_types)
					writer.writerow(columnnames_to_display)
					for i in data:
						row=[]
						for index in range(len(original_column_index)):
							row.append(i[original_column_index[index]])
							if len(row[-1])>max_size_of_columns[index]:
								max_size_of_columns[index]=len(row[-1])
						writer.writerow(row)
					writer.writerow(max_size_of_columns)

		except:
			print("DATA_ERROR: No data in table.")
			return(0)
	if virtual_table_display != None:
		virtual_table()



def where(tname,columns_in_table_type,conditions):
	columns_in_table=[]
	with open(os.path.join(main.location,main.current_db,tname,tname+".yml")) as f:
		data=f.readlines()
		for i in data:
			columns_in_table.append(i.split()[0].lower())

	if os.path.exists(os.path.join(main.location,main.current_db,tname,tname+".dat")):
		pass
	else:
		print("NO DATA IN TABLE.")
		return 0

	with open(os.path.join(main.location,main.current_db,tname,tname+".dat")) as f:
		data,data_lower=[],[]
		reader = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
		for row in reader:
			if row!=[]:
				row1=list(row)
				for i in range(len(row)):
					if columns_in_table_type[i] == 's':
						row[i] = row[i].lower()
					if columns_in_table_type[i] == 'i':
						row1[i],row[i]=int(row1[i]),int(row[i])
				data.append(row1)
				data_lower.append(row)
	conditions_type=[]
	for i in range(len(conditions)):
		condition = conditions[i].lower()
		if '=' in condition and condition.count("=")==1 and '<=' not in condition and '>=' not in condition and '==' not in condition and '!=' not in condition:
			condition=condition.replace("=","==")
		
		condition=condition.replace("not =","!=")
		condition=condition.replace("<>","!=")
		conditions[i] = condition
		try:
			exec(condition)
			conditions_type.append("statement")
		except:
			conditions_type.append("executable")

	ldic={}
	for i in columns_in_table:
		ldic[i]=None

	final_data,final_data_index=[],[]
	count=-1
	for data_element in data_lower:
		count+=1
		flag=1
		ldic["data_element"] = data_element
		for i in range(len(conditions)):
			condition=conditions[i]
			if conditions_type[i]=="statement":
				if eval(condition) == 0:
					flag=0
					break	
				continue
			
			col=""
			for i in condition:
				if i.isalnum():
					col+=i
				else:
					break
			try:
				col_index=columns_in_table.index(col)
			except:
				print(col,"NOT FOUND.")
				return(0)

			exec("{} = data_element[{}]".format(col,col_index),globals(),ldic)
			try:
				if eval(condition,globals(),ldic) == 0:
					flag=0
					break
			except:
				print("PROBLEM IN {} UNDER WHERE CLAUSE.".format(conditions[i]))
				return 0

		if flag==1:
			final_data.append(data[data_lower.index(data_element)])
			final_data_index.append(count)

	with open(os.path.join(main.location,"temp_where_clause.dat"),'w') as f:
		if final_data==[]:
			f.write("--empty--")
		else:
			writer=csv.writer(f,quoting=csv.QUOTE_NONNUMERIC)
			for i in final_data:
				writer.writerow(i)

	with open(os.path.join(main.location,"temp_where_clause_index.dat"),'w') as f:
		if final_data_index==[]:
			f.write("--empty--")
		else:
			writer=csv.writer(f,quoting=csv.QUOTE_NONNUMERIC)
			writer.writerow(final_data_index)


	return 1

def delete(command):
	if main.current_db=="":
			print("DATABASE_ERROR: NO DATABASE SELECTED")
			return(0)
	dummy_cmd=command.lower().split()
	command=command.split()
	try:
		tname=command[dummy_cmd.index("from")+1]
	except:
		print("NO TABLE SELECTED OR TABLE NOT FOUND.KINDLY CHECK.")
		return
		
	grabbed_tables=database.grab_tables(1,"no")
	if grabbed_tables != 0:
		if tname in grabbed_tables:
			pass
		else:
			print("TABLE_ERROR: Table '{}' not found in database.".format(tname))
			return(0)
	else:
		print("DATABASE_ERROR: No tables in selected database")
		return(0)
	
	if "where" in dummy_cmd:
		columns_in_table,columns_in_table_type=[],[]
		with open(os.path.join(main.location,main.current_db,tname,tname+".yml")) as f:
			data=f.readlines()
			for i in data:
				columns_in_table.append(i.split()[0].lower())
				for k in ['numeric','int','tinyint','bigint','smallint','decimal','numeric','float','real']:
					if i.split()[1].lower().strip("\n").startswith(k):
						columns_in_table_type.append('i')
						continue
				else:
					columns_in_table_type.append('s')

		conditions=[]
		where_index=dummy_cmd.index("where")
		dummy_cmd[where_index + 1]=re.sub(r"\s+", "", dummy_cmd[where_index + 1])
		conditions=dummy_cmd[where_index + 1].split(",")
		if where(tname,columns_in_table_type,conditions) == 0:
			return 0

		with open(os.path.join(main.location,"temp_where_clause_index.dat"),'r') as f:
			if f.readline()=="--empty--":
				print("DELETED 0 ROWS.")
				os.remove(os.path.join(main.location,"temp_where_clause_index.dat"))
				os.remove(os.path.join(main.location,"temp_where_clause.dat"))
				return 1
			f.seek(0,0)
			index_to_delete=[]
			reader = csv.reader(f)
			for row in reader:
				if row!=[]:
					index_to_delete.append(row)
			index_to_delete=[  int(x) for x in index_to_delete[0] ]

		with open(os.path.join(main.location,main.current_db,tname,tname+".dat"),'r') as f:
			data=[]
			reader = csv.reader(f)
			for row in reader:
				if row!=[]:
					data.append(row)
		with open(os.path.join(main.location,main.current_db,tname,tname+"_.dat"),'w') as f:
			for i in range(len(data)):
				if i in index_to_delete:
					continue
				writer=csv.writer(f,quoting=csv.QUOTE_NONNUMERIC)
				writer.writerow(data[i])


		os.remove(os.path.join(main.location,main.current_db,tname,tname+".dat"))
		os.rename(os.path.join(main.location,main.current_db,tname,tname+"_.dat"),os.path.join(main.location,main.current_db,tname,tname+".dat"))
		
		if len(data) == len(index_to_delete):
			os.remove(os.path.join(main.location,main.current_db,tname,tname+".dat"))
		
		print("DELETED {} ROWS.".format(len(index_to_delete)))
		os.remove(os.path.join(main.location,"temp_where_clause_index.dat"))
		os.remove(os.path.join(main.location,"temp_where_clause.dat"))
		return(1)


		
	else:
		try:
			os.remove(os.path.join(main.location,main.current_db,tname,tname+".dat"))
		except FileNotFoundError:
			print("DATA NOT FOUND IN TABLE.")
			return(1
				)
		print("DELETED CONTENTS OF TABLE.")
		return(1)
























































