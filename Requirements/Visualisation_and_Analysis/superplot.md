## Requirements document for generalized superplot-like functionality

### Superplot

Superplot (LAMP) is a data comparison tool which offers convenient overplotting of multiple 1D curves originating from one or more workspaces. These can be spectra, data in single bin (i.e. vs vertical axis) or, without loss of generality, 1D slices of arbitrary MD data. The key elements are the sliders (scrollbars): one to switch the spectrum index and another one to switch the index of the workspace itself. The sliders are accompanied with a hold button to keep the current 1D curve on the plot. Without holding, it will simply plot the current spectrum of the current workspace. Once a curve is held, changing either of the sliders will overplot the current curve over the held one. You can see it in action here.

### Tools in Mantid

The tools mantid offers currently are mostly suited for inspection of single workspaces. This makes comparison of several workspaces not so ergonomic. For example for a visual comparison of instrument views of two workspaces one has to open two individual instances of the instrument viewer over the two workspaces. There is a DataComparison GUI which however offers very limited functionality.

### WorkspaceGroupIndexWidget

 

### Reference
