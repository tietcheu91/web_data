import sqlite3
#import urllib.request, urllib.parse, urllib.error
#import ssl
import re

conn = sqlite3.connect('emaildb.sqlite')
cur =conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

try:
	url = input("Enter file name: ")
	if (len(url) < 1) : url = 'mbox.txt'
	fhand = open(url).readlines()
except FileNotFoundError as e:
	print(e)
#print(fhand)

for line in fhand:
	if not line.startswith('From: '): continue
	pieces = line.split()
	email = pieces[1]
	org = re.find('@(\s+.?)', email)
	print(org) 
	cur.execute('SELECT count FROM Counts WHERE org = ?', (org,))
	row = cur.fetchone()
	if row is None:
		cur.execute('INSERT INTO Counts (org, count) VALUES(?,1)', (org,))
	else:
		cur.execute('UPDATE Counts SET count = count + 1 WHERE org=?', (org,))

	conn.commit()
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in  cur.execute(sqlstr):
	print(str(row[0]), row[1])

cur.close()
