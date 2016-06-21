Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)? (Fede)

New Items
---------
* [Anaconda](https://github.com/mantidproject/documents/blob/master/Design/Anaconda.md) (Jiao)
* [HistogramData module](https://github.com/mantidproject/mantid/pull/16627) needs code review (Simon).
* [Maintenance Tasks](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/MaintenanceTasks.md)

Minutes
-------
* Everybody will individually look at the histogram PR and comment
* Mantid no longer directly depends on Qt3. Qwt5 and Qwtplot3d do. We need a plan on how to move from these dead project to something else.
* Python3 compatibility "works" and has a build on the critical tab to see that it continues to build (not running any tests). Python algorithms have not been given compatibility yet.
* Python2 will be the default for mantid 3.8. Around the release we'll package a "tech preview" with python3.
* Mantid now builds against gsl2, but there are 3 unit tests, 1 doc test, and 9 system tests still fail. There isn't currently someone working on this. This is required for ubuntu 16.04. Fede will create tickets for the broken ISIS tests, Pete for the broken SNS tests.
* Mantid unit tests (cxxtestgen) doesn't compile under gcc 6. This is an issue for fedora24. Stuart will briefly look at moving to newer cxxtestgen.
* Jiao will create a pull request for enabling anaconda builds, and create a conda mantid channel.
