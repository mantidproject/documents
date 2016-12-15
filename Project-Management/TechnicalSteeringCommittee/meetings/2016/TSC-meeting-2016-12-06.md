Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?

New Items
---------
* gsl2 status - open issues: [#16680](https://github.com/mantidproject/mantid/issues/16680)
* Bundling of python on osx
* Migration to C++17 Filesystem library? Is `boost::filesystem` a useful stepping stone?
* Update on plotting evaluation
* Update on [Mantid 4](https://github.com/mantidproject/documents/pull/23)
* Update on installing 3rd party projects (e.g. [mslice](https://github.com/mantidproject/mslice), [FastGR](https://github.com/neutrons/FastGR), and [PyVDrive](https://github.com/neutrons/PyVDrive)) that require mantid

Minutes
-------
Attendees: Draper, Gigg, Heybrock, Bush, Campbell, Peterson, Whitfield, Savici, Hahn

* Inform the dev list future code should use `boost::filesystem` in C++ (Pete)
* Mantid 3.9 will bundle python on osx. This can be moved to the next release if time does not allow. (Steve, Gagik, Samuel)
* gsl2 works on linux (ignoring sporadic test failures). osx has one remaining [#17778](https://github.com/mantidproject/mantid/issues/17778)
* 3rd party projects should install via `setup.py`. Installation/validation is still being understood.
* Mantid4/new plotting
  * plans will be presented to the PMB on Dec 15 by Nick
  * TSC prefers the option of writing a new workbench from scratch
