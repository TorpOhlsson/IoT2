from flask import Flask, render_template
import base64
from io import BytesIO
import numpy
from matplotlib.figure import Figure
from get_sensor_data import get_sensor_data

app = Flask(__name__)
#application = app

def sonde_ppm():
    ppm1, ppm2, ppm3,latitude, longtitude, error, timestamps, id = get_sensor_data(10)
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    fig.subplots_adjust(bottom=0.3,right=0.8)
    ax.tick_params(axis='x', which='both',rotation=30)
    ax.set_facecolor("#fff")
    fig.set_figwidth(15)
    fig.set_figheight(6)
    ax.set_title("Sonde Nummer " + str(id[0]))
    dybde1,= ax.plot(timestamps,ppm1, c="#a35903",linewidth="1.5")
    dybde2,=ax.plot(timestamps,ppm2, c="#00a63d",linewidth="1.5")
    dybde3,=ax.plot(timestamps,ppm3, c="#007bb0",linewidth="1.5")
    ax.set_xlabel("Timestamps")
    ax.set_ylabel("PPM (Parts per million)")
    fig.patch.set_facecolor("#fff")
    ax.legend((dybde3, dybde2, dybde1), ('30cm', '20cm','10cm'),loc='upper left', shadow=True, bbox_to_anchor=(1, 1.03),title='Dybde')
    ax.tick_params(axis="x",colors="black")
    ax.tick_params(axis="y",colors="black")
    ax.spines[['left','right','top','bottom']].set_visible(False)
    ax.grid(axis='y',linewidth='1')
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def markers():
    ppm1, ppm2, ppm3,latitude, longtitude, error, timestamps, id = get_sensor_data(1)
     
    return latitude[0], longtitude[0], id[0]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sonde')
def sonde():
    sonde_partikel = sonde_ppm()
    sonde_gps = markers()
    return render_template('sonde.html', sonde_partikel = sonde_partikel, sonde_gps = sonde_gps)

@app.route('/about')
def about():
    return render_template('about.html')
#app.run(debug = True)