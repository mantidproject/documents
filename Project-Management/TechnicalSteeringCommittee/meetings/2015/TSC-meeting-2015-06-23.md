Agenda
======

* Review any outstanding external pull request or issues? (Owen)
* Any status updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)? 
* Summary of moving to gtest (Pete)
* Give brief summary of use cases collected in [HandlingMovingInstrument](/Design/HandlingMovingInstruments.md) (anders)
* Pros and cons of having `clang-format` provide [automatic reporting](http://builds.mantidproject.org/view/All/job/master_clang-format/) (Ross)
* Use tcmalloc on Windows: v3.4 supports releasing memory back to the OS. Initial tests suggest much better performance for large workspaces, e.g. faster non-blocking delete (Martyn)
* With ref to [minutes](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/meetings/2015/TSC-meeting-2015-01-29.md) - transition to VS 2013 or VS 2015
* [Signing mac executable](http://certhelp.ksoftware.net/support/articles/18835-how-do-i-sign-files-on-mac-osx-) 
* Downstream jobs for PR builds. Or can we otherwise speed things up. Request from Nick D.
* Outstanding issues for metrics reporting (Stuart)
* Linode Server - Expires End of Year (Stuart)


Minutes
=======

Present: Pete, Ross, Owen, Martyn and Anders

* No external pull request and no external issues
* [IMDDimensionUpdate](/Design/VATES/IMDDimensionUpdate.md) approved, and has been updated with comments
* Could move to newer cxxtest version - not clear what the benefit of this would be. ExternalProject for gest and cxxtest would get rid of external code in repository. gtest does not have enough additional benefit compare to cxxtest. Perhaps take this up at next joint meeting
* Different versions of clang-format give different results. Run clang-format after merge on master. Look into this further. clang-format 3.6 on ubunto. 
* tcmalloc - problem deleting large event workspaces. Make some further tests around Python (Martyn)
* Waiting for community edition of VS 2015 to be released summer 2015 (https://github.com/mantidproject/documents/blob/master/Design/VisualStudio-2015.md)
* Nuget windows package managemer demoed and seems potential good
