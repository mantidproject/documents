## Requirements document for generalized superplot-like functionality

### Superplot

Superplot (LAMP) is a data comparison tool which offers convenient overplotting of multiple 1D curves originating from one or more workspaces. These can be spectra, data in single bin (i.e. vs vertical axis) or, without loss of generality, 1D slices of arbitrary MD data. The key elements are the sliders (scrollbars): one to switch the spectrum index and another one to switch the index of the workspace itself. The sliders are accompanied with a hold button to keep the current 1D curve on the plot. Without holding it will simply plot the current spectrum of the current workspace. Once a curve is held, changing either of the sliders will overplot the current curve over the held one. You can see the original tool in action [here](https://mailout.ill.eu/attach/download.php?uoy=NDZlNWJkOTg1NGMyMDY2Mzg5N2EwZTA1NjVmNDJjYWU=). 

### Tools in Mantid

The tools mantid offers currently are mostly suited for inspection of single workspaces. This makes comparison of several workspaces not so convenient. This applies not only to curves and overplotting, but to other tools as well. For example, for a visual comparison of instrument views of two workspaces one has to open two individual instances of the instrument viewer over the two workspaces. However, particularly for SANS, one might want to quickly scroll through different samples having a fixed perspective in the instrument view. For data overplotting, there is a DataComparison GUI (Interfaces->General) which offers very limited functionality. Moreover, one has to add the workspaces manually one by one. 

### Proposed solution

A general solution could be to extend all the visualisation tools to handle multiple workspaces. When opening a tool over a selection of workspaces or a WorkspaceGroup, the tools can start with the view of the first workspace in the list and have a slider over the workspaces in the selection. This will allow to browse over workspaces without changing the perspective/slice/zoom or other configurations of the visualisation. This will also avoid having multiple instances of the tools which are hard to manage for a large number of workspaces. 

For overplotting of multiple 1D curves, a hold button next to the slider will also be required. The hold button must have a binary state Hold/Unhold that should be cached for each workspace index in the list. When clicking on Hold, the widget can auto-assign a color, and put the curve in the legend correspondingly.

When plotting a spectrum from a WorkspaceGroup, all the curves are overplotted by default. In this case also the plot window can host the slider and the button to offer more flexible overplotting.

### WorkspaceSliderWidget

The widged should contain a slider over the workspaces in the selected set (WorkspaceGroup or just a homogeneous collection of workspaces in ADS), and an optioinal Hold button with binary state for each value of the slider.

### Tools to extend

- SpectrumViewer
- InstrumentViewer
- SliceViewer
- Regular plot
- Color fill plot
- Others?
