import sqlite3

dbname = 'data/db.sqlite3'
dbconn = sqlite3.connect(dbname)
dbconn.row_factory = sqlite3.Row
dbcursor = dbconn.cursor()
