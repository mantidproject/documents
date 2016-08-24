Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)? (Fede)

Minutes
-------

* Update of plotting evaluation
  * Packages the were moved into detailed evaluation were qwt6, matplotlib, and qtcharts
* Potential VSI Improvements
  * Enable [multithreading in the VSI](https://blog.kitware.com/simple-parallel-computing-with-vtksmptools/)?
    * Add Threading Building Blocks to the Mantid Dependencies?
    * Use TBB on OS X and OpenMP on Linux & Windows?
  * Enable [OSPRay ray-tracing engine](https://blog.kitware.com/kitware-brings-ray-tracing-to-the-visualization-toolkit/)?
    * Requires [OSPRay](http://www.ospray.org/), [Embree](https://embree.github.io/), freeglut, [TBB](https://www.threadingbuildingblocks.org/), [ISPC](https://ispc.github.io/) (building only)
