Agenda
------
* Agree on final strategy for pull requests
* Better strategy for release note creation. Put in rst? (Martyn)
* Topics for the TSC in January
  * Geometry redo
  * Pull requests (workflow including build servers and system tests)
  * Branch naming - drop `feature/`, `bugfix/` etc prefixes? (Martyn)
  * Dependency issues https://github.com/mantidproject/documents/blob/master/Design/DependenciesAndRestructure.md (Owen)
* Go over agenda for [dev meeting](http://www.mantidproject.org/Category:Workshop2015) (Pete...again)
* Github/Jenkins Slack channels (Martyn, Stuart)

Minutes
-------
* We will leave the final decision for pull requests until we meet in person later this month. Stuart will be install the openshift pull request plugin (https://github.com/openshift/test-pull-requests) on Jenkins and disable the current pull request plugin.  Martyn is currently working on external data at the moment.
* Idea is trying to get developers to write the release notes as they go, rather than a huge effort at the end before the release.  When the ticket is accepted, the release notes for that feature is added.  Could we leverage the developer notes for this ? Or the developer notes pulled out from the release notes?  Martyn will pull together a design document.
* One other topic was our move to clang on OS X.  Stuart also reported that we will soon have a 10.10 build server at ORNL.  Also is it worth running system tests on a clean OS X VM rather than the build servers.
* Pete will update the agenda and send an email out to the developer list.  All the presentations should be in the wiki.
* We all agreed to turn off Jenkins auto posting.  We have also made the GitHub channel less chatty (only new issues, pull requests and branches will be shown)
* Pete has the usage statistics server running live.
