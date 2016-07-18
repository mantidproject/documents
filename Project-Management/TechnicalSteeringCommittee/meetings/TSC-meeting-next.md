Agenda
======

Pinned Topics
-------------
* Review any outstanding external pull request or issues? (Owen)
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)? (Fede)

New Items
---------

* PMB have approved 4 weeks of effort for an evaluation of plotting packages in light of `qwt5` -> `qwt6` being a non-trivial transition. In particular the evaluation should include `matplotlib`.
* Potential VSI Improvements
  * Enable [multithreading in the VSI](https://blog.kitware.com/simple-parallel-computing-with-vtksmptools/)? 
    * Add Threading Building Blocks to the Mantid Dependencies?
    * Use TBB on OS X and OpenMP on Linux & Windows?
  * Enable [OSPRay ray-tracing engine](https://blog.kitware.com/kitware-brings-ray-tracing-to-the-visualization-toolkit/)?
    * Requires [OSPRay](http://www.ospray.org/), [Embree](https://embree.github.io/), freeglut, [TBB](https://www.threadingbuildingblocks.org/), [ISPC](https://ispc.github.io/) (building only)
