from sys import getsizeof

def checkmysqltype (entry):
	try:
		int(entry)
	except ValueError:
		try:
			float(entry)
		except ValueError:
			if len(entry)>255:
				sqltype ='BLOB'
			elif len(entry) == 0:
				sqltype = 'EMPTY'
			else:
				sqltype ='VARCHAR(255)'
		else:
			sqltype ='FLOAT'
	else:
		sqltype = 'INT'
	return sqltype
typepriority = {'BLOB':4, 'VARCHAR(255)':3, 'FLOAT':2, 'INT':1, 'EMPTY':0}

def chooseheaders (file, headerswanted, delimeter):
	''' file, list or string, string->dictionary
	function creates a dictionary (or JSON) for each desired header in the table. The header name is the key, 
	and the value is a list with the header index in the file line list as the first entry and "NULL" as a place-
	holder for the SQL type. If all headers are wanted in the table, input 'all', otherwise input a list of header names.
	'''
	headerlist = file.readline()
	headerlist = headerlist.split(delimeter)
	headerlist[-1] = headerlist[-1].strip()#gets rid of the newline character at the end of the headerlist
	headerdict = {}
	if headerswanted == 'all':
		headerswanted = headerlist
	for h in headerlist:
		if h in headerswanted:
			headerdict[h] = [(headerlist.index(h)), 'EMPTY']
	return headerdict
 
def headertypes (file, headerswanted, delimeter):
	headerdict = chooseheaders(file, headerswanted, delimeter)
	for line in file:
		linelist = line.split(delimeter)
		for header in headerdict:
			entryindex = headerdict[header][0]
			entry = linelist[entryindex]
			if typepriority[checkmysqltype(entry)]>typepriority[headerdict[header][1]]:
				headerdict[header][1] = checkmysqltype(entry)
			else: 
				continue
	for header in headerdict:
		if headerdict[header][1] == 'EMPTY':
			headerdict[header][1] = 'CHAR(50)' 
	return headerdict

def createheaderlist (file, headerswanted, autoincrcol, datetim, unixtim, delimeter):
	'''file, list or string, string, string -> string
	creates headers list for SQL create table function. File: opened delimited file. Headerswanted: list of desired columns
	from the text file or 'all' if all headers are to be inputted. Autoincrcol: if an auto incrementing primary key is to be used, 
	input its name, otherwise input 'none'
	'''
	headerdict = headertypes(file, headerswanted, delimeter)
	finallist = [a + ' ' + headerdict[a][1] for a in headerdict]
	if autoincrcol != 'none':
		finallist.insert(0, autoincrcol+' INT AUTO_INCREMENT PRIMARY KEY')
	if datetim != 'no':
		finallist.append('updatedate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
	if unixtim != 'no':
		finallist.append('uxtime INT DEFAULT UNIX_TIMESTAMP(NOW()) ON UPDATE UNIX_TIMESTAMP(NOW())') #UNIX_TIMESTAMP(NOW()) function retrieves value
	finallist = ', '.join(finallist)
	return finallist

def countheaders(file, delimeter):
	headerlist = file.readline()
	bytesize = getsizeof(headerlist)
	headerlist = headerlist.split(delimeter)
	numofcol = len(headerlist)
	returndata = {'bytesize':bytesize,'number of columns': numofcol}
	return returndata

def test():

	file  = open('exportFBMInventory_2019-08-09_09_26_02.txt ', 'r')
	headerswanted = ['asin1','asin2','asin3','sku']
	datetim = 'go'
	unixtim = 'none'
	delimeter = '\t'
	autoincrcol = 'rec_id'
	file.seek(0,0)
	print (createheaderlist(file, headerswanted, autoincrcol, datetim, unixtim, delimeter))
if __name__ == '__main__':
	test()

'''
	file = open('test.txt', 'r')
	print (createheaderlist(file, 'none'))
	file = open('test1FLOAT.txt', 'r')
	print (createheaderlist(file, 'none'))
'''





