# Reflectometry IDF

## Motivation

The reflectometry instrument scientists do not currently use an IDF and are heavily reliant on their own scripts.
If the IDF could properly describe their setup then it would solve existing issues and improve their workflow.

Potential benefits include, but are not limited to:
  - Correct geometric description of detector components and calculation of angles to be fed into [algorithms](https://github.com/mantidproject/mantid/issues/26971)
  - Complex beam paths to allow for accurate description of mirror action, with a view to accurately describe the effect of gravity
  - Saving time by having multiple modes of configuration described within one file
  - Reduce known sources of error due to problems with Q error bars, incorrect angles, gravity corrections, etc.
  - Facilitate new equipment over multiple instruments/facilities, such as 2D detectors

## Solution

This task should be thought of in terms of four main sub-tasks:

  ### 1. POLREF IDF support for relative pixel map
  
  Andrew currently has a scan of the POLREF detector which he uses in a script to move each detector pixel into place every time 
  they run a reduction. This appears to be something which can be supported in an IDF by obtaining the relative pixel positions 
  from the scan and hard-coding them. The actual specular pixel position could then be obtained from the logs and used to do this 
  rotation into place from within the IDF.
  
  ### 2. Support multiple L-distances through a complex beam-path
  
  Current workarounds include the following:
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
