import sqlite3
import sys
conn=sqlite3.connect('sensorsData.db')
curs=conn.cursor()
# function to insert data on a table
def add_data (tempe, light,sound,co2value,covalue,humvalue):
    curs.execute("INSERT INTO dummy_data values(datetime('now'), (?), (?),(?),(?),(?),(?))", (tempe, light,sound,co2value,covalue,humvalue))
    conn.commit()
# call the function to insert data
add_data (20.5, 30,1,1,1,1)
add_data (25.8, 40,2,2,2,2)
add_data (30.3, 50,3,3,3,3)
# print database content
print ("\nEntire database contents:\n")
for row in curs.execute("SELECT * FROM dummy_data"):
    print (row)
# close the database after use
conn.close()