Agenda
======

* Review any outstanding external pull request
* [Move to github issues](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/WorkplanForMoveGithubIssues.md)
* Final vote on label for science validations (Sci Validation, Science Validation, Sci Test, Good Science, Valid Sci or other) and recommended meaning of this label
* [PMB report](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-PMB-report-2015-05-29.md) for this coming Friday
* Pros and cons of having `clang-format` provide [automatic reporting](http://builds.mantidproject.org/view/All/job/master_clang-format/) (Ross)
* Use tcmalloc on Windows: v3.4 supports releasing memory back to the OS. Initial tests suggest much better performance for large workspaces, e.g. faster non-blocking delete (Martyn)
* With ref to [minutes](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/meetings/2015/TSC-meeting-2015-01-29.md) - transition to VS 2013 or VS 2015
* [Signing mac executable](http://certhelp.ksoftware.net/support/articles/18835-how-do-i-sign-files-on-mac-osx-) 
* Doc tests on Windows?
* Downstream jobs for PR builds. Or can we otherwise speed things up. Request from Nick D.
* 

Minutes
=======

Present: Pete, Ross, Martyn, Nick, Owen and Anders

1. No external pull requests
2.  Migration to github issues
  * Script working for all the migration nearly complete by Stuart C
  * Pete still working on [reports](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/WorkplanForMoveGithubIssues.md).
  * Anders is going to send a list of tickets which should be moved across to the autoredcution repository for Stuart to process.
  * Migration will probably take a few hours. 
  * SSC report highlighted to be critical (Nick)
  * We need to make Trac read only and announce the change after the reports are in place
3. Label to use for science validation was agreed to be: Science Validation. In summarise: purpose is it to use this label for issues/tickets where a scientist, specialist in a science domain, will (is required) validate the output beyond that of a testing developer 
4. PMB report discussed, remaining items forwarded to next meeting
