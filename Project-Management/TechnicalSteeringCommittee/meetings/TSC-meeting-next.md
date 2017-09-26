Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?

New Items
---------

* State of 3.11 release
* CMake - [GenerateExportMacro](https://cmake.org/cmake/help/v3.7/module/GenerateExportHeader.html): Would like to use this to replace hand-coded [System.h](https://github.com/mantidproject/mantid/blob/master/Framework/Kernel/inc/MantidKernel/System.h) to be able to create completely low-level standalone modules. Problem: An additional argument that we need to the function only came in with cmake 3.7.2. Should we:
  - rebuild cmake on Linuxes
  - drag in these files to our CMake directory until we require cmake >= 3.7 (Moore/Gigg)
* http://reports.mantidproject.org 
  - openshift v2 (where we are at) is EOL on Sept 30 with v3 charging for the service
  - https://www.heroku.com/ can host django
  - migrating database

Minutes
-------
