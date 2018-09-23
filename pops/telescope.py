import astropy
import numpy as np
from astropy import units as u
from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord

def calcHA(siderealtime, RA):
    # Get an RA and covert to degrees
    a = Angle(RA)
    ra = a.degree
    # Get a sidereal time and convert to degrees
    st = Angle(siderealtime)
    st = st.degree
    hourangle = st-ra
    hourangle = Angle(str(hourangle)+'degree').hms
    print(hourangle)
