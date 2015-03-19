Agenda
======

* RHEL7 and fedora
* Pull request builder (Ross)
* [Design proposal](https://github.com/mantidproject/documents/blob/master/Design/HandlingMovingInstruments.md) for handling of data from moving instruments (Anders) 
* Owner of design proposal to feed in information from other developers, tsc meeting, etc? (Anders)
  * and email out developer list for feedback before bringing it to tsc?
* Moving to a newer gcc on RHEL6 (Martyn)
* Change default logging stream to `std::cout` rather than `std::clog` (which is basically `std:cerr`) (Martyn)
* What to do about [Paraview](/Design/Paraview43.md) (Pete)
* [Developer TSC wiki page added](http://www.mantidproject.org/Technical_Steering_Committee) any comments?

Minutes
=======

* RHEL7 to be used for system tests pending an initial trial. These will replace RHEL6 for the PR jobs if successful. Stuart/Ross.
* Design document for moving instruments to be moved to the next meeting. Anders will update the document and circulate it prior to the next meeting.
* All design documents should be circulated on the developer mailing list either before or after they have been presented to the TSC.
* ParaView 4.3 will be bundled with Mantid for the 3.4 release of Mantid.
 * Steve will lead this by creating a branch and get the packaging for OSX working
 * Martyn and Owen will create any fixes for the windows distribution on the same branch. 
* Ross is to investigate using [leeroy](https://github.com/litl/leeroy) as a replacement and report progress at the next meeting.
 * We need to stress test this before swapping it in as a replacement for the current system.
