
Introduction
============

Purpose: This document describes the detailed design of a command line
interface (CLI) for python control of plotting in the VATES simple
interface (VSI).

Objectives
===========

A former design document
(https://github.com/mantidproject/documents/blob/master/Design/Plotting/plotting_cli.md)
identified the objectives for a new and expanded Python CLI.  The VSI
was listed as one of the item in the functionality that should be
provided. At present the VSI is not exposed to Python. The overall
objective here is to provide a Python CLI to control plotting and/or
visualization in the VSI.

Detailed Objectives
===================

For a start, the following functionality should be provided:

* Control which workspaces are to be shown.

* Add additional workspaces (peaks workspaces) perhaps through a
  setPeaksWorkspaces feature, like the current SliceViewer python
  export has.

* Control which view-mode is used for the display

* Control background colour

* Control colour scale range, as well as what 'scalar-array' to show,
  but assume that the default for the scalar array is called
  'signal'. Allow log scaling

* Take a screenshot. Plot slice allows this and it would be useful to
  us.

* Switch dimension axis on

The points listed above would be enough for a first implementation
stage. Other points to consider later on would be:

* Zoom to region. Describe a point to zoom to, perhaps with a zoom factor too.

* Control axis mapping. What dimensions in the workspace are going to
  be mapped to which axes? I.e if I have 4 dimensions, Qx,Qy,Qz,dE I
  might want Qx along x and dE along y, Qy along T and Qz along z.

* Rotation. Not sure how best to express this.


Solution Overview
===============================

TODO: check and develop these points.

* We should follow a matplotlib-like style as far as possible, as it
  was done for the basic plotting interface (currently provided by the
  mantidplot.future.pyplot module). This includes naming conventions,
  keyword arguments, and as many elements as we can borrow from
  matplotlib (for example handling of colour bars).

* As in mantidplot.future.pyplot it should be possible to identify
  workspaces by their names and their Python object.

* Do we stick to a OO interface? To control VSI objects it seems
  logical to me.

* The VSI interface functionality will be included in a new
  subpackage: mantidplot.VSI.

Overall Design
===============

TODO: classes and functional blocks. Maybe also give a brief about the
main features of the ParaView Python module that this design builds
on.

Typical Example Usage
=====================

TODO: fill in examples here and in the sections below, and add
complete list of examples.

```python

```

Example Usage of More Specific Functionality
============================================



Control workspace to be shown
-----------------------------


```python

```

Add workspaces
--------------

```python


```
