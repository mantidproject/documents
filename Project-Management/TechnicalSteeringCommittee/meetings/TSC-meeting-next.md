Agenda
======

Pinned Topics
-------------
* Review any outstanding external [pull request](https://github.com/mantidproject/mantid/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+-label%3A%22State%3A+In+Progress%22) or [issues](https://github.com/mantidproject/mantid/issues)?
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?
* Find volunteer for presentation at next mantid review meeting

New Items
---------
* RHEL7/workbench/qt5/python3 status
* [Release status](https://github.com/mantidproject/mantid/milestone/71)
* [Maintenance tasks](https://github.com/mantidproject/mantid/projects/15)
* [Status of new workbench](https://github.com/mantidproject/mantid/projects/9)
* [Status of SliceViewer replacement](https://github.com/mantidproject/mantid/projects/19)
* Rewrite graphical parts of instrument view
* Should clean up [all these Jenkins jobs](https://builds.mantidproject.org/view/All/)?
* Do we *really* want CI on Draft PRs?
* Documentation screenshots
* Static link everything we can?
* Thread scheduling issues

Minutes
-------
Attendees: Draper, Gigg, Heybrock, Peterson, Hahn, Savici, Gagik
* RHEL7 python-qt5 packages have been rebuilt. Rebuilding mantid v4.0 and v4.1
* Planning on mantid v4.2 being the last one to support python2 - Nick will add this to the release notes
* Reviewed release - only one week of beta testing left
* Reviewed maintenance tasks - main themes this time:
  * python2/3 compatibility everywhere in preparation of python3 only v4.3
  * move to C++17
