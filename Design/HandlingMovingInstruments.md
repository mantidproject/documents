Handling instruments with moving components
===========================================

Introduction
------------
The purpose of this design document is to form a top level discussion of a better handling of data coming off instruments with moving components. The initial version of this design document includes outcomes from discussions from the development workshop 2015. 

Motivation
----------
Mantid can already handling instrument with moving components, to an extent, by associating the position of a component with a log entry. Specifically this is done in an Instrument Definition File (IDF) using the notation: 
```xml
<parameter name="x">
  <logfile id="trolley2_x_displacement" extract-single-value-as="position 1" />
</parameter>
```
This example reads: take the first value in the log-file `trolley2_x_displacement` and use this value to overwrite the `x` position of a component.

The current limitation of this approach is that only one position value is calculated from a log-file time series.  Hence, by default this approach will not handle the case where different data in a file are associated with different geometry orientations of the instrument. The later can be handed, post loading of data, by taking a workspace of data and split it up into a series of workspaces, where each such workspace only contains data with log-file values from one geometry orientation of the instrument (and where these new log-file values have been used to update the instrument geometry). 

Here proposals are discussed for extending Mantid to include one or more workspaces where different data they contain are associated with different instrument geometries. 

Note an outcome may well be that different such workspaces may be used for different use cases.

Suggestion 1
------------
When a data file is loaded, a MatrixWorkspace is created, which stores an extended instrument which has been created from a base instrument during the loading of the data file, and ensuring that each spectrum in the created workspace is associated with a unique detector or monitor. The advantage of this approach is that all algorithms currently working with MatrixWorkspaces will also work for this workspace. A disadvantage include that the instrument in the instrument view will show all instrument geometries in one view. A question is how to determine during load time which data are associated with which instrument geometry. Bespoke solutions may be needed for different data files and instruments. The question of the handling of monitor data also needs to be addressed. 

Suggestion 2
------------
When a data file is loaded, a MD-workspace is created, where each data point is associated with an instrument geometry. Disadvantages include the current limited support for MD-algorithms and no current support for the visualisation of such workspaces in instrument view.

Suggestion 3
------------
Added addition support for ‘splitter’ algorithms, which create a GroupWorkspace of workspaces, where each of these workspaces only contains data from one instrument geometry. The output from a ‘Load’ may, for some use cases, be outputted in this way.

Suggestion 4
------------
Extend how Mantid can query the position of a component, where a log entry contains information about the whereabouts of a component. At present, if you know the names of such log entries, you can go and query these directly. However the question is whether we should store in a workspace, which components are associated with log entries that contain component whereabouts information. At present we don’t do this. If a method of the workspace was available to ask about this information, it could for example be used to ask: where was the instrument at a specific time. For example in the instrument view you could allow the user to view the instrument geometry at a specific time, or all different instrument geometries between two time values (which perhaps some upper limit of the number of instrument geometries displaced)
