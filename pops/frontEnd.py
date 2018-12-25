# Plot our safe zone and possible targets for the evening
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.lines import Line2D
from matplotlib.collections import PatchCollection
import numpy as np
# We'll work in units of hour angle, declination

# Set the length of our evening; we'll have to change this later
OBSERVING_PERIOD = 1

class SafeZone(object):
    def __init__(self):
        self.safe_zone = np.array([ [0, -20],
                [91.24, 10],
                [91.24, 90],
                [0, 90],
                [0, 60],
                [-60.83, 40],
                [-76, 40],
                [-60.83, 10],
                [-45.6, 5],
                [-45.6,0],
                [-15.2,-10]])

def plot(coordinates, names):
    """Plot the available targets in hour angle, declination space

    Parameters:
        coordinates (ndarray): array of hour angle, declination pairs in decimal degrees.
        names (ndarray): names of each target we're feeding in
    Returns:

    """
    # Make a safe_zone polygon
    patches = []
    safe_zone = Polygon(SafeZone().safe_zone, True)
    patches.append(safe_zone)

    p = PatchCollection(patches, alpha=0.4)

    # Make a figure
    fig, ax = plt.subplots()
    fig.suptitle('Plaskett Safe Zone', fontsize=20)

    # Draw in our safe zone
    ax.add_collection(p)
    # Draw in the paths our targets trace through the night, with their names
    for c,name in zip(coordinates, names):
        # If point is outside our safe zone, set the color to red; else set it to blue
        if point_in_poly(c[0]+0.5*OBSERVING_PERIOD, c[1]):
            color = 'b'
        else:
            color = 'r'
        # Make a line stretching from the start of the observing period to the end
        lstart = c[0]
        lstop = c[0] + OBSERVING_PERIOD
        x = np.array([lstart, lstop])
        y = np.array([c[1], c[1]])
        line = Line2D(x, y, color=color)
        ax.add_line(line)
        ax.text(c[0]-0.25, c[1]+2.5, name)
    ax.set_xlim(-6, 8)
    ax.set_ylim(-30, 100)
    ax.set_ylabel('Declination (degrees)',fontsize=18)
    ax.set_xlabel('Hour angle (hours)',fontsize=18)
    # Draw the plot!
    plt.show()

def test():
    """Test our plotting system with fake input data.

    Parameters:
    """
    test_coordinates = np.array([[-3, 50], [0, 0],[6, -20]])
    names = np.array(['M 31', 'M 101', 'M 51'])
    plot(test_coordinates, names)

def point_in_poly(x,y):
    """
    Determine if a point is inside a given polygon or not
    Polygon is a list of (x,y) pairs. This function
    returns True or False.  The algorithm is called
    the "Ray Casting Method".

    """
    n = len(SafeZone().safe_zone)
    inside = False

    p1x,p1y = SafeZone().safe_zone[0]
    for i in range(n+1):
        p2x,p2y = SafeZone().safe_zone[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside
