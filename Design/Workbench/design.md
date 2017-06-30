Summary
=======

This document describes the design of the new matplotlib-based workbench that will replace MantidPlot.

Workflow
========

The new workbench will be developed on a long-running feature branch within the main [`mantid`][mantidrepo] repository. The exception to this is the new directory
structure described below for the graphical components. These changes will be made on the `master` branch prior to any work starting on the workbench. This
will minimize the effect of merge conflicts on existing components that are going to be reused.


Directory Structure
===================

The following diagram indicates the proposed directory structure for the graphical components.

```
mantid.git
   |-- Framework
   |-- ui
   |   |-- applications
   |   |   |-- mantidplot
   |   |-- algorithm_dialogs
   |   |-- paraview
   |   |-- scientific_interfaces
   |   |   |-- CMakeLists.txt
   |   |   |-- Diffraction
   |   |   |   |-- PowderDiffractionReduction
   |   |   |   |   |-- Powder_Diffraction_Reduction.py
   |   |   |   |   |-- Powder_Diffraction_Reduction
   |   |   |   |   |   |-- ...
   |   |   |-- Indirect
   |   |   |   |-- Common
   |   |   |   |-- Corrections
   |   |   |   |-- DataAnalysis
   |   |   |-- Muon
   |   |   |   |-- ALC
   |   |   |   |-- DataAnalysis
   |   |   |-- Reflectometry
   |   |   |   |-- ISISReflectometry
   |   |   |   |   |-- ISIS_Reflectometry.py
   |   |   |   |   |-- ISIS_Reflectometry
   |   |   |   |   |   |-- ...
   |   |-- mantidui # will become the mantidui python module
   |   |   |-- pyplot
   |   |   |-- widgets
   |   |   |   |-- common
   |   |   |   |-- reduction_gui # Python reduction gui framework
   |   |   |   |-- instrumentviewer
   |   |   |   |-- spectrumviewer
   |   |   |   |-- sliceviewer
```

Packaging
=========

Python
------

The framework package will remain separate and called `mantid`.

The new ui package will be called `mantidui` and have the following submodules:

 - mantidui.pyplot: contain custom plotting code based on matplotlib, i.e keep/make current behaviour, custom toolbars, custom figure window
 - mantidui.widgets: contain these set of reusable widgets used to build the workbench & its components



Beta Testing
============

<!-- Link Definitions -->
[mantidrepo]: https://www.github.com/mantidproject/mantid
