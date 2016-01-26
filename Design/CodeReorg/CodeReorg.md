# Codebase Restructure #

## Motivation ##

The current structure of the codebase has remained largely unaltered since the project's inception, with the exception of the addition of a few library directories and minor directory relocations. The main drivers for considering a restructure of the codebase are:

- Improving code reusability: A lot of code is current locked in algorithm classes in separate libraries leading to code duplication
- More requirements for dedicated GUIs will require a much better library of reusable widgets
- Greater usage of mantid on headless machines requires separate packages for "framework", "gui", etc

## Requirements ##

### Must Haves ###

### Could Haves (Future considerations) ###

## Selected Use cases ##

## Current Structure ##

## Proposed Solution ##

## Solution Details ##

Simple tasks:

- Remove `UserAlgorithms` from being built and shipped with Mantid. This will include removing the development headers from the Windows package. Keep the source code but rename to `Examples`
- Move `Doxygen` to `docs`
- Remove `MatlabAPI`
- Either move `PostInstall` up to project root or find a better way to compile the python files for the packages.
- Move `Properties` directory to a "resources" directory at the top level

### Root-directory Structure ###

The proposed root-directory structure is as follows:

    -/
     -cmake/
     -devtools/
       -buildconfig
       -tools
     -docs/
     -framework/
     -instrument/
     -qt/
       -applications/
         -mantidplot/
	   -qtpropertybrowser
	   -paraviewext
     -resources/
        -fonts
        -images
        -properties
     -scripts/
     -testing/
       -data
     -thirdparty/

### Framework ###

Notes:

Old geometry should go in a `legacy` directory
