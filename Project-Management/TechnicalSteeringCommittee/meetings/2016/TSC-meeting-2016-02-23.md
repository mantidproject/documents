Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)? (Fede)

New Items
---------
* [Pull request template](https://github.com/mantidproject/mantid/pull/15406)
* Update on [Maintenence tasks](/Project-Management/TechnicalSteeringCommittee/reports/MaintenanceTasks.md)
* Are we supporting Ubuntu 16.04 for Mantid `3.7`? Need to fix [problems](http://builds.mantidproject.org/job/master_clean-ubuntu-16.04) with gsl 2.
* Second pass on "big" TSC items from dev workshop for PMB to prioritize ([1](/Project-Management/TechnicalSteeringCommittee/reports/DevMeetingItems-2016.md), [2](https://github.com/mantidproject/documents/blob/master/Project-Management/SSC%20%26%20Strategy%20Collated%20requirements.xlsx), [3](https://github.com/mantidproject/documents/blob/master/Project-Management/SSC%20%26%20Strategy%20Task%20list.xlsx))
* QA - Test documents/scripts within the codebase. It's potluck whether the unscripted test process find issues before a release. Should we have a QA section of the repository containing documents (markdown or rst) on how to test specific features? These would then have to be run through before we even go to beta testing (Martyn)

Minutes
-------
In attendance: Campbell, Draper, Gigg, Hahn, Heybrock, Peterson, Pouzols, Savici, Wedel, Whitfield

* Martyn will move the 3.6 release notes over to sphinx to see how they would work in the main repository.
* New pull request template was approved. Martyn will merge it in.
* Ross will write an [issue](https://github.com/mantidproject/mantid/issues/15421) for Roman to figure out the gsl 2 build errors.
* TSC should go over the time estimate spreadsheet by COB on Feb 24.
* Martyn will start a design document for how to do "unscripted testing"
