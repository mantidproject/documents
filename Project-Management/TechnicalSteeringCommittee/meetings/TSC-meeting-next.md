Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)? (Fede)

New Items
---------
* Patch releases [v3.5.2](https://github.com/mantidproject/mantid/commits/release-3.5) and [v3.6.1](https://github.com/mantidproject/mantid/commits/release-v3.6)
* [Poco 1.6](/Project-Management/TechnicalSteeringCommittee/reports/Poco_14_to_16.md)
* Guidelines for using hdf5 and h5py vs nexus and nexus-python?
* Start made on Geometry requrements [here](/Design/Instrument-2.0/requirements-v2.md) (Owen)
* Tracking of volatile unit tests (Owen)
* [LiveListener Design](https://github.com/mantidproject/documents/pull/7)(Owen)
* Should we add `gtest` (google-test) support to Mantid?
* [Index Abstraction Design](https://github.com/mantidproject/documents/pull/13) (Simon)
* [Histogram Design](https://github.com/mantidproject/documents/pull/14) (Simon)
* Plan to remove Qt3Support module?
  * add [`add_definitions(-DQT3_SUPPORT_WARNINGS)`](https://gist.github.com/quantumsteve/a3d0733cd3ea31452ed0) to the build?   

Minutes
-------
* After 3.6.1 is out (later this week) move rhel7 build to poco 1.6
* TSC recommends hdf5/h5py for all future work. nexus-python dependency will be removed and h5py will be added
* Steve will add maintenance task to take care of QT3 warnings. There will be a build in critical tab of jenkins to help stop people from adding more QT3 to mantid
