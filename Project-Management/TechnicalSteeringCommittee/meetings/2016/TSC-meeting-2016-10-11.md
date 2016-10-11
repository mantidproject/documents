Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)? (Fede)

New Items
---------
* External GUI(s)
  [Ansto Proposed Example](https://github.com/mantidproject/documents/blob/master/Design/ANSTO_SANS/AnstoSans.pdf). How
  do we recommend we do them. Needed for no-bugs week. (Owen & Anton)
* Installing 3rd party projects
  (e.g. [mslice](https://github.com/mantidproject/mslice),
  [FastGR](https://github.com/neutrons/FastGR), and
  [PyVDrive](https://github.com/neutrons/PyVDrive)) that require
  mantid
* Move from 14.04 to 16.04
* Move "main" builds from rhel6 to rhel7
* Move from pylint to flake8
* gsl2 status - open issues:
  [#16680](https://github.com/mantidproject/mantid/issues/16680)

Minutes
-------

Attendees: Arnold, Bush, Draper, Gigg, Hahn, Heybrock, Peterson,
Savici, Whitfield

* External GUI(s):
  * They should create a proper python project with a `setup.py` for
    installing and require the appropriate version of mantid.
  * Arnold will start a document to hold instructions on how to create
    an external project that uses mantid and can have links to
    projects that we know about.
* We can move most build machines from ubuntu 14.04 to 16.04. However,
  ILL uses ubuntu 14.04 as their main platform at the facility so
  mantid will need to continue supporting it.
* The only thing left to move from rhel6 to rhel7 is valgrind builds.
* gsl2 status:
  [`CurveFittingTest_DiffRotDiscreteCircleTest` has an issue with gsl2 on osx](https://github.com/mantidproject/mantid/issues/17778). Otherwise
  this work is considered done.
