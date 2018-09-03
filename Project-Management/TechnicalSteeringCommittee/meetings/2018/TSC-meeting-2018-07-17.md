Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Lamar)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?
* Find volunteer for presentation at next mantid review meeting

New Items
---------
* Status of [release](http://developer.mantidproject.org/ReleaseChecklist.html) and [maintenance tasks](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/MaintenanceTasks.md)
* OSX dependencies discussion
  * Homebrew does not allow setting the deployment target -> can only build for macOS version you have
  * Apple hardware does not allow installing previous versions of macOS on newer hardware
  * Potentially risky situation if hardware fails that we can't support the version of macOS that we need
  * Ideas:
    * is macports/fink an option? - it allows setting the deployment target as a configuration option
    * take the same approach as Windows and build libraries - time consuming, hard to update things
    * linux `clang` on pull requests and osx nightly
* Status of new workbench on RHEL7
* Status of SliceViewer replacement (Hahn)
* [An issue with distributions and dimensionless units](https://github.com/mantidproject/documents/blob/fix-divide-distribution/Design/DistributionsAndDimensionlessData.md) and [Multiplication and division rules for histograms](https://github.com/mantidproject/documents/pull/25)
* Update on move to clang-format `v5.0`

Minutes
-------

Attendees: Gigg, Hahn, Moore, Peterson, Savici, Vardanyan, Whitfield

* The release is going as expected with no large issues
* Ubuntu 18.04 packages currently have an issue with library path that prevents supporting it. Hahn is investigating and will report finding to the TSC tomorrow.
* Maintenance is progressing. Notable items are:
  * `clang-format` v5 was pushed back to after the release. TSC members were reminded to look for people working on issue for a future patch release which will have to be branched from `release-next` since code conflicts will likely make `git cherry-pick` difficult.
  * For C++14: MSVS17 should be ready shortly after the release, `devtoolset-7` on RHEL7 appears to be ready already.
  * Peterson is currently working on automatically building the developer website.
* The OSX topic was pushed to the next meeting. Whitfield was going to investigate building with clang on linux to see if it is a possible option for replacing OSX on pull requests
* Effort is going to be devoted to the new workbench once the release is done.
