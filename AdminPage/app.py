import io
import sqlite3
from threading import Lock

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template, send_file, make_response, request


lock = Lock()

app = Flask(__name__)


conn=sqlite3.connect('/var/www/piapp/dbfolder/sensorsData.db', check_same_thread=False)
curs=conn.cursor()

"""
# Retrieve LAST data from database
def getLastData():
    for row in curs.execute("SELECT * FROM Room_data ORDER BY timestamp DESC LIMIT 1"):
        time = str(row[0])
        tempe = row[1]
        light = row[2]
        sound = row[3]
        co2value = row[4]
        covalue = row[5]
        humvalue = row[6]
    #conn.close()
    return time, tempe, light,sound, co2value, covalue, humvalue

def getHistData (numSamples):
    curs.execute("SELECT * FROM Room_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
    data = curs.fetchall()
    dates = []
    tempes = []
    lights = []
    sounds = []
    co2values = []
    covalues = []
    humvalues = []
    for row in reversed(data):
        dates.append(row[0])
        tempes.append(row[1])
        lights.append(row[2])
        sounds.append(row[3])
        co2values.append(row[4])
        covalues.append(row[5])
        humvalues.append(row[6])
    return dates, tempes, lights, sounds, co2values, covalues, humvalues

def maxRowsTable():
    for row in curs.execute("select COUNT(tempe) from  Room_data"):
        maxNumberRows=row[0]
    return maxNumberRows
# define and initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
    numSamples = 100
"""

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
    return render_template('deletedesc.html')

@app.route("/deletedesc", methods=['POST'])
def post_delete_desc():
    numSamples1 = int (request.form['numSamples1'])
    numMaxSamples = maxRowsTable()
    if (numSamples1 > numMaxSamples):
        numSamples1 = (numMaxSamples-1)

    data1 = deleteDataDesc(numSamples1)
        
    return render_template('deletedesc.html', data1=data1)


@app.route("/deleteasc")
def delete_asc():        
    return render_template('deleteasc.html')

@app.route("/deleteasc", methods=['POST'])
def post_delete_asc():
    numSamples2 = int (request.form['numSamples2'])
    numMaxSamples = maxRowsTable()
    if (numSamples2 > numMaxSamples):
        numSamples2 = (numMaxSamples-1)

    data2 = deleteDataAsc(numSamples2)
        
    return render_template('deleteasc.html', data2=data2)

"""
@app.route("/", methods=['POST'])
def my_form_post_asc():
    global numSamples1
    numSamples1 = int (request.form['numSamples1'])
    numMaxSamples = maxRowsTable()
    if (numSamples1 > numMaxSamples):
        numSamples1 = (numMaxSamples-1)
    
    data1 = deleteDataAsc(numSamples1)
        
    return render_template('index.html', data1=data1)
"""

"""
@app.route("/", methods=['POST'])
def my_form_post():
    global numSamples
    numSamples = int (request.form['numSamples'])
    numMaxSamples = maxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = (numMaxSamples-1)
    time, tempe, light,sound, co2value, covalue, humvalue = getLastData()
    templateData = {
        'time'  : time,
        'tempe' : tempe,
        'light' : light,
        'sound' : sound,
        'co2value'  : co2value,
        'covalue'   : covalue,
        'humvalue'  : humvalue,
        'numSamples': numSamples
    }
    return render_template('index.html', **templateData)

@app.route("/plot/tempe")
def plot_temp():
    times, tempes, lights, sounds, co2values, covalues, humvalues = getHistData(numSamples)
    ys = tempes
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Temperature [°C]")
    axis.set_xlabel("Samples")
    axis.grid(True)
    xs = range(numSamples)
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@app.route("/plot/humvalue")
def plot_hum():
    times, tempes, lights, sounds, co2values, covalues, humvalues = getHistData(numSamples)
    ys = humvalues
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Humidity [%]")
    axis.set_xlabel("Samples")
    axis.grid(True)
    xs = range(numSamples)
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

"""

if __name__ == "__main__":
   app.run()