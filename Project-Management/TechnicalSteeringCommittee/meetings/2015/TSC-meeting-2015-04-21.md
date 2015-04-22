Agenda
======

* Review any outstanding external pull request
* Continue discussion from last TSC on [python api for MDEvents](https://github.com/mantidproject/documents/blob/master/Design/pythonAlgorithmsForMDEvents.rst) (Andrei)
 * A way to do this would be to find a way to get user-defined functions looping over the MDEvent data. How do Numpy do this? (Owen)
* [Design proposal](https://github.com/mantidproject/documents/blob/master/Design/HandlingMovingInstruments.md) for handling of data from moving instruments (Anders)
* [MDWorkspace enhancement proposal](https://github.com/mantidproject/documents/blob/master/Design/VATES/IMDDimensionUpdate.md) (Owen)
* Build server jobs and such:
 * What belongs on the [Critical Jobs](http://builds.mantidproject.org/) tab?
* Moving to a newer gcc on RHEL6. Decide on who should do the changes (Martyn)
* Change default logging stream to `std::cout` rather than `std::clog` (which is basically `std:cerr`) (Martyn)
* Review of [skipped system tests](http://developer.mantidproject.org/systemtests/)
* Plan for moving to Github Issues (Stuart)
* Should [labels](https://github.com/mantidproject/mantid/labels) on github conform to a naming standard (i.e. spaces, pascalcase....)?
* 

Minutes
=======
Present: Pete, Ross, Stuart, Andrei, Anders, Martyn and Owen 

* Action: [Python api for MDEvents](https://github.com/mantidproject/documents/blob/master/Design/pythonAlgorithmsForMDEvents.rst) will be updated to show the options discussed for this design,  and it was agreed the first objective will be to introduce and expose read-only iterators for MDEvents in MDEventWorkspaces. When design document has been updated move it from 'in progress' to 'approved' in [here](https://github.com/mantidproject/documents/edit/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md). (Andrei)
* Action: [Design proposal](https://github.com/mantidproject/documents/blob/master/Design/HandlingMovingInstruments.md) has not been discussed. It will to be updated and re-circulated to the developer list before the next TSC meeting. (Anders)
* Action: [MDWorkspace enhancement proposal](https://github.com/mantidproject/documents/blob/master/Design/VATES/IMDDimensionUpdate.md) will be updated following feed back from the TSC and then circulated on the developer list in the next week. (Owen)
* Action: All develop jobs will be removed from jenkins (Martyn)
