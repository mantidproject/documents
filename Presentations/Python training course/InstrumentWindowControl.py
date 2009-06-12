# -----------------------------------------------------
#  Python Training Exercise 3 Solution.
#  Controlling the instrument window
#------------------------------------------------------

# Load some LOQ data
rootdir = "C:/MantidInstall/"
LoadRaw(rootdir + "data/LOQ48097.raw","LOQ")

# Get a handle on the instrument window
insView = getInstrumentView("LOQ")

# Change the colour map
insView.changeColorMap(rootdir + "colormaps/_standard.map")

# Set the range of values to display
insView.setColorMapRange(0.,195)

# Raise the window
insView.showWindow()