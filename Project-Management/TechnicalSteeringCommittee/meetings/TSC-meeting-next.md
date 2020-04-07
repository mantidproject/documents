Agenda
======

Pinned Topics
-------------
* Review any outstanding external [pull request](https://github.com/mantidproject/mantid/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+-label%3A%22State%3A+In+Progress%22) or [issues](https://github.com/mantidproject/mantid/issues)?
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?
* Find volunteer for presentation at next mantid review meeting

New Items
---------

* Completely seperate framework and several GUI components
* Add [mypy](http://mypy-lang.org/) to static analysis chain (Martyn)
* Start using the Git pre-commit hooks provided by https://pre-commit.com/. (Martyn)
  * Attempt to catch as many style/static-analysis errors before commit
  * Adding other hooks is fairly simple, e.g. [pre-commit-clang-format](https://github.com/martyngigg/pre-commit-clang-format)
* Raw data explorer widget in workbench (Gagik)
* Moving interfaces out of `scripts/`

Minutes
-------
Attendees: Draper, Gigg, Fairbrother, Hahn, Heybrock, Nixon, Peterson, Savici, Vardanyan

* Scheduled maintenance was mostly done. Exceptions are cppcheck did not get moved to 1.9.2, and not all python2 compatibility was removed yet
* Separating GUI
  * Needed for Framework only conda build
  * In `mantid.plots.__init__.py` python bindings
  * Keeps coming into system tests
  * opengl is hiding in rendering code inside `Framework`. Need an abstraction layer
* TSC agrees to add mypy to list of static analysis tools. Martyn will get it into the flake8 static analysis image for build servers
* Start with clang-format in pre-commit to see how that works for developers
* Begin a design of a super-plot like thing to add as a preview to the file browser
  * [example from ESS](https://github.com/nvaytet/visens)
  * need way to decide which preview to use from a given file
  * need way to see if the individual "previewer" can look at a file
  * Gagik will put together a design document
