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

Attendees: Bush, Draper, Gigg, Moore, Peterson, Savici

* Release 3.11
  - testing has not revealed anything that will hold up the release
  - Draper and Savici will go over the release notes
* `GenerateExportMacro` - Moore will drag in appropriate files into our cmake directory for now
* Ubuntu 17.04 has a bug with NeXus package - NIAC has been informed
* Peterson will move http://reports.mantidproject.org to a container on linode
* Gigg will put together the start of a wiki page with various web endpoints and circulate to TSC for additional information
