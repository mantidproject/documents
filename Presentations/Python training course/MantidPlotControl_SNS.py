import os
# -----------------------------------------------------
#  Python Training Exercise 3 Solution.
#  Controlling the MantidPlot items
#------------------------------------------------------
# Perform some algorithms to so that we have some sensible data to plot and look at

# Windows Directory
rootdir = "C:/MantidInstall/data/"
# Unix 
rootdir = os.path.expandvars("${HOME}/data/")

# Load processed data from CNCS
LoadNexusProcessed(rootdir+ "Training_Exercise3a_SNS.nxs", "CNCS")

# Plot three spectra
g1 = plotSpectrum("CNCS",[0,1,2])

# Set the scales on the x- and y-axes
layer = g1.activeLayer()
layer.setAxisScale(Layer.Bottom, -1.5, 1.8)
layer.setAxisScale(Layer.Left, 1, 2500, Layer.Log10)

# Optionally rename the curve titles
layer.setCurveTitle(0, "CNCS, Q = 0.3")
layer.setCurveTitle(1, "CNCS, Q = 0.5")
layer.setCurveTitle(2, "CNCS, Q = 0.7")
