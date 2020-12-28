import io
import sqlite3
import server2
import threading

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template, send_file, make_response, request


app = Flask(__name__)

conn=sqlite3.connect('/var/www/piapp/dbfolder/sensorsData.db', check_same_thread=False)
curs=conn.cursor()

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
if (numSamples > 21):
    numSamples = 20

# main route
@app.route("/")
def index():
    time, tempe,light,sound,co2value,covalue, humvalue = getLastData()
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
    axis.set_title("Temperature [C]")
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


if __name__ == "__main__":
    #t=threading.Thread(target = server2.arduino)
    #t.daemon = True
    #t.start()
    app.run(host='0.0.0.0', port=80, debug=False)


