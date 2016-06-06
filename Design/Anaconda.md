#Anaconda#

The purpose of this document is to examine how useful and feasible it is to
provide conda packages for Mantid framework and/or Mantid GUI for Mantid users.

##Motivation##

(Ana)conda makes it much easier to manage the deployment of a software package itself
and probably more importantly, its dependencies.
Although only started in 2012, it has seen widespread acceptance in the python community
and even high performance computing community. 
An example is that NERSC has conda installed as a module.

**What is (ana)conda**

Anaconda is an open-source solution by [Continuum Analytics](http://continuum.io)
for package management and deployment.

**Where are the packages hosted**

Cloud. http://anaconda.org

**Binary compatibilities**

Anaconda builds a software environment of its own with little dependencies on the system.
This allows for a single linux binary distribution that works for different flavors
of linux systems (dertainly 32bit system and 64bit system needs different binaries).
Windows and OSX need their own binaries as well.

##Selected Use cases##

**Simple installation for novice users**

All he/she needs to do is
* Install anaconda
* Install mantid by
  $ conda install -c mantid mantid

**Simple deployment at High-performance computing facilities**

Manual build of Mantid can be a tedious job for a user of high-performance computing
facilities. 
With conda distribution, a user can easily deploy their Mantid-dependent
computations at such facilties as NERSC.

**Nicely play with other (python) packages**

There are many python packages supported in conda. 
Installation of the packages and their dependencies alongside with Mantid,
making sure they are compiled and linked agaist the same libraries,
would not be a big hassle as it could be.

##Experiment##

An experiment was done to port Mantid (framework only) into conda:
 https://github.com/mantidproject/mantid/compare/master...mcvine:master
 
The main changes are:
* Framework/CMakeLists.txt: have to force finding GSL and OpenGL
* Added subdir conda:
  - meta.yml: pkg meta data. Name and version. Dependencies
  - build.sh: linux build script. Installed dependencies that are not included yet in conda, and then call cmake and make to build
  - run_tests.py: test driver

Artifacts:
* A mantid-framework-only conda package now available at anaconda "mcvine" channel
  - it can be installed by
    $ conda install -c mcvine mantid
  - Only tested so far to reduce some ARCS data. 

##Proposed Solution##
* Make a new Mantid ticket for this
* Migrate changes to a branch
* Improve build scripts (windows build script is not implemented at all)
* Add test of conda package to the jenkins system

