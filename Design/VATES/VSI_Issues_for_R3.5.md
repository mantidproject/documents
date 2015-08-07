# Multidimensional Plotting Tasks for Release 3.5

This documents aims to keep track of the required task which need to be addressed for the current release (3.5).

This will allow us to have an overview of the status quo and how to channel our resources. Please add your issues to this document and change priorities if needed.


## Priority High 


#### GIL compatibility with ParaView for LaTeX style labels
Resolve Python issue with LaTeX in VSI


#### Implement a text filter 2D text next to Peaks
Utkarsh has provided us with a demo for displaying 2D text on a 2D rendered environment. This needs to be developed for the PeaksViewer in Splatterplot mode 

#### Check if items of the Kitware contract have been implemented
Go through the list of deliverables and check if they have been implemented (see contract)

#### Cut then Scale issue
Currently we can scale and then cut, but there is an issue if we reverse the order.

#### Artifacts when changing size
When we change the size of the VSI the rendered view does not update. A similar effect happens when we use the PeaksTable in the Splatterplot mode. The issue is caused by the c

#### Slice position
It was discussed that we should have an input field to define the slice position for the ThreeSliceView

#### Zero Memory copies
Investigate zero memory copies


#### Axes and labels improvement
This will most likely be an umbrella ticket. Some issues are

* Provide TeX-like feautres
* In Threeslice Mode provide a sensible text size


## Priority Medium


#### PipelineBrowser + PropertiesWidget mock ups
Create mock ups for a possibel replacement of the pipeline browser and teh properties widget


## Priority Low

#### Multiple Windows/Instances
Provide multiple VSI instances


## Resolved

* [GIL compatibility with ParaView for LaTeX style labels](#GIL-compatibility-with-ParaView-for-LaTeX-style-labels)


## Resolve later
