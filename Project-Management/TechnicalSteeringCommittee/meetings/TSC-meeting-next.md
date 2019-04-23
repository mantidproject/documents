Agenda
======

Pinned Topics
-------------
* Review any outstanding external [pull request](https://github.com/mantidproject/mantid/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+-label%3A%22State%3A+In+Progress%22) or [issues](https://github.com/mantidproject/mantid/issues)?
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?
* Find volunteer for presentation at next mantid review meeting

New Items
---------
* [Status of new workbench](https://github.com/mantidproject/mantid/projects/9)
* [Status of SliceViewer replacement](https://github.com/mantidproject/mantid/projects/19)
* Framework only build on PR's (Pete)

Minutes
-------
Attendees: Gagik, Draper, Gigg, Hahn, Peterson, Savici, Whitfield

* Will likely schedule push to get open PRs to zero at the "end of the month" (i.e. next week) for two days
* Workbench is continuing to progress, but the "big push" is slowing down. People should help with issues in the [next](https://github.com/mantidproject/mantid/projects/9) column of the project board
* Sliceviewer
  * Main application has a prototype that should be ready for developers next week
  * Currently is designed around MDHisto. MDEvent should be straightforward to add
  * Separate work is occuring for faster rendering of MatrixWorkspace
  * All of the 2d plots should use `imshow`
