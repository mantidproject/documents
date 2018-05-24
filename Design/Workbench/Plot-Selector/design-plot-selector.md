# Plot Selector Widget

## Requirements

The request from the January 2018 user meeting was to have a widget that allowed easy switching between plots, in particular for SANS and Reflectometry users. Another request from the ILL was to have a method to easily arrange the plots.

For consistency the design should follow as closely as possible similar functionality in Mantid, such as the workspace selector and plotting options within the workspace selector.

## Functional Design

### Interface Design

For consistency the plot selector widget should follow a similar design to the workspace selector. Double-clicking a plot name will bring the plot to the foreground and make it the active one.

![Plot Selector Widget](plot_selector.png)

**All plots created from the workbench are shown in the list.** Double-clicking a plot will bring it to the foreground. Filtering works as for the workspace selector. Close can act on one or more selected plots.

![Menu Options](menu_options.png)

**This figure shows the menu options for New, Arrange, Sort and Export.** New allows a choice of plot types, the same selection as for right-clicking a workspace. Arrange allows all plot windows to be cascaded or tiled. Sort allows sorting by name or last modified, ascending or descending. Export allows all selected plots to be exported to commonly used file types.

![New Plot Workspace Selection](new_plot.png)

**Selecting a new plot will then prompt for which workspace to plot.** Selecting multiple workspaces should give the same behaviour as selecting multiple workspaces in the workspace selection widget (e.g. same plot for 1D, side-by-side for 2D).

![Right-Click Menu](rightclick_menu.png)

**Right-clicking on the plot name will bring up a menu with some options.** The options are to make the plot active, rename it, export the plot or close the plot.

### Priorities for Implementation

Essential for workbench prototype:

* List of plots
* Double-clicking a plot brings it to the foreground and makes it active
* Right-click gives the option to bring the plot to the foreground and make it active
* Filtering plots based on name (for consistency behaviour should be the same as the workspace widget - filtering based on any sub-string)

Nice to have:

* Selecting one or more plots and clicking close closes selected plots
* Right-click menu option to close plots
* Right-click menu option to rename plot
* Option to sort by either name or last modified plot, ascending or descending
* Export to export plots a useful subset of supported types
* Right-click menu to export plot
* New option to create a plot from the plot selector
* Arrange option to tile or cascade the current open plots (this could be investigated further to see if anything nicer can be done here to arrange the plots)

Ideas for the future:

* Mini-plot next to the plot name (a la LAMP)
* Plot preview when hovering over the plot name
* Details of the plot as for the workspace selector

## Technical Design

The design should follow the model-view(widget)-presenter design used elsewhere in the new workbench - see [workbench architechtural design](../design-arch.md).

### Access to Plots

Access to a list of figures can be obtained from `qt/applications/workbench/workbench/plotting/currentfigure.py`. This code is currently being refactored to change the Hold/Active functionality. Some form of observer pattern will be required to update the Plot Selector when new plots are made via the `set_active` method. This covers all plots created in the workbench, including those directly created in matplotlib.

To get easy access to the plots the initial implementation will be in the workbench, under a new widgets directory - `qt/applications/workbench/workbench/widgets`. If there are no technical barriers this could eventually be moved into the directory containing the standalone widgets.

