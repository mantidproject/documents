
Introduction
============

Purpose of this Document: This document describes the detailed design of the new CLI for python control of plotting in the MantidPlot application.
 
Objectives
===========

The Scientific Steering meeting of 2014 highlighted some major issues around the current plotting in MantidPlot. Some of these issues relate to the command line interface (CLI). A full listing of the points can be found here: http://www.mantidproject.org/SSC_2014_Mantid_General. The objective will be to provide a better CLI following the advice and comments provided by instrument scientists. 

Detailed Objectives
===================

*	Want simpler control over the plot options
*	Want a limited number of plot options. For the default new CLI configuration.
*	Want a 'familiar' feeling CLI for plotting. For example MatPlot, or MatPlotLib
*	Want a cohesive command set. Individual tools should not have their own unique style and rule set.
*	We should maintain backwards compatibility with current qtiplot as many interfaces will break if not. At least during the inital roll-out
*	Additional top-level plot command that will inspect the data and plot it in the most sensible form.
*	Plot should take an optional tool input, to select which plotting tool to use.
*	plot{...} variants to have a common set of controls, such as for setting log scale, and controlling individual graphs
*	Overwrite plot{...} variants to return a user-friendly plot object
*	Add plotInstrument option
*	Consider python control for future interface exposure such as VSI and tile view. Although the immediate concerns will not involve any additional exposure of UIs.
*	*	Want the ability to switch plotting style/implementation. Ensure that no changes are made that would impede us from support more than one plotting interface. For example Horace style plotting.

Plotting Functionality to Replicate
===================================

The new plotting CLI must deliver analogues for the following functionality:

| Plot command  |
| :-----------: |
| plotSpectrum  | 
| plotBins      | 
| plot          | 
| plot          | 
| plot          | 
| plot          | 
| plot          | 
| plot          | 

Solution Overview
===============================
* We will base the new style CLI on MatPlotLib. 
* Support both a MatPlot style functional methodology, as well as an OO methodology. MatPlotLib already has a very good model for doing this.

Typical Current Example Usage
===============================

plot_handle = plotSpectrum(source=[{Workspaces}], indices=[{Indexes}]) 
graph = plot_handle.activeLayer()
graph.logLogAxes()

Prototype example usage
===============================

Plot
----

Plot will choose the most appropriate registered plotting tool to perform the job, unless the *tool* argument is provided. **kwargs hide the large number of options that would have to be registered for all the plotting tools.

```python
plot(source=[{Workspace}], tool={ToolName}, **kwargs)
```
Return: return type will determine of the exact tool chosen. For example plot_spectrum and plot_bin (see below) would return a tuple of Line2D objects.

Plot Spectrum
-------------

```python

line_2ds = plot_spectrum(source=[{Workspaces}], indices=[{Indexes}]) 

```
Return: Matplotlib.pyplot plot commands return a tuple of objects to represent every line plotted. Our plotting tools should do the same.


Plot Instrument
---------------

```python
instrument_view = plot_instrument({Workspace}, **kwargs)
render_tab = instrument_view.getInstrumentTab()
```

Plot Slice
----------
```python
slice_viewer = plot_slice([{Workspace}], **kwargs)
```

