## VSI Integration issues
Please see below  a list of issues and how to reproduce them.

### Origin of issue key

Likely Source of Issue | Key 
--- | ---
<a name="ParaView">ParaView</a> |  1
<a name="ParaViewFixed">ParaView already fixed</a> | 2
<a name="Mantid">Mantid</a> | 3
<a name="Unknown">Unknown</a> | 4

### Issues

#### Colour Editor Panel 
When loading starting the VSI a second time, we get a message pop up [1](#ParaView) :

    > Replacing existing manager for function : 
    > "COLOR_EDITOR_PANEL" 

#### Quad View
When switch to QuadView, default grid axis is not on any longer displayed (error message) [3](#Mantid)

#### Cut Filter 
The cut filter does not seem to have the positioning tool any longer with which the user can manually select a plane [4](#Unknown)

#### Cut then Scale
First cut then scale does not work [3](#Mantid)

#### Blanking Arrays
Structured data (MDHisto) requires blanking arrays. The Histo data appears as a big box. Blanking arrays seem to be missing. [3](#Mantid) longer term [1](#ParaView)

#### BinMD 
Remove BinMD is not available any longer for rebinned data (probably an issue with active source) [3](#Mantid) 

#### Restart 
Once output warning report from PV is started, it propagates when VSI is restarted. [1](#ParaView) 

#### Drag and Drop
Cannot add PeakWS through drag and drop; it thinks it is an MDEventWS and crashes(More tests needed in Splatterplot, when we can load  PeakWS) [1](#ParaView), [3](#Mantid) 

#### Cube Axis Visibility
Cube axis visibility does not work any longer. [2](#ParaViewFixed) 

#### Colour Bar
Color bar appears only in SplatterPlot mode. There is no checkbox to enable or disable it. [1](#ParaView)

#### Scale then Cut
Apply scale/cut filter, then go to view settings( or anything that can change the focus). We cannot remove the filter any longer.  [3](#Mantid)

#### Multiple Instances
When loading MDEventWS into the VSI and PeakWS into another instance of the VSI, the color scale of the MDEventWS seems to get messed up. It seems that the instances are NOT independent.  [1](#ParaView)

#### Non Orthongonal
Probable issue with BasisVectors in newer ParaView. API change. [3](#Mantid)

#### Rotation Splatterplot
When loading data into splatterplot, it appears that only translation of the data set is possible no rotation. [1](#ParaView)

#### Non-movable slices
When loading data into the ThreeSliceView (QuadView), we cannot move the slice planes any longer. Trying to move the slice planes just translates the data set.
[1](#ParaView)

#### View settings
When making a change in the view settings panel, it seems that this does not have an effect on the VSI
[1](#ParaView)

#### Default view issue

Found my Andrei "Selected a splatter plot for a histo workspace. Defaulted to standard view." [3](#Mantid)

### Who is working on what?
[Drag and Drop](#drag-and-drop): Anton


### Possible Prioritization:

General thoughts:
* Issues [BinMD](#binmd) and [Scale then Cut](#scale-then-cut) probably exist because we cannot select the correct element of the pipeline. Having the pipeline browser back might solve this.
* Issues [Quad View](#quad-view), [Blanking Arrays](#blanking-arrays) and [Cube Axis Visibility](#cube-axis-visibility) seem to be addressed in later versions of PV.
* Issue [Drag and Drop](#drag-and-drop) is something Anton can try to find out more about.
* Issues [Colour Editor Panel](#colour-editor-panel) and [Restart](#restart) seem to be related and seem to be a fundamental issue with PV. So this is probably something that Utkarsh will be able to understand quickly.
* Issue [Cut then Slice](#cut-then-slice) might be a change of the cut filter design. It is worth that Utkarsh verifies this.
* Issue [Colour Bar](#colour-bar) is something that is probably only related to PV, so it is usfull for Utkarsh to have a look at it.
* Issue [Multiple Instances](#multiple-instances) would require some input from Utkarsh, since it seems that the instances of PV seem to communicate. 
* Issue [Non Orthongonal](#non-orthongonal) relates to a ParaView non-orthngonal-source API change around the vtkFieldData. We can probably fix this ourselves.

In terms of rating the issues for Utkarsh:

  1. Issues [Colour Editor Panel](#colour-editor-panel) and [Restart](#restart)
  2. Issue [Multiple Instances](#multiple-instances)
  3. Issue [Colour Bar](#colour-bar)
  4. Issue [Cut Filter](#cut-filter) 
  5. Issue [Rotation Splatterplot](#rotation-splatterplot)
  6. Issue [Non-movable Slices](#non-movable-slices) 
  7. Issue [View settings](#view-settings)
  8. The other issues in no order


### How to reproduce the issues
* [Colour Editor Panel](#colour-editor-panel) 
  1. Load a sample data set into the VSI
  2. Close the VSI
  3.	Load the sample data set again into the VSI
  4.	Confirm that a pop opens with warnings

* [Quad View](#quad-view)
  1.	Will be dealt with when we remove ShowCubeAxes and set CubeAxesVisibility of the representation as Utkarsh suggested.

* [Cut Filter ](#cut-filter)
  1.	Load a MDEvent sample data set into the VSI
  2.	Swith to Standard View
  3.	Apply the Cut filter
  4.	Confirm that there is no visual slice tool available. There used to be a plane that the user could drag around to define the slice. It is not there any longer.

* [Cut then Scale](#cut-then-scale)
  1.	Load a MDEvent sample data set into the VSI
  2.	Switch to Standard View
  3.	Apply the Cut filter, press OK
  4.	Apply the Scale filter
  5.	Confirm that a PV error message appears

* [Blanking Arrays](#blanking-arrays)
  1.	Load a MDHisto sample data set into the VSI
  2.	Switch to Standard View
  3.	Confirm that it is one big box (it should be a more complex shape). Signals of 0 are replaced by blue boxes

* [BinMD](#binmd)
  1.	Load a MDEvent sample data set into the VSI
  2.	Switch to Standard View
  3.	Press the Rebin button, select BinMD and press Ok
  4.	Confirm that a big box is created (same issue as in Issue5)
  5.	Confirm that when pressing Rebin button, there is no option to Remove rebinning. This should be available, if the active source was a rebinned source.

* [Restart](#restart)
  1.	Load a sample data set into the VSI
  2.	Close the VSI
  3.	Load the sample data set again into the VSI
  4.	Confirm that a pop opens with warnings 
  5.	Switch to the Standard view
  6.	Press Scale button
  7.	Confirm that the pop up with warnings appears and you cannot set the scale filter. 

* [Drag and Drop](#drag-and-drop)
  1.	Load a MDEvent sample data set into the VSI
  2.	Switch to SplatterPlot View
  3.	Drag and Drop a PeaksWorkspace into the VSI
  4.	Confirm that a pop up appears claiming that we try to add an MDEventWorkspace. 
  5.	Confirm that Mantid crashes

* [Cube Axis Visibility](#cube-axis-visibility)
  1.	Load a MDEvent sample data set into the VSI
  2.	Switch to Standard View
  3.	Try to set the cub axes visibility
  4.	Confirm that nothing happens

* [Colour Bar](#colour-bar)
  1.	Load a MDEvent sample data set into the VSI
  2.	Switch between Standard View and SplatterPlot View
  3.	Confirm that the Color bar appears in standard view and not in splatterplot view
  4.	Confirm that there doesn’t seem to be an option to set the color bar

* [Scale then Cut](#scale-then-cut)
  1.	Load a MDEvent sample data set into the VSI
  2.	Switch to Standard View
  3.	Apply a scale filter ( you should still have the option to delete it)
  4.	Press the ViewSettings button in the menu bar
  5.	Confirm that you cannot delete the filter any longer
  
* [Multiple Instances](#multiple-instances)
  1.	Load a MDEvent sample data set into the VSI
  2.	Look at the color scaling of the rendered image
  3.	Load a PeakWorkspace into a separate instance of the VSI, i.e. don’t use the drag and drop feature to load the VSI
  4.	Confirm that the displayed colors of the rendered MDEvent sample have changed. The two VSI instances seem to communicate.

* [Rotation Splatterplot](#rotation-splatterplot)
  1.	Load a MDEvent sample data set into the VSI
  2.	Switch to the splatter plot view.
  3.	Perform usual rotation with the mouse
  4.	Confirm that response is not a rotation, but rather a translation

* [Non-movable Slices](#non-movable-slices)
  1.	Load a MDEvent sample data set into the VSI
  2.	Switch to the three slice view
  3.	Try to shift the slice plane
  4.	Confirm that this only results in a translation of the data set

* [View settings](#view-settings)
  1.	Load a MDEvent sample data set into the VSI
  2.	Open the view settings
  3.	Change the background color and press apply
  4.	Confirm that the background color does not change
