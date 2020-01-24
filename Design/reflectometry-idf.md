# Reflectometry IDF

## Motivation

The reflectometry instrument scientists do not currently use an IDF and are heavily reliant on their own scripts.
If the IDF could properly describe their setup then it would solve some existing issues and improve their workflow.

Existing problems that a design needs to address include:
  - An efficient way to describe the relative location of detector pixels, in relation to a 'specular pixel'
  - Mantid incorrectly calculating angles from IDF due to multiple bounce points and constraints on L-distances
  - Flexible description and use of multiple modes of configuration
  - Support for 2D detectors

Potential benefits include, but are not limited to:
  - Correct geometric description of detector components and calculation of angles to be fed into [algorithms](https://github.com/mantidproject/mantid/issues/26971)
  - Complex beam paths which allow for accurate description of mirror action, with a view to accurately describe the effect of gravity
  - Saving time by having multiple modes of configuration described within one file
  - Reduce known sources of error due to problems with Q error bars, incorrect angles, gravity corrections, etc.
  - Facilitate new equipment over multiple instruments/facilities, such as 2D detectors and triple-axis spectrometers

## Solution

This task should be thought of in terms of four main sub-tasks:

  ### 1. POLREF IDF support for relative pixel map
  
  As with other linear detectors, Mantid models the OSMOND detector pixels as regular and uniform, however in reality this is not the case. The reflectometry scientists 
  have a calibration scan of the detector, mapping each pixel to its relative angle, which could be used with an algorithm such as `ApplyCalibration` to correct the 
  simplified description. The relative nature of this pixel map means that summing errors in quadrature when calculating pixel offset could be greatly reduced to 
  include only the two pixels of interest, rather than every pixel in between as per standard Mantid workflow, resulting in uncertainty that would no longer be of the 
  same order of magnitude as the measured value. This also solves the issue that the detector is slightly curved, meaning small angle approximations are not necessary.
  Note that the calibration solution agreed upon for POLREF should be extended to work with [#4](#4. Facilitate the use of 2D detectors).
  
  The relative pixel map is currently used in a script to move each detector pixel into place every time the scientists run a reduction. This appears to be something 
  which could be supported as outlined above, using a similar solution to the SANS group with mask files. The scientists also use the concept of a 'specular pixel' which 
  is derived from the fact that positions are relative. This means that while their chosen specular pixel is pixel 280, any arbitrary pixel could be chosen by shifting 
  the position of every other pixel by the same offset.  The IDF would therefore represent a basic geometric description of the instrument before manipulation of the 
  precise pixel locations. The position of the specified specular pixel could then be obtained, say from the logs, and used to do this rotation into place from within the IDF.
  
  ### 2. Support multiple L-distances through a complex beam-path
  
  Current workarounds used by some other istruments include:
    - Separate 'neutronic' and 'physical instrument' IDFs
	- Dynamic modification of positions via `MoveInstrumentComponent`
	- Storage of the L1 & L2 distances in a separate table, which `ConvertUnits` can be made to 'understand'
	
  The ideal solution to this task would be to create a new `beam-path` tag for description within the IDF. This can then can be used 
  with Owen’s [Instrument 2.0 prototype](https://github.com/DMSC-Instrument-Data/instrument-prototype) which specifically deals with 
  the in-memory side of this task. He has mentioned that ray tracing will not be possible, and even with the prototype discussed above 
  only one flight path per component has been considered, so additional thought will need to be given to multiple flight paths as this 
  is required by the reflectometers in some configurations.
  
  >That is to say, that if you have a mirror, the prototype discussed does not treat different areas of the surface as yielding a 
  >different flight path (even though that is reality). There may also be wavelength dependence on the flight path to consider. 
  >The other thing to consider will be what precision of flight path is needed.
  
  ### 3. Describe multiple modes of configuration
  
  The instrument scientists would like to describe multiple modes of configuration (NR, PNR liquids, etc.) within a single IDF. 
  This will require a sensible way to describe multiple degrees of freedom and, if done accurately, will help in solving an issue they 
  are having with Q error bars and some other possible source of systematic error. It will also allow them to update their workflow in 
  real time as the report often having to change configurations with some users which ultimately takes a lot of time.
  
  A possible solution to this would be to have a generic IDF which can obtain the specified configuration through the log files delivered 
  by SECI, as is currently done in some IDFs. The IDF would then be able to update accordingly through a switch-statement of sorts, 
  moving the relevant components into place. No such log currently exists and so if this solution is decided upon it will require
  collaboration with the IBEX team.
  
  ### 4. Facilitate the use of 2D detectors
  
  Needs further investigation.
  Becky and Max have some data for 2D detectors, so we should talk to them regarding IDF support.

## Design

To be continued...
