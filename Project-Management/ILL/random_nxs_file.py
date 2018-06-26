import glob
import os.path
import random

def randomFile(instrument, years, basePath=os.path.join('/' 'net', 'serdon', 'illdata')):
    """Return a path to a random file in ILL's shared data folders.

       Parameters:
       instrument - case insensitive name of the instrument, such as in4, figaro...
       years - an iterable containing the last two digits of the years to include.
       basePath - a path as a string pointing to the shared 'illdata' folder.
    """
    instrument = instrument.lower()
    year = random.choice(years)
    yearDirs = glob.glob(os.path.join(basePath, '{:2}?'.format(year)))
    yearDir = random.choice(yearDirs)
    instrDir = os.path.join(yearDir, instrument)
    expDirs = glob.glob(os.path.join(instrDir, 'exp_*'))
    expDir = random.choice(expDirs)
    dataDir = os.path.join(expDir, 'rawdata')
    files = glob.glob(os.path.join(dataDir, '*.nxs'))
    try:
      return random.choice(files)
    except IndexError:
      pass

