Agenda
======
1. Are you are aware if there exist good documenation for: describe well which documentation needs to updated before fixing a ticket and tested when testing a ticket. If not should this be a maintenance task?
2. What to do about System tests
3. Moving to cmake external data
4. What to do about slow builds
5. Restructuring mantid (What to do about the dependency tree)
..* Algorithm runtime dependency
..* Core packages
6. dot files for DataProcessingAlgorithms
7. HDF5/Nexus fix
8. Kill off unused headers

Actions/Agreed
========
* Dump cpack for linux. Pete will start looking at the RPMs
* Martyn will look into control files
* Maintenance task to use https://code.google.com/p/include-what-you-use/ via clang
* Move to using public and private features of the Shared libraries in CMAKE 3.0 
* Build improvements should be benchmarked. 40 mins for RHEL6 currently
* 

