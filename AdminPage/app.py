import io
import sqlite3
from threading import Lock

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template, send_file, make_response, request


lock = Lock()

app = Flask(__name__)


conn=sqlite3.connect('sensorsData.db', check_same_thread=False)
curs=conn.cursor()


def maxRowsTable():
    for row in curs.execute("select COUNT(tempe) from  Room_data"):
        maxNumberRows=row[0]
    return maxNumberRows

def getHistData (numSamples):
    try:
        lock.acquire(True)
        curs.execute("SELECT * FROM Room_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
        data = curs.fetchall()
    finally:
        lock.release()
        
    return data

def deleteDataDesc (numSamples1):
    try:
        lock.acquire(True)
        curs.execute("delete from Room_data where timestamp IN (SELECT timestamp from Room_data order by timestamp DESC limit (?) )",str(numSamples1))
        data1 = str(numSamples1)+" last records have been deleted successfully (Descending order)!"
        conn.commit()
    
    except sqlite3.Error as error:
        data1 = "Failed to delete record from sqlite table"

    finally:
        lock.release()
        
    return data1

def deleteDataAsc (numSamples2):
    try:
        lock.acquire(True)
        curs.execute("delete from Room_data where timestamp IN (SELECT timestamp from Room_data order by timestamp limit (?) )",str(numSamples2))
        data2 = str(numSamples2)+" first records have been deleted successfully (Ascending order)!"
        conn.commit()
    
    except sqlite3.Error as error:
        data2 = "Failed to delete record from sqlite table"

    finally:
        lock.release()
        
    return data2

def maxRowsTable():
    for row in curs.execute("select COUNT(tempe) from  Room_data"):
        maxNumberRows=row[0]
    return maxNumberRows

global numSamples
global numSamples1
numSamples = maxRowsTable()
if (numSamples > 21):
    numSamples = 20

# main route
@app.route("/")
def index():
    #c = sqlite3.connect('db_path.db')
    #cur = c.cursor()
    data = getHistData(numSamples)
    
    totalData = maxRowsTable()
        
    return render_template('index.html', data=data, totalData = totalData)


@app.route("/", methods=['POST'])
def my_form_post():
    global numSamples
    numSamples = int (request.form['numSamples'])
    numMaxSamples = maxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = (numMaxSamples-1)
    
    data = getHistData(numSamples)

    totalData = maxRowsTable()
    
    return render_template('index.html', data = data, totalData = totalData)

@app.route("/deletedesc")
def delete_desc():
	totalData = maxRowsTable()
	return render_template('deletedesc.html', totalData = totalData)

@app.route("/deletedesc", methods=['POST'])
def post_delete_desc():
    numSamples1 = int (request.form['numSamples1'])
    numMaxSamples = maxRowsTable()
    if (numSamples1 > numMaxSamples):
        numSamples1 = (numMaxSamples-1)

    data1 = deleteDataDesc(numSamples1)
    totalData = maxRowsTable()
    return render_template('deletedesc.html', data1=data1, totalData = totalData)


@app.route("/deleteasc")
def delete_asc():
	totalData = maxRowsTable()
	return render_template('deleteasc.html', totalData = totalData)

@app.route("/deleteasc", methods=['POST'])
def post_delete_asc():
    numSamples2 = int (request.form['numSamples2'])
    numMaxSamples = maxRowsTable()
    if (numSamples2 > numMaxSamples):
        numSamples2 = (numMaxSamples-1)

    data2 = deleteDataAsc(numSamples2)
    totalData = maxRowsTable()
    return render_template('deleteasc.html', data2=data2, totalData = totalData)


if __name__ == "__main__":
   app.run()