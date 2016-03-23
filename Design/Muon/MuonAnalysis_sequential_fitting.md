### Meeting about sequential fitting in MuonAnalysis ###
#### 23/3/16 ####

Discussed mockups available at `Design/Mockups/muon/MuonAnalysis.bmpr` - the _Data Analysis_ tab.  
(The other tabs - mockups of new plotting functionality - were left for another time, as fitting is the priority).

This covers adding functionality for simultaneous fitting, which is Roadmap issue [#15518](https://github.com/mantidproject/mantid/issues/15518)

Comments from scientists:  

####1. Selection of what data to fit  
  (bottom right of the mockup)

  At the moment we have a _Data_ section in the fit property browser.  
  The _Workspaces_ line offers a dropdown of workspaces previously loaded into the interface.

  - Out of the two suggested dialogs they prefer the one on the right, with Runs, Groups, Periods groupboxes
  
  #####Runs#####
  - The Runs option would be better as a box to type a range into, like elsewhere   
  - Should *not* be restricted to runs that have been loaded into the interface - type any range, like for sequential fitting   
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
  - If there is only one period, hide (rather than grey out) the "Periods" group box to avoid presenting the user with irrelevant choices.

  #####Display#####
  - Rather than having a separate dialog, get rid of the "Data" section of the fit property browser and replace with this  
  (would need to have boxes for start/end times). Can select just one run for a single fit.
  - No need for a "simultaneous fit" option/checkbox - if user selects more than one run, it has to be a simultaneous fit
  - Show what's selected in _Workspaces_ line - or have *Workspaces, Groups, Periods* lines?
    - If this isn't a separate dialog, then not necessary to do this

####2. Parameters 

  James's suggestion is on the right of the mockup, above the data section. 
  
  It has an expand/collapse icon by each parameter. When collapsed, you can set this parameter to the same value for all data sets, but you can also expand to initialise to different values (e.g. phases). Collapsing again will list all values on one line. 

  - The option of expand/collapse parameters was agreed to be a good idea 
  - How would this work with fix/tie/constrain? These use the same expand/collapse icon.
  - Could have another column of checkboxes for "fix" - but still leaves problem for ties and constraints

####3. Sequential fits

  Not strictly related but another point raised:  
  At the moment you can:
  1. initialise parameters to the same values each time, or 
  2. use the previous fit's results. 
  
  It would be good to have a third option: initialise a parameter to a log value (e.g. field).  
  There should be some way to select which log value to use for a given parameter.  
  Also should be able to fix the parameter to the log value for each run.
  

