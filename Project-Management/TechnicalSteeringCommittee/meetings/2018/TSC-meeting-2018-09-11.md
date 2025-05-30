Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Lamar)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?
* Find volunteer for presentation at next mantid review meeting

New Items
---------
* Conda-forge uses GCC 4.8 (Lin), no C++14 support.
  * RHEL6 is already [End of Maintenance Support 1](https://access.redhat.com/support/policy/updates/errata/#exceptions)
  * It appears that conda-forge is moving to RHEL7 as the [linux-anvil2 Dockerfile](https://github.com/conda-forge/docker-images/blob/master/linux-anvil2/Dockerfile) suggests. This only moves gcc from 4.8.2 (with `devtoolset-2`) to 4.8.5 (with stock RHEL7)
  * [Migration to anaconda compilers?](https://github.com/mantidproject/conda-recipes/issues/26)
* [git hook](https://github.com/mantidproject/mantid/tree/master/.githooks) review ([suggestion on messages](https://chris.beams.io/posts/git-commit/))
* Changing how license is specified in headers ([abbreviations](https://spdx.org/licenses/) and [examples](https://spdx.org/sites/cpstandard/files/pages/files/using_spdx_license_list_short_identifiers.pdf))
* Status of move to C++14 - MSVS
* Status of new workbench
* Status of SliceViewer replacement (Hahn)
* Mac dependencies discussion
  * Homebrew does not allow setting the deployment target -> can only build for macOS version you have
  * Apple hardware does not allow installing previous versions of macOS on newer hardware
  * Potentially risky situation if hardware fails that we can't support the version of macOS that we need
  * Ideas:
    * is macports/fink an option? - it allows setting the deployment target as a configuration option
    * take the same approach as Windows and build libraries - time consuming, hard to update things
    * linux `clang` on pull requests and osx nightly
* [An issue with distributions and dimensionless units](https://github.com/mantidproject/documents/blob/fix-divide-distribution/Design/DistributionsAndDimensionlessData.md) and [Multiplication and division rules for histograms](https://github.com/mantidproject/documents/pull/25)

Minutes
-------
Attendees: Draper, Hahn, Lin, Moore, Peterson, Savici, Whitfield

* conda - Lin will continue trying to use the newer ananconda gcc with and extra `cmake` directive to use the old string interface.
* Draper will work on [changing license/copyright](https://github.com/mantidproject/mantid/issues/23488) in source files
* MSVS is still waiting on a bugfix from the compiler
* The new workbench has not made reportable progress
* Hahn is working on a new pcolormesh which will only supply enough points for the screen resolution
