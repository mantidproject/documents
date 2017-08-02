Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?

New Items
---------
- [Workbench Design](https://github.com/mantidproject/documents/pull/49) has superseded [External Python Interfaces](https://github.com/mantidproject/documents/pull/40). I would like to include `mslice` as an external project in the current codebase so we can ship it with MantidPlot. The new workbench will include the improved design for external interfaces. 
- [WorkspacePropertyWithIndex Design](https://github.com/mantidproject/documents/pull/42)
- [Tomography GUI Design (in python)](https://github.com/mantidproject/documents/pull/43)
- All spectra in a workspace need the same number of bins

Minutes
-------
Attendees: Gigg, Heybrock, Bilheux, Savici, Peterson, Whitfield, Hahn

- Nominally approve the new workbench design pending minor changes
  - Fix outstanding pylint warnings before increasing what pylint checks for
  - Should move as much as possible (everything except SliceViewer and SpectrumViewer) to matplotlib instead of making Qwt5/Qwt6 compatible
  - Investigate and estimate effort for adding compatibility to SliceViewer and SpectrumViewer
  
