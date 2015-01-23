# ----------------------------------------------------------------------------------
#  Python Training Exercise 3 Solution.
#  Controlling the MantidPlot items using future.pyplot
#------------------------------------------------------------------------------------
# Perform some algorithms to so that we have some sensible data to plot and look at
ws=Load(Filename="GEM40979.raw", SpectrumMin=431, SpectrumMax=750)

# Convert to dSpacing
ws=ConvertUnits(InputWorkspace=ws, Target= "dSpacing")

# Smooth the data
ws=SmoothData(InputWorkspace=ws, NPoints=20)

# Future import
from pymantidplot.future.pyplot import *

# Plot three spectra
plot(ws, [0, 1, 2, 5])

# Set the scales on the x- and y-axes
xlim(4, 6)
ylim(0, 15)

# Change the title of the x axis
xlabel("New x axis title")
# Change the title of the y axis
ylabel("New y axis title")
