import main
import os,shutil,time
from glob import glob
def use(command):
	dbname=command.split()[-1]
	if os.path.exists( os.path.join(main.location,dbname) ):
		main.current_db=dbname
		print("CURRENTLY USING DATABASE '{}'.".format(dbname))
		return()
	else:
		print("DATABASE_ERROR: DATABASE NOT FOUND.")
		return()


def create(command):
	if os.path.exists(main.location):
		pass
	else:
		return("WORKING FOLDER NOT FOUND\nENSURE THAT CURRENT WORKING FOLDER EXISTS.")
	command=command.split()
	path = os.path.join(main.location,command[-1])
	if os.path.exists(path):
		print("DATABASE_ERROR: DATABASE ALREADY EXISTS.")
		return
	else:
		os.mkdir(path)
		metadata(path,command[-1])
		print("DATABASE SUCCESSFULLY CREATED.")
		return

def drop(command):
	if os.path.exists(main.location):
		pass
	else:
		return("WORKING FOLDER NOT FOUND\nENSURE THAT CURRENT WORKING FOLDER EXISTS.")
	command=command.split()

	path = os.path.join(main.location,command[-1])
	if os.path.exists(path):
		shutil.rmtree(path)
		print("DATABASE REMOVED SUCCESSFULLY.")
		return
	else:
		print("DATABASE_ERROR: DATABASE NOT FOUND.")
		return

def metadata(path,database):
	with open(os.path.join(path,'metadata.dat') , 'w') as f:
		data="#Database '{}' created on\n#{}\n".format(database,time.ctime())
		f.write(data)

def grab_tables(command,show="yes"):
	if show=="yes":
		if main.current_db=="":
			print("DATABASE_ERROR: NO DATABASE SELECTED.")
		else:
			tables=[ str(os.path.basename( os.path.normpath(x) )) for x in glob(os.path.join(main.location,main.current_db)+"/*/") ]
			if tables==[]:
				print("EMPTY DATABASE.")
				return(0)
			x=max([ max([len(i) for i in tables])+2, 14+len(main.current_db)])	
			print("+-"+"-"*x+"-+")
			print("| {} |".format("TABLES_IN_'{}'".format(main.current_db).ljust(x," ")))
			print("+-"+"-"*x+"-+")
			for i in tables:
				print("| {} |".format(i.ljust(x," ")))
				print("+-"+"-"*x+"-+")
			return(1)
	else:
		if main.current_db=="":
			return(0)
		else:
			tables=[ str(os.path.basename( os.path.normpath(x) )) for x in glob(os.path.join(main.location,main.current_db)+"/*/") ]
			if tables==[]:
				return(0)
			return(tables)

def grab_databases(command,show="yes"):
	if show=="yes":
		databases=[ str(os.path.basename( os.path.normpath(x) )) for x in glob(os.path.join(main.location)+"/*/") ]
		if databases==[]:
			print("NO DATABASES FOUND.")
		else:
			x=max([max([ len(i) for i in databases])+2,12])
			print("+-"+"-"*x+"-+")
			print("| {} |".format("DATABASES".ljust(x," ")))
			print("+-"+"-"*x+"-+")
			for i in databases:
				print("| {} |".format(i.ljust(x," ")))
				print("+-"+"-"*x+"-+")
		return(1)
	else:
		if databases==[]:
			return(0)
		else:
			databases=[ str(os.path.basename( os.path.normpath(x) )) for x in glob(os.path.join(main.location)+"/*/") ]
			if databases==[]:
				return(0)
			else:
				return(databases)

def add_table_metadata(command):
	pass

	








