Agenda
======
* NeXus vs HDF5. What are the next steps? (Owen/Pete)
* Is it a good idea to bundle matplotlib (question from PMB)
* Updating [c++ coding standard page](http://www.mantidproject.org/C%2B%2B_Coding_Standards) to reflect in better detail the standard we use as developers, e.g. naming of attributes of a struct which only holds data members? (Anders/Martyn)
* Dependency for fitting proposed by Michael Wedel at PSI - [Adept](http://www.met.reading.ac.uk/clouds/adept/). He has already written a SPEC file & debian control file in a fork: https://github.com/MichaelWedel/adept-fork
* [Pull request workflow](https://github.com/mantidproject/documents/blob/master/Design/PullRequests.md)
* CMake and Paraview training sessions
* Guidelines for algorithm/python algorithm dependencies: -  [Example](http://trac.mantidproject.org/mantid/ticket/10341)

Minutes
=======
* Pete will create a repository in [nexus' github](https://github.com/nexusformat/) to benchmark
* The TSC recommends shiping matplotlib with mantid. It will be required by the rpm/deb installers. Martyn will add it to OSX.
* Updating the C++ coding standards should be a [maintenance task](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/MaintenanceTasks.md).
