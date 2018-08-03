# PyVDrive

## What is PyVDrive

* [PyVDrive Repository](http://docs.mantidproject.org/nightly/algorithms/Fit-v1.html)
* User are used to the IDL-based VDRIVE

### PyVDrive and Mantid

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
 
### What PyVDrive shall do

* Be able to fit all the peaks present FindPeaks can fit,

  * i.e., replace peak fitting in FindPeaks

* Easy to set up

* Be able to tackle the complicated use cases

* More on non-functional requirements

  * Output fitted data
  * Detailed list of fitted parameters' value
  * and etc.
  
### Non-functional requirement: Speed

Users need to see the result quickly
  
## Features

### Slice data

### Batch process

Find out the correct starting value of all the peak profile parameters for [Fit](http://docs.mantidproject.org/nightly/algorithms/Fit-v1.html) to fit the function usually by Levenberg-Markardt.

### Live-view

FitPeaks is taking care of starting value of peak parameters for multiple peaks in multiple spectra.

<img src="group.PNG" width=270 height=200/>

## Next step

* Replace peak fitting algorithm in FindPeaks
* Replace peak fitting algorithm in StripPeaks and thus StripVanadiumPeaks
* Refactor the single peak fitting part in FitPeaks to FitPeak, while remove original FitPeak
  



