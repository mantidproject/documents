Agenda
======
1. Are you are aware if there exist good documenation for: describe well which documentation needs to updated before fixing a ticket and tested when testing a ticket. If not should this be a maintenance task?
2. What to do about System tests
3. Moving to cmake external data
4. What to do about slow builds
5. Restructuring mantid (What to do about the dependency tree)
  * Algorithm runtime dependency
  * Core packages
6. dot files for DataProcessingAlgorithms
7. HDF5/Nexus performance tests should be completed? What to do next?
8. Kill off unused headers
9. Encourage people to use Markdown type formats over microsoft formats in documentation?
10. We need a mechanism in the pull request workflow of stopping pull requests being merged unless system tests haver run and passed.

Actions/Agreed
========
* Dump cpack for linux. Pete will start looking at the RPMs
* Martyn will look into control files
* Maintenance task to use https://code.google.com/p/include-what-you-use/ via clang
* We are going to move to a slightly newer version of CMAKE to take advantage of key features. Move will be to CMAKE 2.8.12
* Start moving to External Data. Get this working in the following order. 
  1. Move the system test scripts over to the main Mantid repository (Martyn)
  2. Then look at adding the external data
  3. CTest for system tests
  4. Parameterized downstream builds so that pull requests will run system tests
* Move to using public and private features of the Shared libraries in newer CMAKE see above.
* Build improvements should be benchmarked. 40 mins for RHEL6 currently

