Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Lamar)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?

New Items
---------
* Status of new workbench on RHEL7 (Peterson)
* SliceViewer replacement (Hahn)
* Update on move to clang-format `v5.0` [#22417](https://github.com/mantidproject/mantid/pull/22417)

Minutes
-------
Attendees: Bush, Draper, Gigg, Hahn, Peterson, Ross, Savici, Soininen, Vardanyan

* Progress is being made on getting devtoolset-7 on RHEL7
* New workbench update
  * RHEL7 needs rebuilds of some dependencies
  * Pete is backporting things from f27 (`sip`, `python-qt5`, and `PyQt4` so far)
* SliceViewer replacement
  * First proof of concept is to create a variant of SpectrumViewer
  * Group wants to start working on a formal design
  * Open question on matplotlib 2D rendering performance - can be solved with resampling and listing to zoom events
  * Need to sort out sequencing of additional features
* clang-format v5 creates issues in reordering the headers. Further exploration is required to solve the issue.
