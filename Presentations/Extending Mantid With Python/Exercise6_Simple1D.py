# Extending Mantid With Python: Exercise 4
#
# The aim of this exercise is to implement a Lorentz function, that has no derivative, to fit
# the output data from exercise 3. For simplicity a solution file, 11001_deltaE.nxs
# is provided with the training data.

from mantid.api import *
import math
import numpy as np

INVERSE_PI = 1.0/math.pi

class Lorentz(IFunction1D):

    def init(self):
        # Tell Mantid about the 3 parameters that are involved in the function
        self.declareParameter("Amplitude",0.0)
        self.declareParameter("PeakCentre",0.0)
        self.declareParameter("Gamma",0.0)

    def function1D(self, xvals):
        # xvals is a 1D numpy array that contains the X values for the defined fitting range.

        # Get the current values of the 3 parameters
        amp = self.getParameterValue("Amplitude") # Access current value during the fit
        half_gamma = 0.5*self.getParameterValue("Gamma")
        c = self.getParameterValue("PeakCentre")

        denom = (xvals - c)**2 + half_gamma*half_gamma
        return amp*INVERSE_PI*half_gamma/denom

# Register with Mantid
FunctionFactory.subscribe(Lorentz)

