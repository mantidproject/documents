### Meeting about sequential fitting in MuonAnalysis ###
#### 23/3/16 ####

Discussed mockups available at `Design/Mockups/muon/MuonAnalysis.bmpr` - the _Data Analysis_ tab

This covers adding functionality for simultaneous fitting, which is Roadmap issue [#15518](https://github.com/mantidproject/mantid/issues/15518)

Comments from scientists:

1. **Selection of what data to fit**  
  (bottom right of the mockup)

  At the moment we have a _Data_ section in the fit property browser.  
  The _Workspaces_ line offers a dropdown of workspaces previously loaded into the interface.

  - Out of the two suggested dialogs they prefer the one on the right, with Runs, Groups, Periods groupboxes
  - The Runs option would be better as a box to type a range into, like elsewhere
  - Should *not* be restricted to runs that have been loaded into the interface - type any range, like for sequential fitting
  - If several runs selected, would fit the same groups/periods for all
  - Also might want to fit several groups/periods for a single run
  - Show what's selected in _Workspaces_ line - or have *Workspaces, Groups, Periods* lines?
  - Rather than having a separate dialog, get rid of the "Data" section of the fit property browser and replace with this  
  (would need to have boxes for start/end times). Can select just one run for a single fit.
  - No need for a "sequential fit" option/checkbox - if user selects more than one run, it has to be a simultaneous fit
  - (N.B. with previous points, must be able to set up a simultaneous fit across groups (for one run) in the fit property browser and then run this as a sequential fit across runs).
  - Groups displayed are those for the first run. Restrict so that the first run is the one loaded through the interface (i.e. groups are those from the _Grouping Options_ tab). If the user selects other runs that have different groupings then that's their own fault, don't try to catch this. 
  - Start off with all the groups ticked by default
  - Keep the "combination" periods option
  - If there is only one period, hide (rather than grey out) the "Periods" group box
  
2. **Parameters**  

  James's suggestion is on the right of the mockup, above the data section.

  - Like the option of expand/collapse parameters. 
  - How would this work with fix/tie/constrain? These use the same expand/collapse icon.
  - Could have another column of checkboxes for "fix" - but still leaves problem for ties and constraints

3. **Sequential fits**

  Not related but another point raised:  
  At the moment you can initialise parameters to the same values each time, or use the previous fit's results.  
  It would be good to have a third option: initialise a parameter to a log value (e.g. field).  
  Some way to select which log value to use for a given parameter.  
  Also should be able to fix the parameter to this value (but a different value for each run).
  

