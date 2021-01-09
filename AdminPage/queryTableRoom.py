import sqlite3

def getHistData (numSamples):

    try: 
        conn=sqlite3.connect('sensorsData.db')
        curs=conn.cursor()
        print("Connected to SQLite")

        print ("\nEntire database contents:\n")
        for row in curs.execute("SELECT * FROM Room_data"):
            print(row)
        
        curs.execute("delete from Room_data where timestamp IN (SELECT timestamp from Room_data order by timestamp DESC limit (?) )",str(numSamples))
        
        #curs.execute("delete from Room_data where timestamp IN (SELECT timestamp from Room_data order by timestamp limit (?) )",str(numSamples))
        
        conn.commit()
        print("Record deleted successfully ")
    
        print ("\nEntire database contents:\n")
        for row in curs.execute("SELECT * FROM Room_data"):
            print(row)
    
        curs.close()
    
    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)

    finally:
        if (conn):
            conn.close()
            print("the sqlite connection is closed")


numsample = 1
getHistData(numsample)