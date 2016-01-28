* Geometry redo
* Workspace redo
* Python discussion
  * better interaction with python data types
  * identifying and exposing *core* numerical operations
  * changing framework from a python wrapped package to python package with c++ innards
* MPI changes to algorithms
  * change the algorithm base class
  * re-write `LoadEventNexus`
  * re-write `ConvertToMD`
* Technical debt
  * reduce size of algorithms' `exec`
  * `Property`
  * algorithm naming and transitioning towards better
* Code re-org
  * top level to support better packaging (e.g. `mantid`, `mantid-gui`, ...)
  * inside framework still needs discussion
  * improve speed of builds
* Inform PMB we want more build servers for improved throughput
* Improving communication
  * assist instrument scientists in generating and connecting to/from mantid
  * developer documentation
* Stability ranked very high at SSC
  * refactoring user interfaces to improve testability
  * improving testing system(s)
