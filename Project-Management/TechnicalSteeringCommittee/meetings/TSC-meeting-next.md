Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Lamar)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?

New Items
---------
* Ubuntu support (14.04, 16.04, 18.04)
* Fedora 28 support?
  * missing dependencies on copr
* OSX support (which versions)
* [An issue with distributions and dimensionless units](https://github.com/mantidproject/documents/blob/fix-divide-distribution/Design/DistributionsAndDimensionlessData.md) and [Multiplication and division rules for histograms](https://github.com/mantidproject/documents/pull/25)

Minutes
-------
Attendees: Anti, Lamar, Martyn, Savici, Peterson, Whitfield, Hahn

* Dropping support for 14.04 and adding support for 18.04
  * 18.04 currently runs out of memory on doc tests. Needs to be figured out.
* clang-format will move to v5
  * Martyn will update ubuntu developer packages
  * Lamar will update the [build script](https://github.com/mantidproject/mantid/blob/master/buildconfig/Jenkins/clangformat) and will reformat the codebase
  * Pete will email the dev list about the change
* Pete will rebuild `mantid-developer` on copr for fc28
* Mantid 3.13 will be the last release to support osx 10.10. After that, the minimum version required will be osx 10.13
* Developer site update
  * Pete will fix build
  * Martyn will add server side redirects
