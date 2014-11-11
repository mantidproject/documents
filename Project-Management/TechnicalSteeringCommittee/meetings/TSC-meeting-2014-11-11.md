Agenda
======
* Micheal Wiedel on [automatic differentiation](https://github.com/mantidproject/documents/blob/master/Design/IntegratingAdept.md)
* Design for [determining usage statistics](https://github.com/mantidproject/documents/blob/master/Design/MeasureUsageStatistics.md)
* Adding OS X clang to matrix build.
* Adding Fedora to the matrix builds & RHEL6/Fedora resourcing (Pete/Stuart)
* Linode maintenance - Jenkins backup (Martyn)
* Make suggestion of topics the TSC presents at developer meeting and agenda items for TSC meeting days scheduled during: http://www.mantidproject.org/Category:January_2015_Visit 
* Are you are aware if there exist good documenation for: describe well which documentation needs to updated before fixing a ticket and tested when testing a ticket. If not should this be a maintenance task?
* Formatting and coding standards ([current definition](http://www.mantidproject.org/Coding_Standards), [c++ comparison](https://gist.github.com/peterfpeterson/f095f0153cab9b6a6459), pep8, [git-clang-format](https://llvm.org/svn/llvm-project/cfe/trunk/tools/clang-format/git-clang-format))
* Brief chat about http://trac.mantidproject.org/mantid/ticket/10501. (Owen)
* Mantid server, obtain a TSC, technology choice. (Owen)


Minutes
=======
* Michael presented his document on automatic differentiation using the Adept package.  The next step is to get the Adept package included within the dependencies for the build servers.  
  * We need to add the linux packages (Stuart/Martyn) to the relevant repos 
  * Create homebrew formula for OS X (Steve/Stuart).  
  * Windows and Mac Intel needs to be added to 3rd party (Owen).
  * Create a build job on jenkins to build the binaries so we document how to build it (Owen).
  * The mantid-developer package dependencies need to be updated (Pete)
* Pete went through the design of collecting OS statistics
  * Point the service at api.mantidproject.org
  * It was decided not to push this into a patch release.
  * Nick to send an email/survey to relevant mailing lists asking about usage.
* Matrix build.
  * Owen to request hardware for a mac build server at ISIS.
  * Decided that we are not urgent to move Windows 8 into matrix build.
* ORNL is moving forward with its migration to Fedora 20. 
  * Add Fedora 20 into the matrix build.
  * Move ornl-rhel7 hardware to fedora 20.
  * Use existing small fedora 20 vmware resources for rhel7.
* It was decided that we are going to standardise on clang-format.

