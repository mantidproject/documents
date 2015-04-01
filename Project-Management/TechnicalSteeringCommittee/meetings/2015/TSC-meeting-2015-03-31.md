Agenda
======

* Bundle Paraview 4.3 with Mantid (OSX Steve, Martyn/Owen Windows)
* Investigations using [leeroy](https://github.com/jfrazelle/leeroy) (Ross)
* Revisit [python api for MDEvents](https://github.com/mantidproject/documents/blob/master/Design/pythonAlgorithmsForMDEvents.rst) (Andrei)
* Moving to a newer gcc on RHEL6. Decide on who should do the changes (Martyn)
* Change default logging stream to `std::cout` rather than `std::clog` (which is basically `std:cerr`) (Martyn)
* Review of [skipped system tests](http://developer.mantidproject.org/systemtests/)
* [Design proposal](https://github.com/mantidproject/documents/blob/master/Design/HandlingMovingInstruments.md) for handling of data from moving instruments (Anders) 

Minutes
=======

Present: Pete, Ross, Stuart, Anders, Owen (and briefly Steven)

* Steven is working with Kitware regarding bundling ParaView 4.3 with Mantid. Steven will update Owen/Martyn when he's ready for us to start working on other platforms regarding this (Steven)
* We need to solve some issues with leeyroy but look to go ahead in making this our default build plugin (Ross)
  *  No restriction on who can kick-off builds, so we may want to review job permissions
  *  Automated build user documentation needs updating
  *  Need to warn developers that the switch is going ahead
  *  Would be best if we could get merge-builds master->feature_branch working. Currently only the feature branch is built.
* MDEvent python api does need improving as Andrei highlighted. 
  * A way to do this would be to find a way to get user-defined functions looping over the MDEvent data. How do Numpy do this? (Owen)
  * From the scripting enviroment, no knowlege of the MDBox structure should be necessary.
  * Adding C++ method for looping over MDEvents could replace double nested loops (over boxes and then over events in each) in C++
* In relation to changing the default for logging steam: Andrei mentioned the autoreduction at SNS currently relies on the logging stream being outputted to std::clog (i.e. std:cerr) 
* Last 4 agenda items moved to the next meeting
