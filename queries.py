#!/usr/bin/python3.4
from MySQLconnect import connect
import mysql.connector

def selectonequery(configfile, section, sqlquery):
	'''connects to a mysql database and makes a query to that database. Need to input a configuration 
	file with host, user, password etc.'''
	cnxn = connect(configfile, section)
	cursor = cnxn.cursor()
	cursor.execute(sqlquery)
	result = cursor.fetchone()
	return result

def selectquery(configfile, section, tabletitle, headers, whereheadsvals):
	'''connects to a mysql database and makes a query to that database. Need to input a configuration 
	file with host, user, password etc. Returns the first value of the result of the select query'''
	cnxn = connect(configfile, section)
	cursor = cnxn.cursor()
	conditional =' AND '.join([key+' = %('+key+')s' for key in whereheadsvals])
	query = "SELECT {0} FROM {1} WHERE {2}".format(headers, tabletitle, conditional)
	cursor.execute(query, whereheadsvals)
	result = cursor.fetchone()
	return result

def selectallquery(configfile, section, tabletitle, headers, whereheadsvals):
	'''connects to a mysql database and makes a select query to that database. Need to input a configuration 
	file with host, user, password etc. Returns a list of the result of the select query '''
	cnxn = connect(configfile, section)
	cursor = cnxn.cursor()
	conditional =' AND '.join([key+' = %('+key+')s' for key in whereheadsvals])
	query = "SELECT {0} FROM {1} WHERE {2}".format(headers, tabletitle, conditional)
	cursor.execute(query, whereheadsvals)
	result = cursor.fetchall()
	return result

def createtable (configfile, section, tabletitle, headers):
	cnxn = connect(configfile, section)
	cursor = cnxn.cursor()
	query = "CREATE TABLE %s (%s);" % (tabletitle, headers)
	#####
	print (query)
	#####
	cursor.execute (query)
	cnxn.commit()
	cursor.close()
	cnxn.close()

def insertmanyquery(configfile, section, tabletitle, headers, values):
	'''connects to a mysql database and inserts a list of tabe delimited rows into a table'''
	cnxn = connect(configfile, section)
	cursor = cnxn.cursor()
	valnum = r"%s, " * len(headers.split(','))
	valnum = valnum[:-2]
	query = "INSERT INTO %s (%s) VALUES (%s)" % (tabletitle, headers, valnum)
	cursor.executemany(query,values)
	cnxn.commit()
	cursor.close()
	cnxn.close()

def deleteallrows(configfile, section, tabletitle):
	cnxn = connect(configfile, section)
	cursor = cnxn.cursor()
	query = "DELETE FROM %s" %tabletitle
	cursor.execute (query)#need to bind variable
	cnxn.commit()
	cursor.close()
	cnxn.close()

def getheadersfromtable(configfile, section, tabletitle):
	cnxn = connect(configfile, section)
	cursor = cnxn.cursor()
	query = r"SELECT column_name FROM information_schema.columns WHERE table_name = '%s';"
	cursor.execute (query, (tabletitle))
	cnxn.commit()
	cursor.close()
	cnxn.close()

def test():
	sqlquery = "SELECT brand FROM marcs_jackets WHERE Purpose = 'biking'"
	configfile = 'config.ini'
	section = 'mydb'
	#print (selectonequery(configfile, section, sqlquery)[0])
	file  = open('MarcsBikes.txt', 'r')
	configfile = 'config.ini'
	section = 'mydb'
	tabletitle = 'MarcsBikes'
	headerslist = ['BikeBrand VARCHAR(255)', 'BikeName VARCHAR(255)', 'Purpose VARCHAR(255)', 'Price VARCHAR(255)', 'YearPurchased INT']
	headers = 'BikeBrand, BikeName, Purpose, Price, YearPurchased'
	values = [('Norco', 'Range', 'Enduro', '8,000.00', '2018')]
	#createtable(configfile, section, tabletitle, headers)
	#insertmanyquery (configfile, section, tabletitle, headers, values)
	

if __name__ == '__main__':
	test()

