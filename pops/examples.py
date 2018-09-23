import pops
from astropy import units as u
from astropy.coordinates import Angle
import numpy as np
# LOCAL IMPORTS
import ngc2000.query_database
import frontEnd

# MIT License

# Copyright (c) 2018 Nat Comeau

# Run from the terminal with "python examples.py"

def ex1():
    """First example."""
    # Star party date and local time (Default location is Victoria; make sure the time zone offset from GMT is correct!)
    date = '06/30/2018'
    # Query US Naval Observatory for sidereal time
    st = pops.getSiderealTime(date)
    print("Local sidereal time on {} is {}".format(date, st.hms))
    print("Sidereal time in degrees is {}".format(st.deg))

    # Provide an RA and create an Angle object from it
    ra = '13h 29m 52.7s'
    ra = Angle(ra)
    # Get hour angle
    ha = pops.getHourAngle(ra, st)
    print("Hour angle is {} degrees.".format(ha.deg))
    print("Hour angle is {}".format(ha.to_string(unit=u.hour)))

def ex2():
    """Get the hour angle of a single named target."""
    # Get RA and Dec for the Ring Nebula
    ra, dec = pops.getRaDec('Ring Nebula')
    # Get sidereal time for 10:45pm, June 6th
    st = pops.getSiderealTime('06/30/2018', time='05:30:00 PM -7')
    # Get hour angle of the Ring Nebula
    ha = pops.getHourAngle(ra, st)
    print("Hour angle of the ring nebula is: {} .".format(ha.hms))

def ex3():
    """Provide target names on the command line to the script getHA.py ."""
    # Example output:

    # Hour angle, declination of M31 is: 15h06m45.898s , 41deg16m08.634s.
    # Hour angle, declination of Ring Nebula is: -3h04m04.8307s , 33deg01m45.03s.
    # Hour angle, declination of Black Eye is: 2h52m46.6074s , 21deg40m58.692s.
    # Hour angle, declination of NGC 4565 is: 3h13m09.4681s , 25deg59m15.63s.
    # Hour angle, declination of Whirlpool is: 2h19m34.0482s , 47deg13m50.0016s.
    # Hour angle, declination of Pinwheel is: 1h46m17.6653s , 54deg20m55.5s.

    # To get these hour angle, declination pairs from a command line run:
    # ./getHA.py M31 "Ring Nebula" "Black Eye" "NGC 4565" "Whirlpool" "Pinwheel"
    # or
    # python getHA.py M31 "Ring Nebula" "Black Eye" "NGC 4565" "Whirlpool" "Pinwheel"

def ex4():
    """Given an observing date and time, find the available NGC/IC objects.
    """
    MAGNITUDE_LIMIT = 15

    # Get the sidereal time
    # Star party date and local time (Default location is Victoria; the star party takes place while it is already Sunday
    # In Greenwich, so query for the Sunday
    date = '09/02/2018'
    # Query US Naval Observatory for sidereal time
    st = pops.getSiderealTime(date)
    print("Local sidereal time on {} is {}".format(date, st.hms))

    # Given a sidereal time, we can set rough guesses of targets that will and won't be available.
    RA_LOWER_LIMIT = st-Angle('6h')
    RA_UPPER_LIMIT = st+Angle('5h')
    DEC_LOWER_LIMIT = Angle('-17d')
    DEC_UPPER_LIMIT = Angle('90d')

    LIMITS = (RA_LOWER_LIMIT.deg, RA_UPPER_LIMIT.deg, DEC_LOWER_LIMIT.deg, DEC_UPPER_LIMIT.deg, MAGNITUDE_LIMIT,)
    available_targets = ngc2000.query_database.getTargets(LIMITS)

    # Make lists of ra, dec, and names for plotting
    ras = []
    decs = []
    names = []
    for target in available_targets:
        ras.append(target[0])
        decs.append(target[1])
        names.append(target[2])

    # Translate a list of ra's to hour angles
    ras = [Angle(str(x)+'d') for x in ras]
    hourangles = [pops.getHourAngle(x, st) for x in ras]

    # Translate decs to astropy angle objects
    decs = [Angle(str(x)+'d') for x in decs]

    # Make an ndarray of (hour angle, declination) pairs, both in decimal degrees
    hourangles = [x.hour for x in hourangles]
    ras = [x.deg for x in ras]
    decs = [x.deg for x in decs]
    coordinates = np.column_stack((hourangles, decs))
    # Check if in safe zone
    print("Name:                               NGC/IC  Type: RAB2000:   DecB2000:  HA:    Mag:    Description:                                       Comments:                   ")
    print("----------------------------------- -----   ---   -------    ------     -----  ----    -------------------------------------------------- ----------------------------")

    for c, target in zip(coordinates, available_targets):
        if frontEnd.point_in_poly(c[0]+0.5*1, c[1]):
            print("{}{}   {}     {}    {}     {:.2f}  {}     {} {}".format(target[-3], target[-2], target[3], target[4], target[5],c[0],target[-6], target[-4], target[-1]))
    # front end plots in hour angle, declination space with names.
    frontEnd.plot(coordinates, names)

ex4()
