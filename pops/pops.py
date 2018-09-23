import numpy as np
from astropy import units as u
from astropy.coordinates import Angle
import urllib
import json
import xml.etree.ElementTree

# MIT License

# Copyright (c) 2018 Nat Comeau

#    ____  __           __        __  __     ____  __                               __  _           
#    / __ \/ /___ ______/ /_____  / /_/ /_   / __ \/ /_  ________  ______   ______ _/ /_(_)___  ____ 
#   / /_/ / / __ `/ ___/ //_/ _ \/ __/ __/  / / / / __ \/ ___/ _ \/ ___/ | / / __ `/ __/ / __ \/ __ \
#  / ____/ / /_/ (__  ) ,< /  __/ /_/ /_   / /_/ / /_/ (__  )  __/ /   | |/ / /_/ / /_/ / /_/ / / / /
# /_/   /_/\__,_/____/_/|_|\___/\__/\__/   \____/_.___/____/\___/_/    |___/\__,_/\__/_/\____/_/ /_/ 
#     ____  __                  _                _____            __                                 
#    / __ \/ /___ _____  ____  (_)___  ____ _   / ___/__  _______/ /____  ____ ___                   
#   / /_/ / / __ `/ __ \/ __ \/ / __ \/ __ `/   \__ \/ / / / ___/ __/ _ \/ __ `__ \                  
#  / ____/ / /_/ / / / / / / / / / / / /_/ /   ___/ / /_/ (__  ) /_/  __/ / / / / /                  
# /_/   /_/\__,_/_/ /_/_/ /_/_/_/ /_/\__, /   /____/\__, /____/\__/\___/_/ /_/ /_/                   
#                                   /____/         /____/                                 
#              ______  ____  ____  _____ _ 
#            _/_/ __ \/ __ \/ __ \/ ___/| |
#           / // /_/ / / / / /_/ /\__ \ / /
#          / // ____/ /_/ / ____/___/ // / 
#         / //_/    \____/_/    /____//_/  
#         |_|                       /_/      

# Font credits: Slant by Glenn Chappell 3/93 -- based on Standard, Modified by Paul Burton '96'
# Includes ISO Latin-1
# figlet release 2.1 -- 12 Aug 1994                       

def getHourAngle(ra, st):
    """Given a right ascension and sidereal time, find the hour angle.
    Hour Angle (HA) is defined as HA = ST - RA

    Args:
        ra (object): right ascension astropy Angle object.
        st (object): sidereal time astropy Angle object.
    
    Returns:
        ha (object): hour angle astropy Angle object
    """
    ha = st - ra
    return ha

def getSiderealTime(date, coords='48.4284N, 123.3656W', reps=1, intmag=1, intunit='minutes', time="05:00:00.000 AM -7"):
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
    response = urllib.request.urlopen(url)
    # Query the USNO
    html = response.read()
    # Convert bytes to string
    html = html.decode("utf-8")
    # Convert string to JSON
    json_response = json.loads(html)
    # Get sidereal time out of the JSON
    st = json_response['properties']['data'][0]['lmst']
    # Looks like 08:52:17.8084; we'll create an angle object from this time
    st.replace(':', ' ')
    st = st + ' hours'
    a = Angle(st)
    return a

def getRaDec(targetName):
    """Resolve a target name using SIMBAD

    Args:
        targetName (string): Name of a target. Eg "M31", "NGC3923"
    
    Returns:
        ra (object): right ascension as an Astropy angle object.
        dec (object): declination as an Astropy angle object.

    """
    # Make our GET Request url
    url = 'http://cdsweb.u-strasbg.fr/cgi-bin/nph-sesame/-oxp/NSV?{}'.format(targetName)
    url = urllib.parse.quote_plus(url, safe='/:?=&,')
    req = urllib.request.Request(url)
    # Send our request to SIMBAD
    response = urllib.request.urlopen(req)
    the_page = response.read()
    # Get the RA and DEC from the resulting XML
    root = xml.etree.ElementTree.fromstring(the_page)
    # Grab the J2000 RA and DEC and return them; give a small error message if it doesn't work.
    try:
        ra = root[0][1].find('jradeg').text
        dec = root[0][1].find('jdedeg').text
    except (IndexError, AttributeError) as e:
        print("Name {} not resolved.".format(targetName))
        raise e
    ra = Angle(str(ra)+'d')
    dec = Angle(str(dec)+'d')
    return ra,dec