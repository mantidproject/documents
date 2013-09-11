# Extending Mantid With Python: Exercise 4
#
# The aim of this exercise is to implement a Lorentz function, that contains a derivative, to fit
# the output data from exercise 3. For simplicity a solution file, 11001_deltaE.nxs
# is provided with the training data.

from mantid.api import *
import math
import numpy as np

INVERSE_PI = 1.0/math.pi

class LorentzWithDeriv(IFunction1D):

    def init(self):
        # Tell Mantid about the 3 parameters that are involved in the function
        self.declareParameter("Amplitude",1.0)
        self.declareParameter("PeakCentre",0.0)
        self.declareParameter("Gamma",0.1)

    def function1D(self, xvals):
        # xvals is a 1D numpy array that contains the X values for the defined fitting range.

        # Get the current values of the 3 parameters
        amp = self.getParameterValue("Amplitude") # Access current value during the fit
        half_gamma = 0.5*self.getParameterValue("Gamma")
        peak_centre = self.getParameterValue("PeakCentre")

        denom = (xvals - peak_centre)**2 + half_gamma*half_gamma
        return amp*INVERSE_PI*half_gamma/denom

    def functionDeriv1D(self, xvals, out):
        # xvals is a 1D numpy array that contains the X values for the defined fitting range.
        # out is a Jacobian matrix object. Mantid expects the partial deriviatives 
        # w.r.t the paramaters and x values to be stored here
        # Get the current values of the 3 parameters
 
        amplitude = self.getParameterValue("Amplitude")
        peakCentre = self.getParameterValue("PeakCentre")
        gamma = self.getParameterValue("Gamma")
        halfGamma = 0.5*gamma

        for i, xval in enumerate(xvals):
            diff = xval-peakCentre
            invDen1 = 1.0/(gamma*gamma + 4.0*diff*diff)
            dfda = 2.0*INVERSE_PI*gamma*invDen1
            out.set(i,0, dfda)

            invDen2 =  1/(diff*diff + halfGamma*halfGamma)
            dfdxo = amplitude*INVERSE_PI*gamma*diff*invDen2*invDen2
            out.set(i,1, dfdxo);

            dfdg = -2.0*amplitude*INVERSE_PI*(gamma*gamma - 4.0*diff*diff)*invDen1*invDen1
            out.set(i,2, dfdg)


# Register with Mantid
FunctionFactory.subscribe(LorentzWithDeriv)

