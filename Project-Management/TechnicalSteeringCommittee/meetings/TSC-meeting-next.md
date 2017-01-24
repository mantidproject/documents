Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?

New Items
---------
* Discussion about [splitting TimeSeriesProperty] (https://github.com/mantidproject/documents/blob/master/Design/EventFiltering/SplitTimeSeriesProperty.md)
* [Maintenance tasks](../reports/MaintenanceTasks.md)
* Add a [python3](http://builds.mantidproject.org/job/python3/) build to pull requests (Ross)
* Creating release branch
* Editing release notes

Minutes
-------

Attendees: Zhou, Whitfield, Peterson, Savici, Hahn, Bush, Draper, Arnold, Gigg

* python3 on ubutuntu 16.04 after [#18047](https://github.com/mantidproject/mantid/issues/18047) is fixed. It will build mantidplot and run the unit tests.
* Martyn will create the release branch once there are less open pull requests. Pete will merge the release branch onto `master` periodically once that is done.
* Nick and Andrei with edit the release notes.
* The `TimeSeriesProperty` design was approved, pending a name for the log that is created with a boolean log of times that are included in the workspace.
* The maintenance tasks were reviewed and it was decided that the top 3 priorities should be the main focus of the maintenance period.
