Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)? (Fede)

New Items
---------

* gsl2 status - open issues: [#16679](https://github.com/mantidproject/mantid/issues/16679), [#16680](https://github.com/mantidproject/mantid/issues/16680), [#16681](https://github.com/mantidproject/mantid/issues/16681), [#16682](https://github.com/mantidproject/mantid/issues/16682), [#16683](https://github.com/mantidproject/mantid/issues/16683)/[PR#16714](https://github.com/mantidproject/mantid/pull/16714), [#16684](https://github.com/mantidproject/mantid/issues/16684),  
* Update on [Mantid 4](https://github.com/mantidproject/documents/pull/23)
* Update on plotting evaluation
* Bundling of python on osx
* Installing 3rd party projects (e.g. [mslice](https://github.com/mantidproject/mslice), [FastGR](https://github.com/neutrons/FastGR), and [PyVDrive](https://github.com/neutrons/PyVDrive)) that require mantid
* Migration to C++17 Filesystem library? Is `boost::filesystem` a useful stepping stone?

Minutes
-------

In attendance: Savici, Campbell, Zhou, Hahn, Whitfield, Peterson, Draper, Gigg, Bush, Heybrock, Wedel

* gsl2 - will not hold up the release. Ubuntu 16.04 will not be supported for 3.8.0. It will be supported in a patch release. Nick/Roman will go through the list of gsl2 issues and make sure they are assigned/correct.
* Plotting evaluation update
  * Consensus was that matplotlib is the library to switch to
  * Next round of evaluation will be done during the maintenance cycle to validate this choice
