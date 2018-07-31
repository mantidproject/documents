Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Lamar)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?
* Find volunteer for presentation at next mantid review meeting

New Items
---------
* Status of [maintenance tasks](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/MaintenanceTasks.md) ([release is done](https://github.com/mantidproject/mantid/releases))
* Unit/doc/system test should work at non ISIS facility (Savici)
* OSX dependencies discussion
  * Homebrew does not allow setting the deployment target -> can only build for macOS version you have
  * Apple hardware does not allow installing previous versions of macOS on newer hardware
  * Potentially risky situation if hardware fails that we can't support the version of macOS that we need
  * Ideas:
    * is macports/fink an option? - it allows setting the deployment target as a configuration option
    * take the same approach as Windows and build libraries - time consuming, hard to update things
    * linux `clang` on pull requests and osx nightly

* Status of move to C++14
* Status of new workbench on RHEL7
* Status of SliceViewer replacement (Hahn)
* Update on move to clang-format `v5.0`
* [An issue with distributions and dimensionless units](https://github.com/mantidproject/documents/blob/fix-divide-distribution/Design/DistributionsAndDimensionlessData.md) and [Multiplication and division rules for histograms](https://github.com/mantidproject/documents/pull/25)

Minutes
-------
Attendees: Savici, Peterson, Whitfield, Gigg, Draper, Moore, Heybrock
* Suggested mantid review meeting topic: engineering interface bake-off
