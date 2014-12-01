Present: Anders, Martyn, Owen, Stuart, Peter

Agenda
======
1. Supporting multiple install versions
2. Moving developer docs into github wiki
3. Additional [builds of interest](http://builds.mantidproject.org/view/Develop%20Builds/): RHEL7 and osx 10.9 c-lang
4. c-lang on mavericks (10.9) vs intel on mountain lion (10.8)
5. Community-based RedHat/Ubuntu package distribution - ppa, copr, src.rpm
6. Maintenance task of speeding up the slowest tests - flagging slow running tests.

Minutes
=======
1. Mostly works for Windows - needs some tidying up in the install/uninstall scripts.  You can currently install, then copy to keep a version.  At the moment the env vars only point to the last installed version. ACTION: Martyn to create a ticket describing what needs to be done.  Mac/Linux both have issues because there is only a single user properties file.  This will be a issue if we have any absolute paths in the config.  Linux has a number of different options. If the users would only want to get the last release then we can generate an additional mantid kit with a different label, as we currently do with nightly/unstable.  ACTION: Pete will have a look at generating the jenkins build jobs.
2. Create a separate 'developer.github.io' repository to house the developer wiki etc.  Point the developer link on the www.mantidproject.org site point to developer.mantidproject.org - maybe have a github pages landing page that looks like the current Category:Development mediawiki page.
3. ACTION: Stuart will look at the 'missing' RPMs for RHEL7.
4. ACTION: Stuart to setup the ORNL Mavericks server with an Xcode build together with an static analysis job. ACTION: Test performance difference between intel (openmp enabled) kit and a clang kit on the same machine. 
5. In order to get mantid to build on ppa/copr you would need to have all the build deps as packages as well.  The main outstanding one is Paraview.  Martyn will check if he can build mantid without paraview in his PPA (Stuart will do the same for fedora/rhel).  We then need to generate Paraview develop kits that have everything mantid needs to build.  On Fedora/RHEL we also need nexus.  
6. How do we flag slow running tests?  We need to keep track of the performance in a better way.  ACTION: Owen will keep an eye on the performance of the new usage tests while he is doing his regular checks.  The question of if we want to create timing guidelines for usage examples was raised. The consensus was no, as the usage examples are more aligned with system tests than with unit tests.  We should configure jobs to run the usage tests in a similar way to the system tests, as in run periodically against incremental kits.  ACTION: Martyn to setup the jenkins jobs.
