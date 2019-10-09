Agenda
======

Pinned Topics
-------------
* Review any outstanding external [pull request](https://github.com/mantidproject/mantid/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+-label%3A%22State%3A+In+Progress%22) or [issues](https://github.com/mantidproject/mantid/issues)?
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?
* Find volunteer for presentation at next mantid review meeting

New Items
---------
* RHEL7/workbench/qt5/python3
* [Status of new workbench](https://github.com/mantidproject/mantid/projects/9)
* [Status of SliceViewer replacement](https://github.com/mantidproject/mantid/projects/19)
* WTF are [all these Jenkins jobs](https://builds.mantidproject.org/view/All/)?
* Do we *really* want CI on Draft PRs?
* Thread scheduling issues
* Documentation screenshots
* Dependency management/packaging update/options
* Static link everything we can?

Minutes
-------
Attendees: Draper, Gigg, Hahn, Nixon, Peterson, Savici

* We will rebuild `python-qt5` as `python2-qt5`, then rebuild `mantid40` and `mantid41`. These will need to be released simultaneously.
* The TSC desires for v4.2 to be the last that supports python2. Some research needs to be done with regards to qt4/SIP. Also requires rebuilding a version of matplotlib for RHEL
* It was observed that the main thing holding back adoption of `mantidworkbench` is missing features in the sliceviewer
* TSC discussed dependency management and identified requirements for a replacement system (not system packages):
  * Required: being able to control dependencies independent of the system
  * Required: being able to have a single system for all linuxes, single for osx, single for windows
  * Required: being able to allow users to mix-in python packages (e.g. pandas) with mantid
  * Desired: being able to build a system install of mantid
