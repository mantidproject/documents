# -----------------------------------------------------
#  Python Training Exercise 3 Solution.
#  Controlling the MantidPlot items
#------------------------------------------------------
# Perform some algorithms to so that we have some sensible data to plot and look at
rootdir = "C:/Mantid/Test/data/"
# Load bank 1 from GEM
LoadRaw(rootdir+ "GEM40979.raw", "GEM-bank2", SpectrumMin="431", SpectrumMax="750")

# Convert to dSpacing
ConvertUnits("GEM-bank2","GEM-bank2", "dSpacing")

# Smooth the data
SmoothData("GEM-bank2", "GEM-bank2", NPoints="20")

# Plot two spectra and merge
g1 = plotSpectrum("GEM-bank2",0)
mergePlots(g1, plotSpectrum("GEM-bank2",1))

# Add another spectra
mergePlots(g1, plotSpectrum("GEM-bank2",2))

# Set the scales on the x- and y-axes
layer = g1.activeLayer()
layer.setAxisScale(Layer.Bottom, 4, 6)
layer.setAxisScale(Layer.Left, 0, 15)

# Optionally rename the curve titles
layer.setCurveTitle(0, "bank2, spectrum " + str(431))
layer.setCurveTitle(1, "bank2, spectrum " + str(432))
layer.setCurveTitle(2, "bank2 spectrum "+ str(433))
