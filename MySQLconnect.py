#!/usr/bin/python3.4
from mysql.connector import MySQLConnection, Error
from MySQLdbconfig import read_db_config
 
 
def connect(filename, section):
    """ Connect to MySQL database """
 
    db_config = read_db_config(filename, section)
    conn = MySQLConnection(**db_config)
    return conn
 
 
if __name__ == '__main__':
    connect('config.ini', 'mydb')