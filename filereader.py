from queries import createtable, insertmanyquery
import SQLlibrary, sys

def maketable(file, headerswanted, autoincrcol, datetim, unixtim, delimeter, configfile, section, tabletitle):
	file.seek(0,0)
	headers = SQLlibrary.createheaderlist(file, headerswanted, autoincrcol, datetim, unixtim, delimeter)
	createtable(configfile, section, tabletitle, headers)
def datatransfer(file, headerswanted, configfile, section, tabletitle, delimeter):
	'''transfers data from a delimited file into a table from line 2 and on
	should be able to work without headerswanted.. should just look up headers in sql table'''
	file.seek(0,0)
	headerdict = SQLlibrary.chooseheaders(file, headerswanted, delimeter)
	file.seek(0,0)
	file.readline()
	headers = [a for a in headerdict]
	headers = ', '.join(headers)
	valuelist=[]
	for line in file:
		linelist = line.split(delimeter)
		linelist[-1] = linelist[-1].strip()
		values = tuple(linelist[headerdict[h][0]] for h in headerdict)
		valuelist.append(values)
	insertmanyquery(configfile, section, tabletitle, headers, valuelist)

def validateinput(file, delimeter):
	if SQLlibrary.countheaders(file, delimeter)['bytesize']< 65535 and SQLlibrary.countheaders(file, delimeter)['number of columns'] < 1024:
		return True
	else:
		return False


if __name__ == '__main__':
	configfile = 'config.ini'
	section = 'mydb'
	filename = sys.argv[1]
	file = open(filename, 'r')
	delimeter = '\t' #getting error, see bottom of page for traceback
	#delimeter = input("please input your file's delimeter")
	if validateinput(file, delimeter):	
		headerswanted = input('please input headerswanted seperated by commas, type "all" for all headers ')
		autoincrcol = input('do you want an autoincrementing primary key? type "none" if no, type the name of the column if yes ')
		datetim = input('do you want to include a datetime of entry? (type "no" if not) ')
		unixtim = input('do you want to include a unixtime of entry? (type "no" if not) ')
		tabletitle = input('what would you like to name your table? ')
		maketable(file, headerswanted, autoincrcol, datetim, unixtim, delimeter, configfile, section, tabletitle)
		datatransfer(file, headerswanted, configfile, section, tabletitle, delimeter)
	else:
		print ('table is too big')

