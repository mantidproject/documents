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

4.Various Tools
 * Waffle.io - Sits on top of github issues and provides a nicer view.
 * gitter.im - a possible replacement for the skype chat

5.Mailing lists
 * A quick look at Mailchimp, seems mainly aimed at marketing.  Looked like it could work (maybe would need to use Mandrill as well).  Martyn will setup a mailing list for the TSC.

6. AOB
 * When do we want to move the MediaWiki ?  If we are sticking with MediaWiki then it may as well be sooner.  
 * Developer documentation - discuss next time (potential options: github site, github wiki, mediawiki, ...)


Agenda for Next Meeting

Date : In about a month

1.
2. 
