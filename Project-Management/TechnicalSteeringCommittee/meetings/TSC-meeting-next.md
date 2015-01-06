Agenda
------
* Agree on final strategy for pull requests
* Better strategy for release note creation. Put in rst? (Martyn)
* Topics for the TSC in January
  * Geometry redo
  * Pull requests (workflow including build servers and system tests)
  * Branch naming - drop `feature/`, `bugfix/` etc prefixes? (Martyn)
* Go over agenda for [dev meeting](http://www.mantidproject.org/Category:Workshop2015) (Pete...again)
* Github/Jenkins Slack channels (Martyn, Stuart)

Minutes
-------
* We will leave the final decision for pull requests until we meet in person later this month. Stuart will be install the openshift pull request plugin (https://github.com/openshift/test-pull-requests) on Jenkins and disable the current pull request plugin.  Martyn is currently working on external data at the moment.
* Idea is trying to get developers to write the release notes as they go, rather than a huge effort at the end before the release.  When the ticket is accepted, the release notes for that feature is added.  Could we leverage the developer notes for this ? Or the developer notes pulled out from the release notes?  Martyn will pull together a design document.
* One other topic was our move to clang on OS X.  Stuart also reported that we will soon have a 10.10 build server at ORNL.  Also it is worth running system tests on a clean OS X VM rather than the build servers.
* 
