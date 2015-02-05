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
9. Developer workshop agenda was agreed upon
10. Coding standards were updated
11. Timelines:
  * Start of v3.4
    * Move to apple clang on OS X (check with Steven)
  * During v3.4
    * Developers will move to pull requests after the workshop
    * Build servers will move to pull requests by the end of March and `develop` is dropped
    * ExternalData and merge of system tests will be implemented by the end March
  * At the start of v3.5
    * Move to GH issues
    * Developers move to VS 2013 (Owen to compile dependencies)
12. Discussion of dependencies issue
  * If the mantid loaders made easier to compile then Paraview would likely support Mantid output formats
  * Benefit of having more but smaller number of library vs the opporsite was discussed
  * Different organisation to Mantid code, e.g. solve issue with long path lenghts, was discussed. It was agreed that code reorganisation should be taken forward. A suggested time for role out v3.6. Easies to create a branch to play around (Pete)
  * Code compile time issue. Different ways of creating binaries. This was agreed. Owen is happy to give this a start
  * class DLLExport on windows. This was agreed. Task to investigate if this is easy or not. Martyn start to investigate
