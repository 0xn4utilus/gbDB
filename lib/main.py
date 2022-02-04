import os,time,sys
script_dir = str(os.path.abspath(__file__)).rstrip("main.py")
if os.path.exists(os.path.join(script_dir,"config.config")):
	with open(os.path.join(script_dir,"config.config"),"r") as f:
		location = f.readline()
		try:
			os.chdir(location)
		except	FileNotFoundError:
			print("Location of database working folder not found!\nPlease ensure that correct path of working database folder is in 'config.congig' file(can be found in 'lib' folder)(you can also try deleting the 'config.config' file) and try again.")
			input("\n\nPress any key to exit.")
			exit()
		
else:
	with open(os.path.join(script_dir,"config.config"),"w") as f:
		f.write(os.path.join(os.getcwd(),os.pardir,"databases") )
	if os.path.exists(os.path.join(os.getcwd(),os.pardir,"databases")):
		pass
	else:
		os.mkdir(os.path.join(os.getcwd(),os.pardir,"databases"))
	location=os.getcwd()
current_db=''

import database,table,queries
try:
	from prompt_toolkit import *
	from prompt_toolkit.styles import Style
	from prompt_toolkit.completion import NestedCompleter
	from prompt_toolkit.history import FileHistory
except:
	print("INSTALLING NECCESSARY MODULES\nPLEASE WAIT...")
	import pip
	pip.main(['install',os.path.join(script_dir,"prompt_toolkit")])
	print("\n\n...PLEASE RESTART THE APPLICATION...")
	exit()



def main():
	commands={"\\q":bye,"exit":bye, "use":database.use ,"create database":database.create ,"drop database":database.drop ,"delete database":database.drop ,"describe":table.describe,"create table":table.create,"insert into":table.insert_into_values,"drop table":table.drop,"show tables":database.grab_tables ,"show databases":database.grab_databases, "select":queries.select,"delete from":queries.delete}
	print("\nWELCOME TO gbDB :)\n\nUse '\\q' or 'exit;' to exit. Uses SQL commands.")

	session = PromptSession(history=FileHistory(os.path.join(script_dir,'.myhistory')))
	completer = NestedCompleter.from_nested_dict({
		'show': {'databases': None,'tables': None},
		'exit': None,
		'\\q': None,
		'create':{'database':None,'table':None},
		'drop': {'database':None,'table':None},
		'delete': {'database':None,'from':None},
		'select': {'*':{'from':None}},
		'describe':None,
		'insert': {'into':None},
		'use': None,
		'where': None,
		'values': None,

	})

	styles=Style.from_dict({"colour":"#2db4d6 bold"})

	while True:
		command = session.prompt(HTML("<colour>\n>>> </colour>"),completer=completer,style=styles)
		if command=="":
			continue
		while command[-1] != ";":
			command += " "+ session.prompt(HTML("<colour>  > </colour>"),completer=completer,style=styles)
		command=" ".join(command.rstrip(";").split())
		check=command.lower()

		for cmd in commands:
			if check.startswith(cmd):
				t=time.time()
				commands[cmd](command)
				print("Time Taken: {:.3f} seconds".format(time.time()-t))


def bye(command):
	print("BYE :)")
	exit()


if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print("Oops, something went wrong.Told you it is under development. ;)")
		time.sleep(3)
		sys.exit(1)


