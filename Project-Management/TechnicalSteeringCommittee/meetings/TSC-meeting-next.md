Agenda
======

* Dropping osx 10.8 from the matrix (Steve)
* Peformance tests. Average commit statistics (Owen Arnold)
* Human interface guide (from developer meeting)
* Best practice for changing rst files. Should common sense apply or should we write a guide (from developer meeting)
* How TSC advertise itself better (from developer meeting)
* Planned work on Multiple scattering [#11106](http://trac.mantidproject.org/mantid/ticket/11106) (Anders) (SSC ticket [#8926](http://trac.mantidproject.org/mantid/ticket/8926))
* Possible improvements to existing definition files (Pete)
  * ~~Change underlying file format to hdf5~~
  * Looking over existing definitions to use `RectangularDetector` and tube
  * Adding new primatives (e.g. array of tubes)
  * ~~Other "easy" improvements~~
* [cxxtest](https://github.com/CxxTest/cxxtest) is not dead ([#11000](http://trac.mantidproject.org/mantid/ticket/11000) and  [FindCxxTest.cmake](https://github.com/Kitware/CMake/blob/v2.8.12/Modules/FindCxxTest.cmake)) (Pete)
* Any comments to first cut at report for [tracking design documents](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md) (Anders)
* [Design proposal](https://github.com/mantidproject/documents/blob/master/Design/HandlingMovingInstruments.md) for handling of data from moving instruments (Anders) 

Minutes
=======
Present: Anders, Pete, Ross, Stuart, Martyn

1. Drop on all but `master_clean`
2. Owen not present
3. Steve Miller is starting. Pete to check with Steve in 1 month
4. No guide to be written. Not worth the time
5. Advertising TSC:
    * Send minutes to developer list (Anders)
    * Add link to tsc email on developer page (Anders)
    * Design documents to go to developer list
6. Just for information
7. Points discussed
    * Update rectangular definitions to use primitives
    * Add array of tubes and others
    * Other file formats not considered here.
8. Explore other options for unit testing framework
