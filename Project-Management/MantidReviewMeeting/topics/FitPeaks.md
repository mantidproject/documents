# FitPeaks

## The algorithms to do peak fitting in Mantid

* [Fit](http://docs.mantidproject.org/nightly/algorithms/Fit-v1.html)
* [FitPeak](http://docs.mantidproject.org/nightly/algorithms/FitPeak-v1.html)
* [FindPeaks](http://docs.mantidproject.org/nightly/algorithms/FindPeaks-v1.html)
* MantidPlot fitting UI

### A brief history

* Long long time ago...
  * Fit
  * FindPeaks -- call Fit as a child algorithm
    * Finding peaks by fitting peaks in the given location;
    * Using Mariscotti algorithm to *observe* peaks; Fitting peaks that are *observed*
    
* Required to improve for
  * fitting some vanadium peaks
  * fitting for tens of thousands Gaussian peaks
  
* FindPeaks got more and more complicated and hard to read and improve
  * FitPeak was split from FindPeaks for better maintanence
  
* Eventually in 2017, it failed on several applications
  * Vulcan's diamond data
  * Powgen's low angle data
 
### What we want in FitPeaks

* Be able to fit all the peaks present FindPeaks can fit,

  * i.e., replace peak fitting in FindPeaks

* Easy to set up

* Be able to tackle the complicated use cases

* More on non-functional requirements

  * Output fitted data
  * Detailed list of fitted parameters' value
  * and etc.

## FitPeaks

### First place to look: [FitPeaks](http://docs.mantidproject.org/nightly/algorithms/FitPeaks-v1.html).

### Core algorithm

Find out the correct starting value of all the peak profile parameters for [Fit](http://docs.mantidproject.org/nightly/algorithms/Fit-v1.html) to fit the function usually by Levenberg-Markardt.

### Starting value of peak parameters

FitPeaks is taking care of starting value of peak parameters for multiple peaks in multiple spectra.

* Observable parameters: height, center, **width**
* Parameters hard to have valued guessed from observation:
  * Example: A, B and S from back to back exponential convoluted with Gaussian
  
#### Estimating peak width

 * Percentage of TOF or dSpacing (instrument resolution)
 * 2nd moment (only 1 peak in the fit window)
 * Using the neighboring peak's fitted width
 
#### In order to get a good starting value of peak width

 * Peak positions
 * Peak range or instrument resolution
 
## Next step

* Replace peak fitting algorithm in FindPeaks
* Replace peak fitting algorithm in StripPeaks and thus StripVanadiumPeaks
* Refactor the single peak fitting part in FitPeaks to FitPeak, while remove original FitPeak
  



