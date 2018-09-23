#!/usr/bin/env python

# MIT License

# Copyright (c) 2018 Nat Comeau

# LOCAL
import pops
import frontEnd
# STDLIB
import sys
from astropy import units as u

# SET date; must be date of time of star party in UTC. for star parties, usually
# one day ahead.
date = '08/19/2018'

# Process a list of target names we supplied on the command line.
# First get the sidereal time from the US Naval Observatory:
# Get sidereal time for 10:30pm (5:30 UT -7 hours) on June 30th 2018
st = pops.getSiderealTime(date)
print("Local sidereal time on {} is {}".format(date, st.to_string(unit=u.hour, sep=(':', ':'))))

# Get a list of target names from the command line, or if none provided get input from a txt file
if len(sys.argv) == 1:
    with open('targetlist.txt') as f:
        targets = f.readlines()
    targets = [x.strip('\n') for x in targets]
else:
    targets = sys.argv[1:]

coordinates = []
coordinates_big = []
hour_angles = []
# For each target:
for i in range(len(targets)):
    # With a SIMBAD Query get RA and DEC from the target name.
    # For when a bad target name is entered use the try/except block to catch the errors and skip to the next target.
    ra,dec = None, None
    try:
        ra, dec = pops.getRaDec(targets[i])
    except (IndexError, AttributeError):
        continue
    # Calculate hour angle; HA = ST - RA
    ha = pops.getHourAngle(ra, st)
    coordinates.append((ha.hour, dec.deg,))
    hour_angles.append(ha)
    coordinates_big.append((ra,dec,))
# Print HA, Declinations
print('{:<20}  {:<20}  {:<20}  {:<20}'.format('Name:', 'RA:', 'Dec:', 'HA:'))
for i in range(len(targets)):
    print("{:<20}  {:<20}  {:<20}  {:<20.3f}".format(targets[i], coordinates_big[i][0].to_string(unit=u.hour, sep=(':', ':')), \
    coordinates_big[i][1].to_string(unit=u.degree, sep=('°', '\'', '\"')), \
    hour_angles[i].hour))
# Plot coordinates if they're in the safe zone
# Plot coordinates
frontEnd.plot(coordinates, targets)
