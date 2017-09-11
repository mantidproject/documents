**Draft Pending TSC Approval**

This document summarises project proposals to form a programme of work for the [Core Mantid Developement Team(s)](https://github.com/mantidproject/documents/blob/master/Project-Management/PMB/Mantid%20core%20team%20proposal.docx).
This document will be maintained and updated and prioritised as a [Mantid Technical Steering Committee](https://github.com/mantidproject/documents/tree/master/Project-Management/TechnicalSteeringCommittee) responsibility.

Core team projects must align with the [core team](https://github.com/mantidproject/documents/blob/master/Project-Management/PMB/Mantid%20core%20team%20proposal.docx) strategy, covering

*	Correctness of scientific results
*	Product stability
*	Runtime performance
*	Improved collaboration between facilities
*	Cleaner interfaces and structure allowing faster development
* Refactoring mantid to allow developers to better contribute scattering software rather than developing system software

Guiding principles

1. Stability is vital, including stability of the user experience
1. Mantid is a python project with C/C++ as needed  (Note this is yet to be agreed by all parties!)
1. Prefer language standards, then community accepted libraries, then develop solutions
1. Interoperability with existing scientific python ecosystem
1. Make choices to empower users to contribute code
1. Data structures should represent science

# Core Programme

1. [Histogram Library](#histogram-library)
1. [Event Data Library](#event-data-library)
1. [Crystallography Library](#crystallography-library)
1. [Curve Fitting Library](#curve-fitting-library)
1. [Metadata Library](#metadata-library)
1. [Other Libraries](#other-libraries-for-_neutron-_physics-related-concepts)
1. [Workspace-2.0](#workspace-2_0)
1. [read write standard nexus files](#read-write-standard-nexus-files)
1. [leverage beamline](#leverage-beamline)
1. [distributed data reduction 2D](#distributed-data-reduction)
1. [units](#units)
1. [workspaces](#workspaces)
1. [distributed data reduction MD](#distributed-data-reduction-md)
1. [Project Structure: Python vs C++ with extensions](#Project-Structure:-Python-vs-C++-with-extensions)
1. [Lazy loading NeXus files](#lazy-loading-nexus-files)
1. [Uniform approach to interacting with NeXus (or just HDF5)](#Uniform-approach-to-interacting-with-NeXus)
1. [Replace MD with appropriate VTK data structure](#Replace-MD-with-appropriate-VTK-data-structure)

## Histogram Library
### Motivation
A major part of data reduction is about histograms.
Developers as well as users need a simple but fast and versatile way to store and manipulate histograms.
The `HistogramData` library is a first step in that direction.
It needs to be extended with more functionality and must be made fully accessible from Python.
### Blocking Projects
None
### Specialist Skills Required
### Resource and Profile Estimate
### Risks if Not Addressed
### PMB Approval and Comments
#### Approval Date 
#### Comments

## Event Data Library
Provide a twin library of the `HistogramData` library for low-level interaction with neutron event data.
This would extract and possible extend a lot of functionality that is currently encapsulated in `EventList` and possible also the event representation of `MDEventWorkspace`.
As usual, this should be fully functional with a complete Python interface.
### Motivation
### Blocking Projects
None
### Specialist Skills Required
### Resource and Profile Estimate
### Risks if Not Addressed
### PMB Approval and Comments
#### Approval Date 
#### Comments

## Crystallography Library
### Motivation
Many experiments are dealing with crystals and thus data reduction must be able to handle crystallography related concepts such as HKL values, point- and space-groups, and many more.
These low level concepts should be provided as a small and lightweight library, providing data types for safely and correctly storing and manipulating them.
As usual, this should be fully functional with a complete Python interface.
### Blocking Projects
None
### Specialist Skills Required
### Resource and Profile Estimate
### Risks if Not Addressed
### PMB Approval and Comments
#### Approval Date 
#### Comments

## Curve Fitting Library
The current fitting framework is complex and depends and workspaces.
Fitting should be made available for individual histograms by a library that does not depend on higher level concepts such as workspaces.
As usual, this should be fully functional with a complete Python interface.
### Motivation
### Blocking Projects
None
### Specialist Skills Required
### Resource and Profile Estimate
### Risks if Not Addressed
### PMB Approval and Comments
#### Approval Date 
#### Comments

## Metadata Library
Apart from histograms and event lists, metadata is another major component of workspaces.
Storing, accessing, searching, and filtering of such metadata should be encapsulated in a library.
As usual, this should be fully functional with a complete Python interface.
### Motivation
### Blocking Projects
None
### Specialist Skills Required
### Resource and Profile Estimate
### Risks if Not Addressed
### PMB Approval and Comments
#### Approval Date 
#### Comments

## Other Libraries for (Neutron-)Physics Related Concepts
### Motivation
The libraries listed above are most likely not a comprehensive list covering all relevant concepts in (neutron-)physics.
Identify such concepts and evaluating whether it is worth providing a library for them or not.
### Blocking Projects
None
### Specialist Skills Required
### Resource and Profile Estimate
### Risks if Not Addressed
### PMB Approval and Comments
#### Approval Date 
#### Comments

## Workspaces-2.0
### Motivation
The current workspace hierarchy is an inflexible, bloated, and frequently abused construct that most developers do not fully understand.
Based on many of the low-level libraries above, a more versatile and complete set of workspace types would be developed.
### Blocking Projects
None
### Specialist Skills Required
### Resource and Profile Estimate
### Risks if Not Addressed
### PMB Approval and Comments
#### Approval Date 
#### Comments


## Read Write Standard NeXus Files

### Motivation
The NeXus [format](http://www.nexusformat.org/) is a well estabilished and critical file format for neutron data. That standard is undergoing change, with an early proposal for Geometry layout expected by September 2017. The new format will replace the string-based Instrument Definition File. 

1. **Performance**: relating to Instrument Definition processing has already been highlighted as an operational [requirement- Geometry 2016](https://github.com/mantidproject/documents/blob/master/Design/Instrument-2.0/requirements-v2.md#performance-as-a-non-functional-requirement) by a cross-facility delegation, owing to performance concerns.
1. **Correctness**: Mantid, at present, only load instrument definitions. A saved process nexus file, from a workspace that has been subject to an in-memory translation yields a incorrect geometry. 
1. **Cost**: As the nexus geometry is in embryo, cost of change is low, and we are invited to preview and try the new formats prior to ratification. Post rattification, our ability to influence the format, or request changes will be limited.
1. There is already momentum from the ESS to steer, define and use an updated format. There are economies of scale reasons for collaborating on this now. ISIS/ESS are prototyping the new format, summer 2017, with findings available to steer better estimates and inform benefits available mid September 2017.

### Blocking Projects
None
### Specialist Skills Required
TODO
### Resource and Profile Estimate
TODO
### Risks if Not Addressed
* Cost. Delaying involvement will cost more time and effort. See Motivation.
* Correctness issues will remain. See Motivation.
* Performance issues will remain. See Motivation.
* The processed nexus format saved by Mantid is already not NeXus compliant. Delaying will put Mantid further behind.
* Technical debt. Old/legacy code for handling IDFs remains, with no future for replacement. 
### PMB Approval and Comments
#### Approval Date 
#### Comments

## Leverage Beamline

### Motivation

The ESS and ISIS in-kind team has, thus far, provided 100% of the resourcing of the `Instrument 2.0`/`Beamline` project. This has yielded more efficient and faster in-memory structures for all users, and core step-scanning changes required by the ILL. `Instrument 2.0` is explicitly described in the [SNS 5-year plan, section 4](https://github.com/mantidproject/documents/blob/master/Design/ORNL_Mantid_5yearplan.pdf)

1. We currently wrap aspects of Instrument 1.0, and created Instrument 2.0 based on Instrument 1.0, which is highly inefficient. Killing Instrument 1.0 would not only reduce the size of the code base, but also vastly improve in-memory performance and load/save times. This would first require extending and leveraging Instrument 2.0 for things such as shape related operations.
2. The ESS and ISIS in-kind team has extensively designed and prototyped features for Mantid, that are not a 1/1 replacement for `Instrument 1.0`, and will support new classes of real neutron instruments. These are described in Section 4.1.2 (Objectives) in the [SNS 5-year plan](https://github.com/mantidproject/documents/blob/master/Design/ORNL_Mantid_5yearplan.pdf) and include complex beam paths. Prototyping has signficantly de-risked these designs, and they are now ready to be put into production.

### Blocking Projects
None
### Specialist Skills Required
TODO
### Resource and Profile Estimate
* 2-5 months at 1FTE to complete basic Beamline with performance optimisation
* 2-6 months at 1FTE for non-straight beam paths
* 3-12 months at 1FTE to eliminate Instrument 1.0
### Risks if Not Addressed
* Knowledge sharing. Understanding of the Instrument 2.0 long-term design and current implementations is entirely within the ESS Mantid team.
* Performance and memory requirements. `Instrument 1.0` is becoming an uncessary overhead. See Motivation.
* Technical debt around legacy Geometry/Instrument. No other contingency plans to resolve this.
### PMB Approval and Comments
#### Approval Date 
#### Comments

## Distributed Data Reduction 
### Motivation

In-situ data reduction, and increasingly large data sets require rapid processing at the Algorithm level. These factors are increasingly of concern to several facilities. The problems are particularly accute for Event mode processing.

Section 9.1 of the [ORNL 5-year plan](https://github.com/mantidproject/documents/blob/master/Design/ORNL_Mantid_5yearplan.pdf) outlines a desire to apply Mantid in heterogeneous distributed computing environements. This is also a featured in Section 2.2.3 ESS data-reduction-report 2017. 

For `MatrixWorkspaces`, a coordinated, [framework level approach](https://github.com/mantidproject/documents/blob/master/Performance/mpi-based_data_reduction_-_different_approach.pdf) a first usable version is close to delivery. Not only is there is  a need to identify and correctly port a mimimal set of critical algorithms over to this way of working, we also need to ensure that the framework itself is well developed and supported, particularly during the initial rollout phases.

### Blocking Projects
No other core projects block this though Workspace design is of interest
### Specialist Skills Required
TODO
### Resource and Profile Estimate
4-8 months for 1FTE based on ESS estimates
### Risks if Not Addressed
* Mantid will not be suitable for data rates produced by modern facilities
* Piecemeal approaches will not yield the overall performance required.
* Attempting to solve framework performance problems at the last minute is risky at the operating facility level
* Mantid uses a range of ad-hoc/un-coordinated approaches for distributed computing
* The current knowledge of the framework level approaches is siloed to the ESS
### PMB Approval and Comments
#### Approval Date 
#### Comments

## Units
### Motivation
Described in section 4 [ORNL 5-year plan](https://github.com/mantidproject/documents/blob/master/Design/ORNL_Mantid_5yearplan.pdf)
### Blocking Projects
Aspects of Beamline, particularly complex beam paths are relevant to this project
### Specialist Skills Required
TODO
### Resource and Profile Estimate
TODO
### Risks if Not Addressed
TODO
### PMB Approval and Comments
#### Approval Date 
#### Comments

## Workspaces
### Motivation
Described in section 5 [ORNL 5-year plan](https://github.com/mantidproject/documents/blob/master/Design/ORNL_Mantid_5yearplan.pdf). Current data Structures no longer accurately reflect the science. Abuse of `MatrixWorkspace` as a base container in many areas of the codebase.
### Blocking Projects
No blockers
### Specialist Skills Required
TODO
### Resource and Profile Estimate
TODO
### Risks if Not Addressed
* Continued accumulation of technical debt related to shoehorning of `MatrixWorkspace`
* Missing API correctness. Confusion imposed on users with current structures.
* May prevent distributed data reduction for multidimensional data
### PMB Approval and Comments
#### Approval Date 
#### Comments

## Distributed Data Reduction MD
### Motivation

ESS data-reduction-report 2017. Correctness, portability and performance and [ORNL 5-year plan](https://github.com/mantidproject/documents/blob/master/Design/ORNL_Mantid_5yearplan.pdf) section 9.1.

Currently no distributed approach to working with `MDWorkpaces`. Many data redution workflows will spend significant amounts of their total processing effort working with `MDWorkspaces`. There is a signficant conceptual challange here, particularly for `MDEventWorkspaces`

### Blocking Projects
We reccommend that Workspace design is approach, first, particularly taking into account of the [ORNL comment]((https://github.com/mantidproject/documents/blob/master/Design/ORNL_Mantid_5yearplan.pdf)) in section 5 regarding investigation of VTK type data structures.
### Specialist Skills Required
TODO
### Resource and Profile Estimate
6-36 months for 1FTE depending on complexity of solution by ESS estimates
### Risks if Not Addressed
* There are between 6-36 months of estimated effort for this item. It cannot be simply retrofitted if required in short order.
* For Direct Inelastic and SCD, MD processing is the rate determining step. Distributed data reduction for the 2D apsects will not obviate the need for this.
### PMB Approval and Comments
#### Approval Date 
#### Comments

## Project Structure: Python vs C++ with extensions
### Motivation
Mantid is currently a C++ project that has a python interface, with this original design Python could be one of many API's or interface languages, however it makes it harder to integrate as well with some aspects of Python.
The project could be restructured as a Python project with some C++ extensions where necessary.

This work package should include an evaluation of he advantages and disadvantages of each approach.
Whichever approach is taken it should also include work to harmonize the code structure within C++, Python and algorithm categories within Python, and improvements to the python API to make getting data to and from workspaces and python easier and more efficient. 
### Blocking Projects
TODO
### Specialist Skills Required
TODO
### Resource and Profile Estimate
TODO
### Risks if Not Addressed
TODO
### PMB Approval and Comments
TODO
#### Approval Date 
TODO
#### Comments
TODO

## Lazy loading NeXus files
### Motivation
TODO
### Blocking Projects
TODO
### Specialist Skills Required
TODO
### Resource and Profile Estimate
TODO
### Risks if Not Addressed
TODO
### PMB Approval and Comments
TODO
#### Approval Date 
TODO
#### Comments
TODO

## Uniform approach to interacting with NeXus (or just HDF5)
### Motivation
TODO
### Blocking Projects
TODO
### Specialist Skills Required
TODO
### Resource and Profile Estimate
TODO
### Risks if Not Addressed
TODO
### PMB Approval and Comments
TODO
#### Approval Date 
TODO
#### Comments
TODO

## Replace MD with appropriate VTK data structure
### Motivation
Provides a distributed AMR data structure
### Blocking Projects
TODO
### Specialist Skills Required
TODO
### Resource and Profile Estimate
TODO
### Risks if Not Addressed
TODO
### PMB Approval and Comments
TODO
#### Approval Date 
TODO
#### Comments
TODO
