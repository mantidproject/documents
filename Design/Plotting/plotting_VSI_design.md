
Introduction
============

Purpose: This document describes the detailed design of a command line
interface (CLI) for python control of plotting in the VATES simple
Interface (VSI).

Objectives
===========

A former design document
(https://github.com/mantidproject/documents/blob/master/Design/Plotting/plotting_cli.md)
identified the objectives for a new and expanded Python CLI.  The VSI
was listed as one of the items in the functionality that should be
provided. At present the VSI is not exposed to Python at all. Having scritablility features will vastly improve the user experience of this tool, as well as the entire MD toolset. The overall
objective here is to provide a Python CLI to control plotting and/or
visualization in the VSI.

Detailed Objectives
===================

The following functionality should be provided:

1. Control which workspaces are to be shown.
1. Add additional workspaces (peaks workspaces) perhaps through a
  setPeaksWorkspaces feature, like the current SliceViewer python
  export has.
1. Control which view-mode is used for the display
1. Orientation. Perhaps using 2 of the reciprocal lattice vectors.
1. Zoom to region. Zoom to peak will be handled separately.si
1. Control axis mapping. What dimensions in the workspace are going to
  be mapped to which axes? I.e if I have 4 dimensions, Qx,Qy,Qz,dE I
  might want Qx along x and dE along y, Qy along T and Qz along z. The SliceViewer already implements this kind of behaviour.
1. Rotation around the aforementioned orientations.
1. Control background colour
1. Control colour scale range, as well as what 'scalar-array' to show,
  but assume that the default for the scalar array is called
  'signal'. Allow log scaling
1. Take a screenshot. Plot slice allows this and it would be useful to
  us.
1. Switch dimension axis on


Solution Overview
===============================

TODO: check and develop these points.

* We should follow a matplotlib-like style as far as possible, as it
  was done for the basic plotting interface (currently provided by the
  **mantidplot.future.pyplot** module). This includes naming conventions,
  keyword arguments, and as many elements as we can borrow from
  matplotlib (for example handling of colour bars).

* As in **mantidplot.future.pyplot** it should be possible to identify
  workspaces by their names and their Python object.

* The new package will provide an object-oriented (OO) and a
  functional interface, both providing equivalent functionality, as it
  was done in future.pyplot. New classes, like View, Colorbar will be
  introduced.

* The VSI interface functionality will be included in a new
  subpackage: mantidplot.VSI.

* All the visualization functionality, whether currently available in
  the VSI or not, will be exposed to python through the VSI (rather
  than using some of the ParaView python modules, like paraview.simple
  paraview.servermanager, etc.).

Overall Design
===============

TODO: classes and functional blocks. Maybe also give a brief about the
main features of the ParaView Python module that this design builds
on.

Hig level classes to be introduced (not a full list):

- **Pipeline**, representing a VSI/ParaView pipeline.
- **Figure**, representing a VSI/Paraview window. We keep this as consistent as possible with Matplot lib. Change of basis for example may be controlled by manipulating the figure, as well as other axes operations that should carry across all views.
- **View**, representing a VSI/ParaView/VTK view, as obtained for example
  from `paraview.simple.GetRenderView()` or
  `paraview.servermanager.RenderView()`, which will be wrapped into a
  class with limited interface for the moment.
- **Colorbar**

At the moment, only one VSI window can be open at a time. This will change in the near future.

General points considered in the design:

- In the OO interface much of the functionality will be provided
through methods of the View class. The Figure class will provide the
same methods, which by default will operate on the first (only) view
included in each Figure.

- In the functional interface, the functions implicitly modify the
current view (as obtained from `paraview.simple.GetRenderView()`), as
an analog to the 'current figure' concept that is used in matplotlib
and future.pyplot.

- Naming conventions (and as far as possible names of classes and
methods) will be taken from matplotlib. Do the same with the names of
functions and equivalent OO methods. For example: `savefig()` ->
`fig.savefig()`; `xlim()` -> `fig.ax[0].set_xlim()`

- Use keyword arguments wherever convenient and/or possible.


Typical Example Usage
=====================

It should be possible to add a new workspace into a new pipeline using
a plot command like this:

```python
pipelines = plot(ws_source)
```

The command returns a list of Pipeline objects. Here it is assumed
that `ws_source` is a workspace or a workspace list, where every
workspace can be identified by its name or by the Python object as
retrieved from the Mantid Analysis Data Service (with for example `mtd['name']`). It is also
assumed that we have an implicit `view` object of `View` class that
represents the render view included in the VSI/ParaView window.

Here is an example of typical usage with the functional interface:

```python

mdws1 = Load('SEQ_MDEW.nxs', OutputWorkspace='SEQ_MDEW')
peaks1 = Load('peaks_qLab.nxs', OutputWorkspace='peaks_qLab')

pipelines = plot([mdws1, peaks1], hold='on')
set_view_mode('standard')
setp(bgcolor='gray')
view_down((0, 1, 0), 1.5)
center_at((0.2, 0.3, 0.5))
savefig('example_vis.png'

mdws2 = Load('MDworkspace.nxs', OutputWorkspace='SEQ_MDEW')
pipes2 = plot(mdws2, hold='on')
...
```

An equivalent example now using the OO interface would look like this:

```python

mdws1 = Load('SEQ_MDEW.nxs', OutputWorkspace='SEQ_MDEW')
peaks1 = Load('peaks_qLab.nxs', OutputWorkspace='peaks_qLab')

pipelines = plot([mdws1, peaks1], hold='on')
view = pipelines[0].get_view()
fig = view.get_figure()
 # the following methods should be callable on the figure and the view
view.set_view_mode('standard')
view.set_bgcolor('gray')
view.view_down((0, 1, 0), 1.5)
view.center_at((0.2, 0.3, 0.5))
view.savefig('example_vis.png')

mdws2 = Load('MDworkspace.nxs', OutputWorkspace='SEQ_MDEW')
pipes2 = plot(mdws2, hold='on')
...
```

Example Usage of More Specific Functionality
============================================

Control workspace to be shown
-----------------------------

Workspaces are added into parallel VSI/ParaView pipelines with the
plot command, which returns the current list of pipelines.  Whether
they are shown together with the previously shown ones or not is
controlled via the `hold` argument, as in x-y plots in future.pyplot
and following a matlab/matplotlib convention.

The first version of future.pyplot introduced two plotting tools:
'plot_spectrum' and 'plot_bin', and the general command `plot` uses
`plot_spectrum` as default for MatrixWorkspaces.

Here, the `plot` command will be modified so that it defaults to use
the `vsi` tool for PeaksWorkspaces and MDWorkspaces with 3 or more
dimensions. The default for MDWorkspaces with two dimensions will be
`plot_spectrum`

The following examples are equivalent, assuming that the workspace has
3 or more dimensions:

```python
plot(mdws1)
```

```python
plot_vsi(mdws1)
```

```python
plot(mdws1, tool='vsi')
```

Add workspaces
--------------

Additional workspaces can be plotted with the same plot command. A new
pipeline is created for new workspaces, and they are shown together
with previously shown workspaces if the `hold` parameter is set to
'on'.

```python
plot(mdws2, hold='on')
```

Control which view-mode is used for the display
-----------------------------------------------

Two equivalent alternatives can be used here:

```python
set_view_mode(`multislice`)
```
```python
setp(view_mode=`multislice`)
```

For this we introduce four names for the different view modes:
- `standard`
- `three_slice`
- `multislice`
- `scatter_plot`

Control background colour
-------------------------

There are multiple alternatives drawn from matplotlib, and in
principle we could support all of them:

Use the `bgcolor` keyword in commands like add_workspace.

```python
set_bgcolor('gray')
```

```python
setp(bgcolor='r')
```

Note that in this matplotlib can be a bit confusing, as there are
different names for the 'background' color in different modules,
including 'bgcolor', 'facecolor' and things like 'axisbg'. You have
`add_subplot(111, axisbg=".6")`, `figure(facecolor=".6")`, or
`rcParams["figure.facecolor"]`. If we ever support style sheets we
might want to use 'facecolor' there for consistency with
mantidplot. This is supposed to be its technical name.

Control colour scale range
--------------------------

Here it is also required to control what 'scalar-array' to show, but
assume that the default for the scalar array is called 'signal'. Allow
log scaling.

TODO: a `Colorbar` class needs to be introduced at least.


Take a screenshot
-----------------

Here we use essentially the same interface as in future.pyplot:

- Functional variant:
```python
savefig('example_saved_vsi_figure.png')
```

- OO variant:
```python
fig.savefig('example_saved_vsi_figure.png')
```

Switch dimension axis on
------------------------

For this we introduce the `view_down` command, with the following
syntax: `view_down(axes, magnitude)`. The second parameter is
specificed as a factor or fraction.

```python
view_down((1,0,0))
view_down((-1,0,0), 2)
```

More specific commands to modify the view
-----------------------------------------

TODO: this section might need a bit more of
discussion/thinking/feedback.

The following functionality and commands would approximate fulfil the
last three points listed above in the detailed objectives.

- Set the projection frame TODO: clarify what options are/can be available.

```python
fig.set_projection_frame()
```

```python
set_projection_frame()
```

- Zoom in/out: use the command `zoom(factor)`, where
`factor` is a real number

- Center view at a point: use the command `center_at(point)`, where
  point is a coordinates triplet.

- Rotate an angle: use the command `rotate(angle)` where angle is a
  triplet, `angle=(a, b, c)`, and the `a` component correspond to the
  axis that has been set in the last `view_down` command. Additional
  commands could be provided to rotate around every axis: `rotate0`,
  `rotate1`, `rotate2`.

- Control the axis mapping in plot commands. This could be achieved
  via a `xyzdim` keyword argument which would take a triplet value:
  what to put along x, what to put along x-y, and what to put on the
  perpendicular to x-y.
