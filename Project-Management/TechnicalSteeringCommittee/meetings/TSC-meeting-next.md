Agenda
======

* Bundle Paraview 4.3 with Mantid (OSX Steve, Martyn/Owen Windows)
* Build server script updates for bundled ParaView (Owen)
* Summarize experience from switching to [leeroy](https://github.com/jfrazelle/leeroy) (Ross)
* Build server jobs and such:
 * Currently on every PR: cppcheck, OSX, RHEL6, RHEL7 (with system tests), Ubuntu, Windows (with usage tests)
 * Should we add pylint or doxygen?
 * What belongs on the [Critical Jobs](http://builds.mantidproject.org/) tab?
* TSC actions from last [PMB minutes](https://github.com/mantidproject/documents/blob/master/Project-Management/PMB/Minutes/PMBMinutes29thJan15.docx) 
 * Create a user example for how to integrate non-Mantid code with Mantid
 * Determine what code in Mantid needs validation by scientific expert
* Moving to a newer gcc on RHEL6. Decide on who should do the changes (Martyn)
* Change default logging stream to `std::cout` rather than `std::clog` (which is basically `std:cerr`) (Martyn)
* Review of [skipped system tests](http://developer.mantidproject.org/systemtests/)
* Continue discussion from last TSC on [python api for MDEvents](https://github.com/mantidproject/documents/blob/master/Design/pythonAlgorithmsForMDEvents.rst) (Andrei)
 * A way to do this would be to find a way to get user-defined functions looping over the MDEvent data. How do Numpy do this? (Owen)
* [Design proposal](https://github.com/mantidproject/documents/blob/master/Design/HandlingMovingInstruments.md) for handling of data from moving instruments (Anders) 

Minutes
=======

* Paraview 4.3 branch bundling has been done, but problem with functionality. 
* Build server script updates for bundled ParaView. Not high priority. Uncertain resource requirement.  
