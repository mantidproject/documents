Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)? 

New Items
---------

* Review and assign [maintenance tasks](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/MaintenanceTasks.md)
* Consider dropping the matrix jobs for the clean builds etc in favour of separate jobs as is done with pull requests. Motivation is that a failed job in the config stops the whole thing and the matrix rebuild plugin doesn't play well with downstream projects and artifacts. We could still use the MultiJob plugin, as the [Valgrind job](http://builds.mantidproject.org/view/Valgrind/job/valgrind_plugin_packages/) for the plugins does to group them together for display.  (Martyn) 

Minutes
-------

* Agreed to separate matrix jobs on Jenkins out to jobs per configuration to avoid rebuilding all configurations when one fails.
* Pete discussed annual developer/SSC meeting with PM. Tentative dates: 18th-29th January.
