Motivation
==========

Shaping Mantid as a SciPy styled package is one of the strategic aims in the [ORNL Mantid 5 year plan](ORNL_Mantid_5yearplan.pdf).
Howver it has become clear over several meetings and workshops that what should be included as part of this aim is not commonly agreed or 
understood within the development team or management of the project.
This document is an attempt to harmonise this understanding or at least provide a center point for discussion and agreement or what we want 
to achieve as part of this strategic aim and to provide a baseline high level plan of what we need to do to implement it.

Requirements
============

As mentoned above the requirements underlying the strategic aim are not universally shared so this document will serve as a place to detail
what we have agreed.

This is an initial draft from a discussion between Nick Draper and Martyn Gigg and will need to be discussed and agreed with 
other team leads.

Must
----

1. The Algorithms need to be seperated into sensible sub packages that allow sensible imports of only the areas of interest 
   rather than all algorithms as is the current situation.
1. The current top level api import must be maintained in name and function. 
   So `from mantid.simpleapi import *` must import all of the sub packages.
1. The documentation structure of Algroithms must match that of the sub packages to make it easier to locate the documents you need.
1. The category structure in Mantid must match the python package structure, but use english language syntax rather than Python syntax.
   For example Neutron vs Mantid.Neutron.
   


Should
------

1. The structure of the python sub packages and other structures should be based on that presented by Andre Savici at the 
   [2017 Users Workshop] (../Presentations/DevMeetings/2017-06/Mantid4PythonLibrariesAndNames.md).  
   Note: this will not include the changes to the naming of algorithms, just the package structuring.
1. We should take advnatage of the restucturing into smaller packages to define a small number of these to be "core".
   This will define this term, which currently is interpreted by each individual.
1. The C++ library structure should mirror the python package structure as far as possible to make it easy for developers to 
   navigate the code.
1. We should decrease the time it takes to generate the Python API at run time. 
   Investigations have shown this is a major part of the startup time of Mantid.
   

Could
-----

1. The developers will need tools or help to make it easier to add new libraries, and have full support (builds, python, installers, 
   unit testing, docs, static analysis etc).
1. While restructuring of the Algorithms libraries it would be beneficial to breakup the very large libraries of Algorithms and 
   DataHandling.
1. Low level functions for a limited list of operations (ConvertUnits, Rebin and possible a few others), could be created and
   exposed to python allowing simple operations on vectors or numpy arrays of data without using workspaces or geometry etc.
   1. Where these are created they should be used within the matching algorithm as long as that does not degrade 
      performance or maintainability.
   1. The low level function for ConvertUnits could replace much of the code in UnitConverter.py.

Won't (recorded for the future)
-------------------------------

1. Renaming of algorithms to follow a more consistent pattern.  
   This is not currently desirable due to the dirsuption it would make to users scripts.

Design
======




Example
-------

Questions
=========

1. If you have imported a sub selection of packages of IO, what does that mean for Load?

