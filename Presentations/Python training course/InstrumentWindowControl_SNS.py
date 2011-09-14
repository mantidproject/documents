# -----------------------------------------------------
#  Python Training Exercise 3 Solution.
#  Controlling the instrument window
#------------------------------------------------------

# Define some directory locations...
# Data directory
datadir = "C:/MantidInstall/data/"    # Windows default
#datadir = os.path.expandvars("${HOME}/data/")  # UNIX

# Colour Maps directory
colormaps = "C:/MantidInstall/colormaps/"   # Windows 
#colormaps = "/Applications/MantidPlot.app/colormaps/"  # Mac OS X
#colormaps = "/opt/Mantid/colormaps/"  # Linux 

# Load some ARCS data
LoadNexusProcessed(datadir + "Training_Exercise3b_SNS.nxs","ARCS")

# Get a handle on the instrument window
insView = getInstrumentView("ARCS")

# Change the colour map
insView.changeColorMap(colormaps + "BlackBodyRadiation.map")

# Set the range of values to display
insView.setColorMapRange(0.,2000)

# Raise the window
insView.showWindow()
