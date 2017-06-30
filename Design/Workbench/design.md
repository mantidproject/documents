Summary
=======

This document describes the design of the new matplotlib-based workbench that will replace MantidPlot.

Workflow
========

The new workbench will be developed on a long-running feature branch within the main [`mantid`][mantidrepo] repository. The exception to this is the new directory
structure described below for the graphical components. These changes will be made on the `master` branch prior to any work starting on the workbench. This
will minimize the effect of merge conflicts on existing components that are going to be reused.

The advantage here is that we can remove the existing MantidPlot on this branch and reuse the name for the new workbench.

User Testing
============

During development we will require a small group of actively engaged users to test drive the new interface to ensure we are
developing it as expected.

As the development is occuring on a long-running feature branch we will need a separate set of packages to be able to give to users. It is proposed that we
use the same suffix system that is currently used for the linux packages but for all environments. A package called `mantid-guibeta` can be generated
that will install to different default locations on Windows/macOS and in `/opt/mantid-guibeta` for Linuxes. These packages will not alter the user environment
in any way and will not create desktop shortcuts in case they are confused with the current C++ version.

The beta-testers will have to run the program by navigating to a given directory and running a script/executable.


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

Technologies
============

The workbench will be written primarily in Python using:

 - [PyQt5][PyQt5]
 - [matplotlib][matplotlib_org]
 - [IPython][IPython]

`sip` will be used for exporting any required C/C++ to Python.

Python 2/3
----------

Due to the requirement to support RedHat 7 we will continue to write Python 2/3 compatible
code.

PyQt shim
----------

An abstraction layer around `PyQt4`, `PyQt5`, `PySide` will be used to wrap all calls to PyQt functionality. This should reduce
portability concerns in the future when its inevitable that a PyQt6 will come out. The shim should provide a similar layer
of protection as it currently does between `PyQt4` & `PyQt5`.

We could either write our own, use those provided by other dependencies: [matplotlib][matplotlib_qtcompat], [IPython][IPython] or
use a separate package such as [qtpy][qtpy] provided by the [Spyder][Spyder] developers.


<!-- Link Definitions -->

[mantidrepo]: https://www.github.com/mantidproject/mantid
[matplotlib_org]: https://matplotlib.org/
[matplotlib_qtcompat]: https://github.com/matplotlib/matplotlib/blob/master/lib/matplotlib/backends/qt_compat.py
[PyQt5]:https://riverbankcomputing.com/software/pyqt/download5
[IPython]: https://ipython.org/
[qtpy]: https://pypi.python.org/pypi/QtPy
[Spyder]: https://github.com/spyder-ide/spyder
