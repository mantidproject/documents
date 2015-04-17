Agenda
======

* Build server jobs and such:
 * What belongs on the [Critical Jobs](http://builds.mantidproject.org/) tab?
* Moving to a newer gcc on RHEL6. Decide on who should do the changes (Martyn)
* Change default logging stream to `std::cout` rather than `std::clog` (which is basically `std:cerr`) (Martyn)
* Review of [skipped system tests](http://developer.mantidproject.org/systemtests/)
* Continue discussion from last TSC on [python api for MDEvents](https://github.com/mantidproject/documents/blob/master/Design/pythonAlgorithmsForMDEvents.rst) (Andrei)
 * A way to do this would be to find a way to get user-defined functions looping over the MDEvent data. How do Numpy do this? (Owen)
* [Design proposal](https://github.com/mantidproject/documents/blob/master/Design/HandlingMovingInstruments.md) for handling of data from moving instruments (Anders) 
* [MDWorkspace enhancement proposal](https://github.com/mantidproject/documents/blob/master/Design/VATES/IMDDimensionUpdate.md) (Owen)
* Plan for moving to Github Issues (Stuart)
