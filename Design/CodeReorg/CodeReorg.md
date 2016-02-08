# Codebase Restructure #

## Motivation ##

The current structure of the codebase has remained largely unaltered since the project's inception, with the exception of the addition of a few library directories and minor directory relocations. The main drivers for considering a restructure of the codebase are:

- Improving code reusability: A lot of code is current locked in algorithm classes in separate libraries leading to code duplication
- Speeding up build times by having smaller libraries more focused on specific concepts
- Greater usage of mantid on headless machines requires separate packages for "framework", "gui", etc
- More requirements for dedicated GUIs will require a much better library of reusable widgets

## Requirements ##

Quote from "Large Scale C++ Software Design" by John Lakos - *"Carefully partitioning a system into large units and then considering aggregate dependencies among these units is critical when distributing the development effort for projects across multiple individuals, development teams, or geographical sites."*

### Must Haves ###

- GUI and "framework"-code should be separated
- Framework buildable as an isolated entity
- Framework buildable without any "GUI" packages installed, e.g X11 (Linux)
- Separate Linux packages for headless (framework), GUI
- Includes next to source files makes it easier for some tools & IDEs


## Current Structure ##

See [here](https://github.com/mantidproject/mantid/tree/69588f49e31434895c656e097d41bbaf99c87dce) for a link to state around the time this document was written.

## Proposed Solution ##

Simple tasks:

- Remove `UserAlgorithms` from being built and shipped with Mantid. This will include removing the development headers from the Windows package. Keep the source code but rename to `Examples`
- Move `Doxygen` to `docs`
- Remove `MatlabAPI`
- Either move `PostInstall` up to project root or find a better way to compile the python files for the packages.

### Root-directory Structure ###

The proposed directory structure (without the framework detail) is as follows:

	mantid.git
	|-- cmake
	|-- devtools
	|   |-- buildconfig
	|   |-- tools
	|-- docs
	|   |-- doxygen
	|   |-- sphinx
	|-- framework
	|-- instrument
	|-- qt
	|   |-- applications
	|   |   |-- mantidplot
	|   |   |-- mdviewer (formerly standalone VSI)
	|   |-- paraviewext
	|   |   |-- common
	|   |   |-- paraviewplugins
	|   |-- widgets
	|	|   |-- qtpropertybrowser
	|   |   |-- instrumentview
	|   |-- resources
	|-- resources
	|   |-- fonts
	|   |-- images
	|-- scripts
	|-- testing
	|   |-- data
	|-- thirdparty

### Framework ###

The proposed directory structure for the framework package is as follows:

	framework
	|-- catalog
	|-- common
	|   |-- algorithm
	|   |-- constants
	|   |-- core
	|   |-- datamodel
	|   |-- units
	|-- geometry
	|   |-- legacy
	|-- io
	|   |--
	|-- mpi
	|-- optimization
	|   |-- common
	|   |-- costfunctions
	|   |-- minimizers
	|   |-- models
	|-- neutron
	|   |-- diffraction
	|   |-- inelastic
	|   |-- crystallography
	|   |...
	|-- muon
	|-- remote
	|   |-- live
	|   |   |-- common
	|   |   |-- ess
	|   |   |-- isis
	|   |   |-- sns
	|   |-- cluster
	|   |-- scriptrepository
	|-- resources
	|   |-- properties

Notes:

- each subdirectory will have its own `testing` directory
- the library names will be formed from concatenating directory names togther, e.g. `common/core` would produce `libmantidcommoncore.so`
