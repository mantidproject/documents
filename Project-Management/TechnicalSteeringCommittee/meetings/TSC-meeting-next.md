Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?

New Items
---------
* Ubuntu 14.04 build servers
* gsl2 status - open issues: [#16680](https://github.com/mantidproject/mantid/issues/16680)
* Bundling of python on osx
* Migration to C++17 Filesystem library? Is `boost::filesystem` a useful stepping stone?
* Update on plotting evaluation
* Update on [Mantid 4](https://github.com/mantidproject/documents/pull/23)
* Update on installing 3rd party projects (e.g. [mslice](https://github.com/mantidproject/mslice), [FastGR](https://github.com/neutrons/FastGR), and [PyVDrive](https://github.com/neutrons/PyVDrive)) that require mantid

Minutes
-------
Attendees: Whitfield, Campbell, Savici, Peterson, Gigg, Heybrock, Bush

* Plotting evaluation: matplotlib appears to have what we need. 2d features have been confirmed via
  mslice. SliceViewer functionality for multi-dimensional plotting needs to be further studied.
* Need to start planning the migration of plotting to matplotlib.
* Two machines (one at ORNL, one at ESS) will remain on Ubuntu 14.04 running incremental and nightly. 
  Other Ubuntu machines will be moved to 16.04. Changes will happen on Friday.
