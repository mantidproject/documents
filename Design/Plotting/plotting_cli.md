```python
Introduction
============
Purpose of this Document: This document describes the detailed design of the new CLI for python control of plotting in the MantidPlot application.
 
Objectives:
==============
The Scientific Steering meeting of 2014 highlighted some major issues around the current plotting in MantidPlot. Some of these issues relate to the command line interface (CLI). A full listing of the points can be found here: http://www.mantidproject.org/SSC_2014_Mantid_General. The objective will be to provide a better CLI following the advice and comments provided by instrument scientists. 

###	Detailed Objectives
*	Want simpler control over the plot options
*	Want a limited number of plot options. For the default new CLI configuration.
*	Want the ability to switch plotting style/implementation. Ensure that no changes are made that would impede us from support more than one plotting interface. For example Horace style plotting.
*	We should maintain backwards compatibility with current qtiplot as many interfaces will break if not.
*	Additional top-level plot command that will inspect the data and plot it in the most sensible form.
*	Plot should take an optional tool input, to select which plotting tool to use.
*	Overwrite plot{...} variants to return a user-friendly plot object
*	plot{...} variants to have a common set of controls, such as for setting log scale, and controlling individual graphs
*	Overwrite plot{...} variants to return a user-friendly plot object
*	Add plotInstrument option
*	Consider python control for future interface exposure such as VSI and tile view.

##	High-level Proposed Solution(s)
*	Additional top-level plot command that will inspect the data and plot it in the most sensible form.
*	Wrap and extend existing qtiplot python functionality in all cases. Existing behaviour must be preserved until it can be phased out.
*	Use forwarding methods expose the activeLayer functionality to the returned plot handle (MultiLayerPlot  proxy)
*	Possible to have a new 'Facade' type to expose all options. This could be a new type (returned by the plot methods), which encompasses MultiLayerPlot, Graph and Legend, as well as, ErrorBarSettings etc. It would avoid the need for users to drill-down and fetch the relevant objects to access aspects of the control.

##	Current Example Usage
plot_handle = plotSpectrum(source=[{Workspaces}], indices=[{Indexes}]) 
graph = plot_handle.activeLayer()
graph.logLogAxes()

##	Prototype example usage
###	Plot
Plot(source={Workspace}, tool={ToolName}, **kwargs)

Return: Easiest thing to do would be to return whatever it is that the individual tool returns. More complex, but possibly more useful thing to do would be to return some kind of abstraction which would give access to common utilities on all tools.
###	Plot Spectrum
plot_handle = plotSpectrum(source=[{Workspaces}], indices=[{Indexes}]) 
plot_handle.logLogAxes()

Return: current MultiLayer type object (with Graph forwarding methods) or Façade.
Expose common options such as log axis and line colours as function arguments
plotSpectrum([{Workspaces}], [{Indexes}], Axes='LogLogAxes')

###	Plot Instrument
instrument_view = plotInstrument({Workspace})
render_tab = instrument_view.getInstrumentTab()
```
