A new way of handling monitor data
==================================

Motivation
----------

The background to this document is that a requirement exists that monitor data be available in Mantid's live data toolset. In particular, the [SNS live listener](https://github.com/mantidproject/mantid/blob/master/Code/Mantid/Framework/LiveData/src/SNSLiveEventDataListener.cpp) needs to be able to pass back the full event-based monitor data since there are certain analyses and tools that require this information.

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

There are two main guiding principles behind this design (in addition to it solving the main problem at hand of getting monitors into the live data workflow): (1) it will not break any existing user scripts/workflows, and (2) it is open for extension at a later stage, if so desired.

### In detail

- MatrixWorkspace gains an "m_monitorWorkspace" member. 
- It is of type MatrixWorkspace_sptr. (We could consider a specific MonitorWorkspace type but I don't think we need to, or that it would be helpful.)
- By default it would be an empty shared_ptr.
- Loading routines (including live listeners) can create a workspace containing spectra pertaining to monitors (and linked in the usual way to the detector objects within the instrument) and set it via a setMonitorWorkspace() method.
- It is possible to have either event or histogram monitor workspaces irrespective of the parent type. (This design would not allow a mixture of monitor types. An alternate design could have a collection of single-spectra monitor workspaces.)
- There is likely to be a getMonitorWorkspace() method as well. It will probably need to return a MatrixWorkspace_sptr (i.e. non-const).
- An ExtractMonitorWorkspace algorithm would pull out the monitor workspace, put it in the ADS with a provided name and set the internal monitor workspace pointer to null. This would be the normal way to access the workspace.
- Creating a workspace from its parent (via the WorkspaceFactory) would not carry forward any monitor workspace. Thus running an algorithm on an input workspace holding an internal monitor workspace would lead to an output workspace that doesn't hold monitors, unless that algorithm modifies the workspace in place. Such in-place modification of the holding workspace would not modify the monitor workspace.
- Algorithms should not act on an internal monitor workspace. If a user wants to interact with this workspace they should extract it and act upon it 'manually'. There is a good case for monitor-specific algorithms such as NormaliseToMonitor to look for the internal monitor workspace, but this will not be done at this stage.
- Certain loaders (in particular LoadEventNexus) will be modified to hold the monitor workspace in the internal pointer *in addition* to adding a separate ADS entry as at present. 

Feedback
--------

The feedback below relates to the design as it was described at [this point] (https://github.com/mantidproject/documents/blob/6ead06a9c7f467158da7af1b00a8de3e87b2d340/Design/MonitorsInLiveData.md).

### From Nick
- I'm concerned that a move away from having monitors available as _monitors would adversely affect many users scripts.  I accept that ExtractMonitorWorkspace would ameliorate this down to a single line change needed, but it would still need script changes.  See below for a suggestion.
- I'm not happy about the special rules around which algorithm affects monitor workspaces and which doesn't.  It's confusing.
- A suggested middle ground:
  - Have them monitor workspace link within a workspace as you suggested, together with the methods to access it.
  - Store both the normal workspace AND any attached monitor workspace in the ADS using the _monitors convention when the parent is stored.  This way it is backwardly compatible with the way things are currently done, but you still have unstored workspaces able to keep links to it's monitors.
  - Have the owning workspace subscribe to updates from the ADS so it can react to deletion and updates of the monitor workspace (e.g. someone rebins the montior workspace leading to a change in memory location, or the user intentionally deletes the monitor workspace as it is large and not needed anymore).
  - You could even consider enhancing the GetMonitorWorkspace Methods to search the ADS for a xxx_monitors workspace if the shared pointer is empty (assuming the current ws is stord in the ADS as xxx).
- I think this approach maintains the current way of working with "seperated" monitor workspaces, while giving the flexibility you ned with live data for a workspace to own and maintain the lifetime of it's monitors.

### From Andrei
Nice solution. I just have a small suggestion. Don't allow any algorithm to modify the monitor workspace, not even Plus. If one needs to add monitors, it should be done explicitly:

    w=w1+w2
    w.monitorWorkspace=w1.monitorWorkspace+w2.monitorWorkspace

Otherwise we'll have some algorithms that are aware of the monitors, others that are not, which will lead to confusions. For example, should multiplying with a single valued workspace act on the monitor as well? What if the workspace that I am multiplying with is a regular matrix workspace? How about Rebin? Or Plus on some processed workspaces?

### Response from Russell
Andrei – I think you are right. The idea to have it in Plus was as a convenience for its use with live data. It can just be handled inside LoadLiveData instead. You’re suggested python syntax looks nice, but I’d have to check whether that will work with the way the LHS functions to work out a name (subsequent note: no it won't).

Nick – The “no breaking impact on existing users” clause applies beyond just live data, even though I didn’t explicitly say that. I’d no intention of taking away the “_monitors” workspace where it’s currently put in the ADS (see second to last bullet). The idea is that this solution is amenable to extension in the future if desired. I’m not too keen on doing things that reinforce the existing ADS-based way as I don’t think that’s a great way of doing things (doesn’t work well for child algorithms, for example).
