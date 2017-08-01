Summary
=======

This document describes the layout and high-level details of the new matplotlib-based workbench that will replace MantidPlot.

Workflow
========

The new workbench will be developed on a long-running feature branch within the main [`mantid`][mantidrepo] repository. The exception to this is the new directory
structure described below for the graphical components. These changes will be made on the `master` branch prior to any work starting on the workbench. This
will minimize the effect of merge conflicts on existing components that are going to be reused.

## Merging & Removal of MantidPlot

There will become a point when the new workbench has enough features to be releasable to the general audience as a viable replacement for MantidPlot. MantidPlot would not be removed at
this point until we can be satisfied that the new workbench serves our current users needs. See section in [architeture](design-arch) section regarding widget code shared between MantidPlot
and the new workbench.

Source Code Directory Structure
===============================

The following diagram indicates the proposed directory structure for the graphical components.

```
mantid.git
   |-- Framework
   |-- MantidPlot
   |-- qt
       |-- applications
       |   |-- mantidworkbench
       |-- paraview_ext
       |-- resources
       |-- scientific_interfaces
       |   |-- CMakeLists.txt
       |   |-- Diffraction
       |   |   |-- PowderDiffractionReduction
       |   |       |-- Powder_Diffraction_Reduction.py
       |   |       |-- Powder_Diffraction_Reduction
       |   |       |   |-- ...
       |   |-- Indirect
       |   |   |-- Common
       |   |   |-- Corrections
       |   |   |-- DataAnalysis
       |   |-- Muon
       |   |   |-- ALC
       |   |   |-- DataAnalysis
       |   |-- Reflectometry
       |   |   |-- ISISReflectometry
       |   |       |-- ISIS_Reflectometry.py
       |   |       |-- ISIS_Reflectometry
       |   |       |   |-- ...
       |-- python
       |   |-- mantidqt # python mantidqt module
       |       |-- reduction_gui # Python reduction gui framework
       |       |-- widgets # would contain combine qtwidgetscommon.dll with sip exports to give mantidqt.widgets python library
       |       |-- __init__.py
       |-- widgets
           |-- common # qtwidgetscommon.dll
           |-- plugins
           |   |-- algorithm_dialogs # qtwidgetspluginsalgorithm_dialogs.dll
           |   |-- designer # qtwidgetspluginsdesigner.dll
           |-- instrumentview # qtwidgetsinstrumentview.dll
           |-- spectrumviewer # qtwidgetsspectrumviewer.dll
           |-- sliceviewer # qtwidgetssliceviewer.dll
```

Mapping of the current structure to this is as follows:

 - `/MantidPlot`: NOT MOVED (will be deleted once replacement is up to scratch)
 - `/Vates` --> `/qt/paraview_ext`
 - `/MantidQt/API/` & `/MantidQt/MantidWidgets/` combined --> `/qt/widgets/common`
 - `/MantidQt/MantidWidgets/InstrumentView` --> `qt/widgets/instrumentview`
 - `/MantidQt/RefDetectorViewer` --> `/qt/widgets/refdetectorview`
 - `/MantidQt/SpectrumViewer` --> `/qt/widgets/spectrumviewer`
 - `/MantidQt/SliceViewer` --> `/qt/widgets/sliceviewer`
 - `/MantidQt/CustomDialogs` --> `/qt/widgets/plugins/algorithm_dialogs`
 - `/MantidQt/DesignerPlugins` --> `/qt/widgets/plugins/designer`
 - `/MantidQt/Python` --> `/qt/python`
 - Remove Factory directory as it seems unecessary
 - All resources, fonts, images etc, moved under qt/resources

Shared libraries will follow a naming structure that includes all of their parent directories.

`.ui` files should be kept with the header files of the corresponding classes.

Technologies
============

The workbench will be written primarily in Python using:

 - [PyQt5][PyQt5]
 - [matplotlib][matplotlib_org]
 - [IPython][IPython]

`sip` will be used for exporting any required C/C++ to Python. `boost.python` will be maintained for the framework exports.

See a note in [architecture design](design-arch.md) about Qwt and existing interfaces/widgets.

Python 2/3
----------

Due to the requirement to support RedHat 7 we will continue to write Python 2/3 compatible code.

PyQt shim
----------

An abstraction layer around `PyQt4`, `PyQt5`, `PySide` will be used to wrap all calls to PyQt functionality. This should reduce
portability concerns in the future when its inevitable that a PyQt6 will come out. The shim should provide a similar layer
of protection as it currently does between `PyQt4` & `PyQt5`.

We could either write our own, use those provided by other dependencies: [matplotlib][matplotlib_qtcompat], [IPython][IPython] or
use a separate package such as [qtpy][qtpy] provided by the [Spyder][Spyder] developers. My suggestion would be using [qtpy][qtpy].

Packaging & Deployment
======================

Python
------

The framework package will remain separate and called `mantid`.

The new ui python package will be called `mantidqt` and have the following submodules:

 - mantidqt.plotting: contain custom plotting code based on matplotlib, i.e keep/make current behaviour, custom toolbars, custom figure window
 - mantidqt.widgets: contain these set of reusable widgets used to build the workbench & its components

The workbench will be called `mantidworkbench` and depend on `mantudqt` & `mantid`. In Anaconda We will have the following packages, in addition to the current `mantid-framework` package:

 - `mantid-qt`: gives you `mantidqt` python package
 - `mantid-workbench`: gives you the new workbench

Installation
------------

It is proposed that a new package be generated for shipping the new workbench. The reasons for this are:

* it avoids disturbing the production package at all to provide maximal stability for existing users
* Qt5/PyQt5 will need to be shipped on Windows/OSX and this would explode the current package size if we bundled it there
* we may want to experiment with different versions of packages that we already ship and we don't want to disturb the current application
* it can be a starting point for generating the separate packages on Linux (hand-written spec/debian files??).

For Windows/Mac we will use the same installer technology as we do currently. The packages **must** be able to live alongside a current production or nightly version. The package names suggested are:

* Windows/OSX: mantidpreview - A combined package bundling everthing, much as we currently do. Defaults to a different install location than current
* Linux: `mantidpreview-framework`, `mantidpreview-qt`, `mantidpreview-workbench`: separate packages to allow just dependencies on widgets etc.


Windows Installed Layout
========================

Our windows installation structure is poorly layed out. For example the `bin` directory contains many files and it is difficult to navigate and also contains our Python bundle. A new layout, based on the
[miniconda][miniconda] layout on Windows, is proposed. It is as follows:

```
C:\MantidInstall
  |-- bin
  |-- instrument # instrument definitions
  |-- library
  |   |-- bin # dependent DLLs: boost, poco, core mantid libraries, vtk etc
  |   |-- plugins
  |   |   |-- mantid # Our plugins
  |   |   |   |-- python # python algorithms
  |   |   |   |-- qt
  |   |   |-- pvplugins
  |   |   |-- qt # Qt plugins for image formats etc
  |-- python2.7
  |-- scripts # existing scripts directory
  |-- share
      |-- colormaps
      |-- docs
```

This will require a small patch in `python2.7\Lib\site.py` to add the `library\bin` directory to the `PATH` on startup and also set the `MANTIDPATH` variable.
Anaconda make a similar modification to the `PATH` in their bundled Python installation.


<!-- Link Definitions -->

[mantidrepo]: https://www.github.com/mantidproject/mantid
[matplotlib_org]: https://matplotlib.org/
[matplotlib_qtcompat]: https://github.com/matplotlib/matplotlib/blob/master/lib/matplotlib/backends/qt_compat.py
[PyQt5]:https://riverbankcomputing.com/software/pyqt/download5
[IPython]: https://ipython.org/
[qtpy]: https://pypi.python.org/pypi/QtPy
[Spyder]: https://github.com/spyder-ide/spyder
[Nsis]: http://nsis.sourceforge.net/Main_Page
[QtInstallerFramework]: http://doc.qt.io/qtinstallerframework/
