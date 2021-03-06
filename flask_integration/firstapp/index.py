from flask import Flask, request, jsonify, render_template
# STDLIB
import urllib
import ssl
import json
import numpy as np
from astropy import units as u
from astropy.coordinates import Angle

app = Flask(__name__)

safeZone = {"safeZone":[
                [0, -20],
                [15, -18],
                [30, -16],
                [45, -14],
                [60, -10],
                [75, 0],
                [90, 10],
                [90,20],
                [90,30],
                [90,40],
                [90,50],
                [90,60],
                [90,70],
                [75,70],
                [75,90],
                [60, 90],
                [45,90],
                [30,90],
                [15,90],
                [0, 90],
                [0,80],
                [0,70],
                [0,60],
                [0,50],
                [-15, 50],
                [-30, 50],
                [-45,50],
                [-60,50],
                [-60, 40],
                [-75, 40],
                [-75,20],
                [-67.5,15],
                [-60, 10],
                [-52.5, 5],
                [-45,0],
                [-37.5,-5],
                [-30,-5],
                [-22.5,-10],
                [-15,-10],
                [-7.5,-10],
                [-7.5,-10],
                [0,-20]] }

#safeZone = {"safeZone": [[0,90],[60,90],[60,-40],[0,-40],[0,90]]}

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/safezone')
def safezone():
    return jsonify(safeZone)


@app.route('/siderealtime/')
def getSiderealTime(date='12/25/2018', coords='48.4284N, 123.3656W', reps=1, intmag=1, intunit='minutes', time="05:00:00.000 AM -7"):
    """Query US Naval Observatory for local sidereal time. Must enter date and time relative to UTC, not local time.

    Args:
        date (string): date for query. Eg "09/25/2049", "9/25/1937".
        coordinates (string): lattiude and longitude of observers position.
                              Eg: 41.89N, 12.48E
        reps (string): number of iterations, eg 5
        intv_mag (string): interval magnitude, eg 5 (means 5 minutes in this example)
        intv_unit (string): interval units, eg minutes
        time (string): UT (GMT) start time of queries including time zone.
                       eg. "05:13:05.512 PM -7" corresponds to 10:30 PM in Victoria during daylight savings time.
        filename (string): name of file to write response to.

    Returns:
        An astropy Angle object of the sidereal time.

    Example usage:

        getSiderealTime('09/25/2017', '41.8N, 12.48E', 1, 1, 'minutes', "05:13:05.512 PM -5", 'st.json')

        date = '06/30/2018'
        st = getSiderealTime(date)
        print("Local sidereal time on {} is {}".format(date, st))

    """
    url = "http://api.usno.navy.mil/sidtime?ID=NC&date={}&coords={}&reps={}&intv_mag={}&intv_unit={}&time={}".format(date, coords, reps, intmag, intunit, time)
    # Make the URL safe to use
    url = urllib.parse.quote(url, safe='/:?=&,')
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    # Query the USNO
    html = response.read()
    # Convert bytes to string
    html = html.decode("utf-8")
    # Convert string to JSON
    json_response = json.loads(html)
    # Get sidereal time out of the JSON
    st = json_response['properties']['data'][0]['lmst']
    st.replace(':', ' ')
    st = st + ' hours'
    a = Angle(st)
    st = a.to_string(unit=u.degree, decimal=True, sep=':')
    st = {"siderealtime": st}
    # Looks like 08:52:17.8084; we'll create an angle object from this time
    return jsonify(st)
