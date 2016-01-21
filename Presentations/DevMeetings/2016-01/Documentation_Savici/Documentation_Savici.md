# Organize algorithms and documentaion
---
# 1. Questions that one might ask:

* What is Mantid? How do I start?
* What does this thing do?
* What algorithm should I use? Why?

---
# 2. What is Mantid? How do I start?

* We have some tutorials, but it might not be relevant to most users

--

* Should create a "Starting with Mantid" that should tell the users 

  - what is the difference between MantidPlot and the Framework

--

  - quick description of what a workspace is, what it contains

--

  - talk about user interfaces (should be links to technique specific ones)

--

  - point to tutorials for python in Mantid, MantidPlot, etc

--

  - Very important: where can I find more help?

---
# 3. What does this thing do?

* We have over 750 Algorithms, plus fit functions, concepts, user interfaces 
* Make sure the names reflect what the algoritm does
* Make sure to spell out limitrations
* Relevant physics - links to papers, write down formulas, etc. (this is very uneven)

---
# 4. What algorithm should I use? Why?

* With so many algorithms, users are easily turned off by Mantid
* We should have technique specific, very detailed step by step description of the physics and links to the relevant algorithms
---
# 5. Example: I want to do an inelastic experiment on HYSPEC

* What is my original data look like? - events (TOF, wall clock time, weights, errors)
* What is the final goal? - S(H,K,L,w) on a regular grid
* Filter bad events - low proton charge, wrong temperature
* Look at the instrument view, see bad detectors, mask them
* Transform events from TOF to w. Note that there are some corrections, since neutrons leave the moderators at to!=0
* Corrections about the detector efficiency (wavelength dependent or overall)
* Apply ki/kf
* Transform to HKL - UB matrix formalism, sample orientation, goniometer, find peaks, etc.
* Transform to MD
* Normalization and binning

---
# 6. Other documentation

* we should have advanced Mantid usages for instrument scientists
* this should include calibration, diagnostic of the instrument, etc.
 
