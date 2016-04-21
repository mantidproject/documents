### Meeting about sequential fitting in MuonAnalysis ###
#### 23/3/16 ####

Discussed mockups available at `Design/Mockups/muon/MuonAnalysis.bmpr` - the _Data Analysis_ tab.  
(The other tabs - mockups of new plotting functionality - were left for another time, as fitting is the priority).

This covers adding functionality for simultaneous fitting, which is Roadmap issue [#15518](https://github.com/mantidproject/mantid/issues/15518)

Comments from scientists:  

####1. Selection of what data to fit  

  Conclusion of this section so far:  
![mockup](https://cloud.githubusercontent.com/assets/15363125/14645508/d6ba7586-064d-11e6-8b4f-91e89f2573f3.PNG)

  At the moment we have a _Data_ section in the fit property browser.  
  The _Workspaces_ line offers a dropdown of workspaces previously loaded into the interface.

  - Out of the two suggested dialogs they prefer the one on the right, with Runs, Groups, Periods groupboxes
  
  #####Runs#####
  - The Runs option would be better as a box to type a range into, like elsewhere   
  - Should *not* be restricted to runs that have been loaded into the interface - type any range, like for sequential fitting  
    - This conflicts with syntax for *co-added* runs on home tab. Added radio buttons to solve this.
  - If several runs selected, would fit the same groups/periods for all
  - If one run selected, can fit several groups/periods for that single run   
    - Can then set up a sequential fit across runs for this (sequential fit not possible if several runs selected in browser)   
  
  #####Groups#####
  - Groups displayed as checkboxes to choose from are those for the first run.  
  - Restrict so that the first run is the one loaded through the interface (i.e. groups are those from the _Grouping Options_ tab).   
  - If the user selects other runs that have different groupings then that's their own fault, don't try to catch this.     
  - Start off with all the groups ticked by default
  
  #####Periods#####
  - Keep the "combination" periods option, should be like it is on the _Home_ tab   
  - If there is only one period, hide the "Periods" group box to avoid presenting the user with irrelevant choices. Scientists would prefer to hide it rather than grey it out.

  #####Display#####
  - Rather than having a separate dialog, get rid of the "Data" section of the fit property browser and replace with this  
  (would need to have boxes for start/end times). Can select just one run for a single fit.
  - No need for a "simultaneous fit" option/checkbox - if user selects more than one run, it has to be a simultaneous fit
  - Show what's selected in _Workspaces_ line - or have *Workspaces, Groups, Periods* lines?
    - If this isn't a separate dialog, then not necessary to do this

####2. Parameters 

  The intention at present is to reuse the components from the existing MultiDatasetFitting interface, as far as possible.
  This could certainly be done with the fit function / parameters section.
  This is in MantidWidgets and already supports initialising parameters to different values for each dataset (e.g. phases), which is something that was agreed to be a good idea in the meeting.
  If you click in the "Value" column for a non-global parameter, there is a button that opens a dialog as below.
  This enables setting/fixing different initial values for each dataset.
  
  ![image](https://cloud.githubusercontent.com/assets/15363125/14713128/c716ea48-07d7-11e6-86ae-7c83eefbc3f6.PNG)

####3. Sequential fits

  Not strictly related but another point raised:  
  At the moment you can:
  1. initialise parameters to the same values each time, or 
  2. use the previous fit's results. 
  
It would be good to have a third option: initialise a parameter to a log value (e.g. field).  
There should be some way to select which log value to use for a given parameter.  
Also should be able to fix the parameter to the log value for each run.
  
There are three possible ways to do this:  
1. Right-click and "set from log" as in James's suggestion below  
2. Something similar to the "intelligent fitting" that is done with *IkedaCarpenterPV* on GEM - for specific instruments, certain parameters are initialised from a log  
3. Doing something with the fit string itself  

James's comments:
> It would also be convenient to have that option when manually stepping through runs and fitting them one by one. In that case   loading a run would reinitialise the value, though it could be possible to edit it before doing the fit. Also in Simultaneous fits across a sequence of runs, we might want to initialise a (non-global) parameter to a log value per run, and not have to type all the numbers in manually.

> Given this is set on a per-parameter basis, it would be logical to add another option “Set from Log” to the main fit dialog, in the pop up menu along with “Fix”, “Constraint” and “Tie” for a fit parameter. Either use this in combination with “Fix”, or have two variants “Fix to log” and “Initialise from log”.

> You’d select from log values available in the currently loaded or first run in the sequence and it’s the user’s fault if a later run doesn’t have that log value any more.

> We may need either (a) the option to enter a formula to calculate the fit parameter from the log value instead of a direct copy, or (b) variants on functions such as “ExpDecayOsc” which take a field parameter rather than a frequency.


