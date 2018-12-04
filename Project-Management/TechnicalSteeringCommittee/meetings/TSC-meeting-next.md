Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues?
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?
* Find volunteer for presentation at next mantid review meeting

New Items
---------
* Linux builds / [Xvfb](https://github.com/mantidproject/mantid/pull/24057) / [docker](https://github.com/mantidproject/dockerfiles)
* `MDEventWorkspace` speedup / design based on prototype Dan Nixon presented at NOBUGS:
  - [Design document](https://github.com/mantidproject/documents/blob/008e06f2d98622285e63abe541b75cc674fa58df/Design/MDWorkspace/MDSpaceDesign.md)
  - Final proposed solution does not actually require API changes, just an option in algorithms.
* [Dataset design document](https://github.com/mantidproject/dataset/pull/2) discussion.
* Status of move to C++14 - MSVS
* [Status of new workbench](https://github.com/mantidproject/mantid/projects/9)
* Status of SliceViewer replacement (Hahn)
* add scikit-image as a Mantid dependency?

Minutes
-------
Attendees: Whitfield, Hahn, Savici, Peterson, Heybrock, Gigg, Nixon, Arnold, Draper

* Linux builds have moved to using Xvfb already
* Setting up to use docker images for builds is not trivial. Dan will investigate options.
* Dan will work on moving from leroy to pipeline builds
* Change to `MDEventWorkspace` design was approved and work is starting
* MSVS upgrade is the primary maintenance task. Martyn is working on upgrading build servers "soon"
