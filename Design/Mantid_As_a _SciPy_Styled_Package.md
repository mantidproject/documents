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

This is primarily about structuring the locations of Algorithm more sensibly, the `Mantid.simpleapi` will maintain backward compatibility by accumulating all of the algorithms into a single import so existing scripts should work as normal.  For this reason, and to prevent other problems elsewhere this will mean we have to keep Algorithms names unique as we currently do even when in seperate packages.
The structure below if modified from that presented by [Andre Savici at the 2017 Users Workshop](../Presentations/DevMeetings/2017-06/Mantid4PythonLibrariesAndNames.md).  We will only create a library if we have at least one algorithm to include within it.

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
* mantid.instrument 
    - grouping, masking, etc
    - e.g. `GroupDetectors`, `MaskBTP`, `SetGoniometer`, `MoveInstrumentComponent`

---

* mantid.math.multidimensional
    - technique agnostic multidimensional workspace operations
    - does not include `ConvertToMD`
* mantid.metadata
    - logs, titles, but not history
* mantid.muons
    - muon related stuff
* mantid.neutrons
    - things that are related to neutrons (time of flight), but not specific to a certain subfield (like diffraction)
    - e.g. `ConvertUnits`, `ConvertToMD`, `NormaliseByCurrent`, `He3TubeEfficiency`

---

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

---

* mantid.constants
    - no algorithms here
    - physical constants
    - neutronic constants
* mantid.remote
    - `SubmitRemoteJob`, `AbortRemoteJob`
* mantid.simulations
    - deal with outside simulation programs (CASTEP, SASSENA, ...)
    - `CalculateInelasticScatteringFromAbInitioPhonon` (`Abins`)
* mantid.workspace
    - manipulate workspaces, history
    - `RenameWorkspace`, `GroupWorkspaces`, `CompareWorkspaces`, `Comment`
    
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

The documentation of 

C++ Library Structure
---------------------

Low Level operations
--------------------


Example
-------

Questions
=========

1. Mantid.IO should we split out NeXus, ISAW etc?
1. If you have imported a sub selection of packages of IO, what does that mean for Load?

