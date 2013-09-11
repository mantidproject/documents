# Extending Mantid With Python: Exercise 4
#
# The aim of this exercise is to implement a peak fit function function to fit 
# the output data from exercise 3. For simplicity a solution file, 11001_deltaE.nxs
# is provided with the training data. 

from mantid.api import *
import numpy as np
import math

INVERSE_PI = 1.0/math.pi

class LorentzPeak(IPeakFunction):

    def init(self):
        # Tell Mantid about the 3 parameters that are involved in the function
        self.declareParameter("Amplitude",0.0)
        self.declareParameter("PeakCentre",0.0)
        self.declareParameter("Gamma",0.0)
        
    def functionLocal(self, xvals):
        # xvals is a 1D numpy array that contains the X values for the defined fitting range.
        half_gamma = 0.5*self.getParameterValue("Gamma")
        denom = (xvals - self.getParameterValue("PeakCentre"))**2 + half_gamma*half_gamma
        return self.getParameterValue("Amplitude")*INVERSE_PI*half_gamma/denom
        
    def functionDerivLocal(self, xvals, out):
        # xvals is a 1D numpy array that contains the X values for the defined fitting range.
        # out is a Jacobian matrix object. Mantid expects the partial deriviatives 
        # w.r.t the paramaters and x values to be stored here

        # Get the current parameter values
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

    def centre(self):
        # Return a guess at the centre
        return self.getParameterValue("PeakCentre")
 
    def height(self):
        # Return a guess at the height
        return self.getParameterValue("Amplitude") 
 
    def fwhm(self):
        # Return a guess at the FWHM
        return 2*self.getParameterValue("Gamma")
 
    def setCentre(self, new_centre):
        # Update centre guess when a new value is chosen from GUI
        self.setParameter("PeakCentre",new_centre)
 
    def setHeight(self, new_height):
        # Update Amplitude guess when a new height is chosen from GUI
        self.setParameter("Amplitude", new_height)
 
    def setFwhm(self, new_fwhm):
        # Update Gamma guess when a new width is chosen from GUI
        self.setParameter("Gamma",new_fwhm/2.0)
        
# Register function with Mantid
FunctionFactory.subscribe(LorentzPeak)
