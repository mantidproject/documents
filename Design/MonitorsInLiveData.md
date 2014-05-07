Design for a new way of handling monitor data in Mantid
=======================================================

Motivation
----------

The background to this document is that a requirement exists that monitor data be available in Mantid's live data toolset. In particular, the SNS live listener (link) needs to be able to pass back the full event-based monitor data since there are certain analyses and tools that require this information.

Current system for handling monitors
------------------------------------

Historically, Mantid has employed two distinct methods of loading and carrying-around monitor detector data. Both methods suffer from significant drawbacks.

1. The monitors are held as additional spectra within the main data workspace. This is the default method used when loading ISIS raw files. The advantage of this is that the data objects are aggregated. However, the strong disadvantage is that at some point the monitor data will have to be split off or extricated from the main workspace.

2. The monitors are loaded into a separate workspace that is stored in the ADS in addition to the workspace containing the main data. The monitor workspace name is set to match that of the data workspace, with "_monitors" appended. Of the two methods, this one is generally preferred - it keeps the monitor data separated, so that it can be processed differently, or not all, without polluting the scattering data itself. A drawback is that the only semantic connection between the loaded workspaces is in their name. This is just a string, so we cannot lean on the type system. Furthermore, it goes against the design philosophy of Mantid for algorithms to have to know anything about a workspace's name.

### Obstacles to using the current methods

A number of options have been considered in deciding how to bring monitor data to Mantid's live infrastructure. A key motivation in choosing a solution is that it should be introduced in a way that is transparent to existing users of the live data framework (and to their scripts). This rules out method 1 above, though it has anyhow been clear for some time that this is not a good way of working. 

Attempting to go with method 2 would present significant problems. The live listener interface (correctly) does not use workspace names at all, but rather passes back a single workspace pointer when the sole method for getting hold of the data - extractData() - is called. One possible way around this would be to pass back a WorkspaceGroup composed of two workspaces, one monitor data and the other scattering data. This idea presents a number of problems. If no changes were made to the live listener client (the LoadLiveData algorithm) then the group would propagate to the user level - meaning it would fail the test of being transparent; the user would have to handle or split the group whether they cared about monitors or not, and existing scripts would break. Handling the group somehow in the LoadLiveData algorithm would be very challenging to do robustly and elegantly. With no type information or even a workspace name to distinguish a monitor workspace, we would have to resort to looking through the detectors attached to each spectrum to try and identify the nature of the workspace. There could be a possibility of introducing a monitor workspace type, but I would argue that workspace groups have a role when there are homogenous collections of workspaces, but are really not amenable to handling heterogenous collections.

### Other rejected options

- A third option is to hold the monitor events as a sample log. This has the advantage of being transparent, and not having a large hidden memory cost (as most logs are not not combined when workspace chunks are added together). It would also be simple to implement. However, there are concerns around the performance of using the TimeSeriesProperty structure to store large data volumes; it wasn't designed with that in mind. There is also the issue of working with this monitor data: it would presumably have to be extracted into a workspace and associated with the correct Detector object despite the weak semantics (at best a text string) connecting the two.

- An event list hanging off of the monitor Detector object has been suggested. As this inverts our existing data-pixel connection, it suffers from dependency problems for which there is no immediately obvious straightforward solution.

Design
------

The high-level summary of the design is that we will hold the data for the monitors in their own workspace that is itself held by the 'main' workspace. Setters and getters will provided.

### In detail

- MatrixWorkspace gains an "m_monitorWorkspace" member. 
- It is of type MatrixWorkspace_sptr. (We could consider a specific MonitorWorkspace type but I don't think we need to, or that it would be helpful.)
- By default it would be an empty shared_ptr.
- Loading routines (including live listeners) can create a workspace containing spectra pertaining to monitors (and linked in the usual way to the detector objects within the instrument) and set it via a setMonitorWorkspace() method.
- It is possible to have either event or histogram monitor workspaces irrespective of the parent type. (This design would not allow a mixture of monitor types. An alternate design could have a collection of single-spectra monitor workspaces.)
- There is likely to be a getMonitorWorkspace() method as well. It will probably need to return a MatrixWorkspace_sptr (i.e. non-const).
- An ExtractMonitorWorkspace algorithm would pull out the monitor workspace, put it in the ADS with the "_monitor_" suffix (or a custom name if given) and set the internal monitor workspace pointer to null. This would be the normal way to access the workspace from Python. (Or should it leave it in the parent workspace as well???)
- Creating a workspace from its parent would not carry forward any monitor workspace. Thus running an algorithm on an input workspace holding an internal monitor workspace would lead to an output workspace that doesn't hold monitors, unless that algorithm modifies the workspace in place. This saves worrying about 
- The Plus algorithm is likely to be an exception to this rule - it should sum monitor workspaces as well (if they exist on both operands). This will aid live data processing when there is only post-processing.
- ConvertUnits could be another exception. Though saying so feels like the start of a slippery slope...

- I would not move existing monitor methodologies over to this automatically (e.g. LoadEventNexus/LoadNexusMonitors would still produce a separate ADS entry, though it could use the monitor workspace member internally as a first step).
- Over time this way of doing things could be extended, for example algorithms such as NormaliseToMonitor could be amended.




