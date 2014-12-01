Agenda
======
* [Centralized Jenkins](http://198.74.56.37:8080/) update - the details
* [RHEL6 developer cost](http://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/RHEL6-issues.md)
* [Workspace history  proposal](http://github.com/mantidproject/documents/blob/master/Design/Nested%20History%20Detailed%20Design%20Document.docx)
* Next generation offline docs - using [QHelpEngine](http://qt-project.org/doc/qt-4.8/qthelp-framework.html#using-qhelpengine-api)
* Request from PMB to have version N and N-1 installed on linux machines.


Minutes
=======

Russell gave a run through of the current state of Jenkins on the Linode server.

* Request from PMB to have version N and N-1 installed on linux machines (the distros that are being used at the facilities).
** Stuart will start a document to outline the various options.  
Things to consider are:
* Including version in package name and then switch using alternatives/modules.
* Just have an additional kit for mantid-last
* What do we do for the dependencies. - should we use SCLs for all dependencies.


Edit Workflow History Document Review
* Concern about NeXus performance for both API layer and tree structure of history.
* Michael's mockup for GUI layout for saving rolled/unrolled history
* Example script should not use SofQW, but a dummy name or a real workflow alg (e.g. DgsReduction)



Next Meeting - Tue/Wed after Easter Monday

Agenda

1. Documentation workflow proposal ![Documentation workflow proposal](../../../Design/Documentation/Documentation%20workflow%20option%201.png)
2. [Instrument downloading proposal](http://github.com/mantidproject/documents/blob/master/Design/InstrumentFetching.md)
3. Review Tools
4. Investigate 3rd party mailers (as an alternative to using our own mailman)
