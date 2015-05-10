# Time Slicing of Added Event Data in SANS #

### Context ###

Up until April 2015, the SANS interface allowed only to add data set as added histograms.
We added the option to add event data and save this as added event data.
This works fine until time slicing of the added event data is performed, 
as the logs of the event data seem to get concatenated.

### Current workflow of adding the event data ###
For adding the event data, we apply the Plus algorithm on both the event data and the monitor data.
Once all runs are added, we group the added event data and the added monitor data.
This group workspace is then stored in a file. This file can then be loaded from the "Run Numbers" tab. 
