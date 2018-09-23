import sqlite3

def makeTable():
    """
    """
    conn = sqlite3.connect('ngc2000/ngc2000.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE ngc
             (_RAJ2000 real, _DEJ2000 real, Name text, Type text, RAB2000 text, DEB2000 text, Source text, Const text, l_size, size real, mag real, n_mag, Desc, Object, Name_2, Comment)''')

def getTargets(limits):
    """
    """
    conn = sqlite3.connect('ngc2000/ngc2000.db')
    c = conn.cursor()
    # Do this instead
    c.execute('SELECT * FROM ngc WHERE (ngc."_RAJ2000" BETWEEN ? AND ?) AND (ngc."_DEJ2000" BETWEEN ? AND ?) AND ngc."mag" < ?', limits)
    result = c.fetchall()
    conn.close()
    return result
