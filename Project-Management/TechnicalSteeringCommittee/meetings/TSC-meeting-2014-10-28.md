Agenda
======
* Guidelines for algorithm/python algorithm dependencies: - [Example](http://trac.mantidproject.org/mantid/ticket/10341)
* Compiler/system checks in code - Create a global set in Kernel (Martyn)
* Guidelines for modifying existing fitting function (Anders)
* [Threading Building Blocks](https://www.threadingbuildingblocks.org/) (TBB) (Hahn)
* Linode maintenance - Security updates (Martyn)

Minutes
=======
* Martyn will create documentation to say not to call python algorithms from c++ algorithm unit tests
* Compiler checks for features should be a maintenance task, and it should be advertised to the developers
* Anders will write up guidelines for modifying existing fitting functions to pass by the TSC. There should be a similar document for algorithms
* Performance benchmark results:
  * Need to try a osx10.9/clang build on a osx10.8 system (Steven)
  * Still need to move to paraview 4.2 before osx10.9/clang is the supported version (Stuart)
  * Change the `PARALLEL_*` macros and then all of the code (Steven organizes)
  * We should have additional build of the performace tests that run in serial (Steven)
  * newer gcc on RHEL6 (Stuart)
  * Leftover tasks: clang on linux, consolidating mutex usage to one version, converting `ThreadPool` to abstract a library
* Linode server automatically install security update (Martyn)
