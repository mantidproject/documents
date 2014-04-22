Agenda
======
1. Documentation workflow proposal 
2. Review of the text for the contributing file.
3. [Instrument downloading proposal](http://github.com/mantidproject/documents/blob/master/Design/InstrumentFetching.md)
3. Review Tools
4. Investigate 3rd party mailers (as an alternative to using our own mailman)

Minutes
=======

1.Documentation Workflow Proposal 
![Documentation workflow proposal](../../../Design/Documentation/Documentation%20workflow%20option%201.png)

There was some discussion about whether we need to pull in the science specific sections from the wiki (that the users can edit) into the offline documentation.

Martyn gave a quick overview of the sphinxext he wrote and sphinx's doctest extension.  Next step is to write a prototype.
 
2.Anders will update the CONTRIBUTING.md to ask them to contact us first and there should be some mention of preferring small pull requests.  

3.Instrument downloading proposal
 * There was a question about GitHub's rate limiting on unauthenticated connections.  We will probably not hit this limit, but we could always authorise the Mantid App and pass a key.  
 * Should it be Framework or GUI level ?  The consensus was Framework.
 * For the case of a user starting Mantid and then loading an instrument data file that has a newer IDF that hasn't been downloaded yet.  Ideally we would want to block loads for that instrument (and not the others).
 * To avoid having to check all the time, check at startup then add a method to run the check for updates on demand.

Agenda for Next Meeting

Date : 

1.
2. 
