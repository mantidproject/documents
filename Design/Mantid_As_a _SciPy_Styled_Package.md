Motivation
==========

Shaping Mantid as a SciPy styled package is one of the strategic aims in the [ORNL Mantid 5 year plan](ORNL_Mantid_5yearplan.pdf).
Howver it has become clear over several meetings and workshops that what should be included as part of this aim is not commonly agreed or 
understood within the development team or management of the project.
This document is an attempt to harmonise this understanding or at least provide a center point for discussion and agreement or what we want 
to achieve as part of this strategic aim and to provide a baseline high level design of what we need to do to implement it.

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
1. We must maintain backward compatability with the majority of users scripts, small changes are permissible if we are confident that this will not affect a significant number of users or scripts.  All breaking changes must be notified in advance of the release, ideally supporting deprecated aspects for at least one release.
1. All documentation and training courses will need to be updated to match the new structures.

   


Should
------

1. The structure of the python sub packages and other structures should be based on that presented by Andre Savici at the 
   [2017 Users Workshop](../Presentations/DevMeetings/2017-06/Mantid4PythonLibrariesAndNames.md).  
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

Python API 
----------

### Structure ###

This is primarily about structuring the locations of Algorithm and Fit functions more sensibly, the `Mantid.simpleapi` will maintain backward compatibility by accumulating all of the algorithms and Fit functions into a single import so existing scripts should work as normal.  For this reason, and to prevent other problems elsewhere this will mean we have to keep Algorithms names and Fit Function names unique as we currently do even when in seperate packages.

The structure below if modified from that presented by [Andre Savici at the 2017 Users Workshop](../Presentations/DevMeetings/2017-06/Mantid4PythonLibrariesAndNames.md).  We will only create a library if we have at least one item to include within it.

* Mantid.simpleapi
    - An accumulation libaray that will import all of the algorithms within Mantid as it currently does
* mantid.api
    - the current mantid.api (workspaces, validators, algorithm)
    
---

* mantid.io
    - all loading and saving
    - ?? should we split out NeXus, ISAW etc ??
* mantid.math 
    - matrix workspace math (also include `V3D`, `VMD`, ...)
    - `Plus`, `ExponentialCorrection`, `Rebin`, `Fit`
    - add aliases `Add`=`Plus`, `Subtract`=`Minus`
* mantid.math.axes
    - changing the axis of a matrix workspace (not the data), that is technique independent
    - e.g. ScaleX`, `ConvertAxisByFormula`, `MedianBinWidth`
* mantid.math.events
    - deals with events (technique agnostic)
    - `FilterEvents`, `RebinByPulseTime`
* mantid.math.multidimensional
    - technique agnostic multidimensional workspace operations
    - does not include `ConvertToMD`
* mantid.optimization
    - Curve Fitting and Optimization
    - e.g. Fit
* mantid.instrument 
    - grouping, masking, etc
    - e.g. `GroupDetectors`, `MaskBTP`, `SetGoniometer`, `MoveInstrumentComponent`
* mantid.workspace
    - manipulate workspaces, history
    - `RenameWorkspace`, `GroupWorkspaces`, `CompareWorkspaces`, `Comment`
* mantid.metadata
    - logs, titles, but not history

---



* mantid.muons
    - muon related algorithms and Fit Functions
* mantid.neutrons
    - things that are related to neutrons (time of flight), but not specific to a certain subfield (like diffraction)
    - e.g. `ConvertUnits`, `ConvertToMD`, `NormaliseByCurrent`, `He3TubeEfficiency`
* mantid.neutrons.crystal
    - single crystal stuff. Will include `UnitCell`, `OrientedLattice`, `SymmetryOperation`
    - e.g. `SetUB`, `FindPeaksMD`, `IndexPeaks`
* mantid.neutrons.diffraction
    - powder/amorphous diffraction stuff
    - e.g. `StripVanadiumPeaks`, `AlignAndFocusPowder`
* mantid.neutrons.inelastic
    - algorithms related to both direct and indirect inelastic spectroscopy
    - e.g. `GetEi`, `CorrectKiKf`, `SofQW`
* mantid.neutrons.reactor
    - single wavelength algorithms
    - right now most are facility specific
* mantid.neutrons.reflectometry
    - e.g. `FindReflectometryLines`
* mantid.neutrons.sans
    - e.g. `CalculateEfficiency`
* mantid.simulations
    - deal with outside simulation programs (CASTEP, SASSENA, ...)
    - `CalculateInelasticScatteringFromAbInitioPhonon` (`Abins`)
    
---

* mantid.constants
    - no algorithms here
    - physical constants
    - neutronic constants
* mantid.remote
    - `SubmitRemoteJob`, `AbortRemoteJob`


    
---

# Facility Specific Libraries

* mantid.ess
* mantid.hfir
* mantid.ill
* mantid.isis
* mantid.sns
* can add instrument or technique specific sublibraries
    - `mantid.sns.corelli.CrossCorelation`


### Generation ####

The generation of the Mantid Python API for algorithms is currently done at run time on startup, and has been found to take a large proportion of the time taken to start Mantid.  

#### C++ Libraries of Algorithms ####

Once C++ libraries are compiled within Mantid they will not change (other than being added to or removed from the plugins directory).  Therefore the API for a C++ library can be calculated once, and then resused until a new version that library is installed.
This could be done at compile time, or at runtime and not re-created if a valid API has already been created.  

Martyn Gigg has some ideas about how to achieve this, and will update this document later to add detail.

The following aspects need to be considered:

1. A user may add a library to the plugin directory they have compiled themselves, and may not have created a compile time API, so the would need to create one for this at run time (ideally once)
1. APIs will need to have some mechanism to ensure they match that specfifc library, for example by compring the modified date time of the library.
1. The APIs will need to be updated or removed when installing a different (new or older) version of Mantid, this should also include deleting APIs of Libraries that have been removed.


#### Python Algorithms ####

The registration of Python Algorithms and creation of the run time API is currently planned to be left as is, purely done at run time.

Documentation Structure
-----------------------

### Top Level ###
The documentation of Mantid will be rearranged to follow this structure:

> * Concepts
> * Simple scripting in Mantid (`mantid.simpleapi`)
> * Mathematical operations (`mantid.math`)
> * Instrument manipulations (`mantid.instrument`)
> * Workspace manipulations (`mantid.workspace`)
> * Experimental metadata (`mantid.metadata`)
> * Optimization and Curve Fitting (`mantid.optimization`)
> * File IO (`mantid.io`)
> 
> * Common scientific Constants (`mantid.constants`)
> * Common neutron operations (`mantid.neutrons`)
> * Common Muon operations (`mantid.muons`)
> * Working with simulation codes (`mantid.simulations`)
> 
> * Facility Specific Libaries (`mantid.sns` etc)
> 
> * User Interfaces
> * Release Notes
> * API Reference
>     - Python 
>     - C++ <http://doxygen.mantidproject.org/>
>     - Full list of Algorithms
>     - Full list of Fit Functions
>     - Full list of Fit Minimizers

### Module Page ###

Each module page would not be auto generated as now, but would have sections within it that are autogenerated within sphinx as we currently do within the algorithm pages, this wold be done by new custom directives.

An example module page would contain the following:
> The Title
> A short description of the module and its purpose
> A list of sub modules
> A list of Algorithms within this module
> A list of Fit functions within this module
> Other objects
> An example or two of things that are possible using this module with python examples that are doctested

Each of the lists will be generated by a directive, and should not appear at all if there is nothing in the list.
?? is it possible to extract the short module description from a docstring? ?? - If so all of the top can be replaced with a single directive.

### Algorithm and Fit Function Pages ###

These will remain as is, except that the category links will be redirected to the module pages.

C++ Library Structure
---------------------

In order to make the C++ library easy to navigate we will rearrange the library to match the module structure of the python modules.  This will increase the number of libraries we have, but will help split out some of those that have become bloated, such as Algorithms and DataHandling.

?? Do we want seperate C++ libaries for sub-modules such as mantid.math.axes or should be stop at a certain level and gather all the mantid.math into a single library? ??

If we decide to allow objects (such as algorithms) to be aliased in other python modules then we will need to define a rule of where the C++ algorithm will reside, we should use the first entry in the algorithm Category to be where the real code exists and the rest are aliases.

Low Level operations
--------------------



Questions
=========

1. Mantid.IO should we split out NeXus, ISAW etc?
1. Should mantid.simulations be mantid.neutron.simulations ?
1. If you have imported a sub selection of packages of IO, what does that mean for Load?
1. is it possible to extract the short module description from a docstring? 
1. Do we want seperate C++ libaries for sub-modules such as mantid.math.axes or should be stop at a certain level and gather all the mantid.math into a single library? 
