import io
import time
import sqlite3
#import server2
from threading import Lock

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template, send_file, make_response, request

lock = Lock()

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
    try:
        lock.acquire(True)
        curs.execute("SELECT * FROM Room_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
        data = curs.fetchall()
    finally:
        lock.release()

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

@app.route("/historical")
def my_historical():
    global numSamples   
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
    return render_template('historical.html', **templateData)

@app.route("/historical", methods=['POST'])
def my_historical_post():
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
    return render_template('historical.html', **templateData)  

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

@app.route("/plot/light")
def plot_light():
    times, tempes, lights, sounds, co2values, covalues, humvalues = getHistData(numSamples)
    ys = lights
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Lights [lux]")
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

@app.route("/plot/sound")
def plot_sound():
    times, tempes, lights, sounds, co2values, covalues, humvalues = getHistData(numSamples)
    ys = sounds
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Sound [dB]")
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


@app.route("/plot/co2value")
def plot_co2value():
    times, tempes, lights, sounds, co2values, covalues, humvalues = getHistData(numSamples)
    ys = co2values
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Co2 Value [ppm]")
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


@app.route("/plot/covalue")
def plot_covalue():
    times, tempes, lights, sounds, co2values, covalues, humvalues = getHistData(numSamples)
    ys = covalues
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Co Value [ppm]")
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




