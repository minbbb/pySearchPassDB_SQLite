import sqlite3
import os
import re
import sys
import argparse

DB_NAME = "pySearchPassDB_SQLite.db"
TABLE_NAME = "pySearchPassDB_SQLite"
PATTERN_SPLIT = (':', ';')

#Function to connect to the database
def connectToDB():
	conn = sqlite3.connect(DB_NAME)
	cursor = conn.cursor()
	return conn, cursor

#Create database and table
def createDBandTable():
	conn, cursor = connectToDB()
	cursor.execute("CREATE TABLE " + TABLE_NAME + " (email text, pass text)")

#Add fields to db
def addToDB(dir):
	conn, cursor = connectToDB()
	doesntParse = open('doesntParse.txt', 'a')
	for files in os.walk(dir):
		for file in files[2]:
			with open(files[0] + "/" + file, errors='ignore') as f:
				for line in f:
					for pattern in PATTERN_SPLIT:
						arrLine = re.split(pattern, line.strip('\n'), maxsplit=1)
						if len(arrLine) == 2:
							break
					else:
						print("Error: string '" + str(arrLine[0].strip('\n')) + "' does not parse")
						doesntParse.write(str(arrLine[0]) + '\n')
						continue
					arrLine[0] = arrLine[0].lower()
					cursor.execute("SELECT email, pass FROM " + TABLE_NAME + " WHERE email=? AND pass=?", [arrLine[0], arrLine[1]])
					if len(cursor.fetchall()) == 0:
						cursor.execute("INSERT INTO " + TABLE_NAME + " VALUES (?, ?)", [arrLine[0], arrLine[1]])
						conn.commit()
	doesntParse.close()

#Clear all db fields
def clearDB():
	conn, cursor = connectToDB()
	cursor.execute("DELETE FROM " + TABLE_NAME)
	conn.commit()

#Search email
def searchEmail(email):
	conn, cursor = connectToDB()
	cursor.execute("SELECT email, pass FROM " + TABLE_NAME + " WHERE email='" + email.lower() + "'")
	return cursor.fetchall()

#Search email and convenient output
def printSearchEmail(email):
	res = searchEmail(email)
	if res:
		for i in range(len(res)):
			print("email: {}, pass: {}".format(res[i][0], res[i][1]))
	else:
		print("Not found")

#Get count fileds of db
def getCountEmails():
	conn, cursor = connectToDB()
	return cursor.execute("SELECT count(*) from " + TABLE_NAME + "").fetchone()[0]

#Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--create', action='store_true', help='Create database and table')
parser.add_argument('-s', '--search', help='Search email', metavar = 'EMAIL')
parser.add_argument('-a', '--add', help='Add fields to db', metavar = 'PATH')
parser.add_argument('-c', '--count', action='store_true', help='Show count fileds of db')
parser.add_argument('--clear', action='store_true', help='Clear all db fields')

if parser.parse_args().create:
	createDBandTable()

if parser.parse_args().count:
	print(getCountEmails())

if parser.parse_args().search:
	printSearchEmail(parser.parse_args().search)

if parser.parse_args().clear:
	clearDB()

if parser.parse_args().add:
	addToDB(parser.parse_args().add)

if len(sys.argv) == 1:
	parser.print_help()
