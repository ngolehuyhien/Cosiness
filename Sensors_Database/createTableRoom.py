import sqlite3 as lite
import sys
con = lite.connect('sensorsData.db')
with con: 
    cur = con.cursor() 
    cur.execute("DROP TABLE IF EXISTS Room_data")
    cur.execute("CREATE TABLE Room_data(timestamp DATETIME, tempe NUMERIC, light NUMERIC, sound NUMERIC, co2value NUMERIC, covalue NUMERIC, humvalue NUMERIC)")