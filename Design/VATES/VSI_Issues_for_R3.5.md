# Multidimensional Plotting Tasks for Release 3.5

This documents aims to keep track of the required tasks which need to be addressed for the current release (3.5).

This will allow us to have an overview of the status quo and how to channel our efforts. Please add your issues to this document and change priorities if needed. Also if you think that we won't resolve something for this release, then add/move it to the [Resolve later](#resolve-later) section.

## Currently being looked at


## Tasks
### Priority High 

##### ~~GIL compatibility with ParaView for LaTeX style labels~~
Owner: Martyn  
Resolve Python issue with LaTeX in VSI

##### ~~Check if items of the Kitware contract have been implemented~~
Owner:  Owen
Go through the list of deliverables and check if they have been implemented (see contract)

##### ~~Cut then Scale issue~~
Owner: Anton  
Currently we can scale and then cut, but there is an issue if we reverse the order. See [here.](https://github.com/mantidproject/mantid/issues/12368)

##### ~~Artifacts when changing size~~

Owner:  Roman

When we change the size of the VSI the rendered view does not update. A similar effect happens when we use the PeaksTable in the Splatterplot mode. The issue is caused by applying the old state xml file when switching views.

Fixed [here](https://github.com/mantidproject/mantid/pull/13615)

##### ~~Unticking of AutoScale~~
Owner: Anton 
The AutoScale option seems to unselect itself whenever you load data into the VSI. Related to saving the view state.

Fixed [here](https://github.com/mantidproject/mantid/pull/13595)


##### ~~Zero Memory copies~~
Owner: Steven Hahn  
Investigate zero memory copies
Fixed [here] (https://github.com/mantidproject/mantid/pull/13322)

##### ~~Axes and labels improvement~~
Owner: Anton
This will most likely be an umbrella ticket. Some issues are:  
* Axes labels are not being picked up by Axes Grid only by Cube Axes system. vtkPVChangeOfBasisHelper does not seem to be used by Axes Grid --> SOLVED
* The Axes Grid boundaries don't seem to be correct in ThreeSliceView (Axes Grid box is smaller than data set) -->SOLVED
* Currently we have both the Axes Grid and the Cube Axes system. --> This remains, we need to go to a higher PV version
* Provide TeX-like features --> SOLVED (Martyn)
* In Threeslice Mode provide a sensible text size (Note that this will need a newer version of PV.) --> Solved

Fixed [here](https://github.com/mantidproject/mantid/pull/13565)

##### ~~Apply patches to source build of paraview~~
Owner: Steve

##### ~~CutMD in VSI can come back with zero data in it~~
Owner: Owen
We have no ability to remap non-integrated dimensions such that we form a contiguous set of these for generating our 
vtkDataSets. Integrated dimensions interspersed amongst non-integrated dimensions cause empty datasets in the visualisation.
See [here](https://github.com/mantidproject/mantid/issues/12554)

##### ~~Loading an MDHisto Workspaces causes the signal to vanish~~
Owner: Owen/Anton/Andrei
When loading an MDHisto Workspace or using BinMD on an MDEvent Worspace we end up with a constant signal value. This seems to be due to the selection of the normalization. This is down to the AutoSelect normalization behaviour for MDWorkspace types. [#12832](https://github.com/mantidproject/mantid/issues/12832)

### Priority Medium

##### ~~Fix Scale Filter~~
Owner: Owen Arnold
The scale filter should work with any vtkPointSet, such as the newly provided vtkStructuredGrids (above)
Fixed [here](https://github.com/mantidproject/mantid/pull/13528)

## Resolve later

### Priority Medium

##### PipelineBrowser + PropertiesWidget mock ups
Owner:  
Create mock ups for a possible replacement of the pipeline browser and the properties widget

##### Slice position
Owner:  Anton
It was discussed that we should have an input field to define the slice position for the ThreeSliceView. 

##### Implement a 2D text filter for Peaks in Splatterplot
Owner:  
Utkarsh has provided us with a demo for displaying 2D text on a 3D rendered environment. This needs to be integrated with the PeaksViewer in Splatterplot mode (Anton has the demo code).

### Priority Low

##### Multiple Windows/Instances
Owner:  
Provide multiple VSI instances. See [here](https://github.com/mantidproject/mantid/issues/12395).
