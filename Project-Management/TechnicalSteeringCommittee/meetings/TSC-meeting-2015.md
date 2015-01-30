Agenda
======
1. Geometry redo
 1. Considerations for indirect instruments
 2. Mcstas 
 3. Spectra table convert units
2. Pull requests (workflow including build servers and system tests)
3. Branch naming - drop feature/, bugfix/ etc prefixes? (Martyn)
4. [Dependency issues](https://github.com/mantidproject/documents/blob/master/Design/DependenciesAndRestructure.md) (Owen)
5. Switching from apache to nginx on linode to reduce system load
6. Switch to Ninja for build scripts on Linux/Mac
7. Moving development information to gh-pages/github wiki
8. Dropping support for OSX 10.8. Paraview/clang/intel/etc is pushing us to make this decision (Stuart/Pete on behalf of Steve)
9. Names against all items on agenda for Dev meeting. 
10. C++ coding standard feedback
11. Time line for pull request and moving to github issues
12. Timeline for transition to VS 2013

Minutes
=======
1. Geometry discussion - see [notes](../reports/IDFv2-notes.md)
2. External Data - Martyn gave overview of progress on external data. Main mantid repository was nearly converted but the question still remained about where the data should go remotely. As a temporary solution is was decided to use Linode while a longer term solution was found. Issues to look in to:
  * Build scripts need to configure locations for data during build;
  * Location of remote data;
  * Links for SNS dropbox that get mounted locally;
  * Fold in system tests + data into main repository. New target to download system data.
3. Discuss and decide how to best role out pull request - [see notes](TSC-meeting-2015-Pull-Request-Plan.md)
4. Branch prefixes to be dropped - Martyn to check trac hooks/git aliases before annoucement
5. No benefit in moving to nginx from Longview reports
6. Agreed to move linux/mac buildscripts to use Ninja
  * Martyn to coordinate
  * Update documentation for developers about build environment
7. Need to plan moving the tutorials to rst/Sphinx
8. PMB agreed that 10.8 OS X support could be dropped for the next release
