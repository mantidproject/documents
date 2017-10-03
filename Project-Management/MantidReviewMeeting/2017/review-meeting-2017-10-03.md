Agenda
======

* Add your links, etc. here

- Prefer using SimpleAPI over API for child algorithms. [link](https://github.com/mantidproject/documents/blob/master/Project-Management/ILL/NoteOnSimpleAPI.md). (PR [#20668](https://github.com/mantidproject/mantid/pull/20668))

Upcoming Instrument Changes 3.12
--------------------------------
* How does one [add](https://github.com/mantidproject/mantid/blob/master/Framework/Geometry/test/ParInstrumentTest.h#L36-L37) a detector to an `Instrument`?
* What is currently happening [here](https://github.com/mantidproject/mantid/blob/master/Framework/Geometry/src/Instrument.cpp#L714-L716)?
* What currently happens if the ID is duplicated?
* Offending IDFs now [fixed](https://github.com/mantidproject/mantid/issues/19553) as part of Mantid 3.11
* Upcoming [PR](https://github.com/mantidproject/mantid/pull/20686) **prevents the creating of corrupt `Instrument` objects**, a necessary change for `Instrument 2.0`. If your IDF contains duplicates, you will not be able to load the instrument.

Questions
=========
