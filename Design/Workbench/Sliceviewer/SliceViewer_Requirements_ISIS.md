## Mantid 4 - Sliceviewer Rewrite

### Requirements from ISIS

At the January developer meeting in 2017 we agreed the approach to migrate both the spectrum viewer and sliceviewer into Mantid 4 
would be to rewrite and merge both of these two tools together.  As the majority of this work is planned to be based at ORNL, this document 
has been written to capture the aspects of sliceviewer that are currently in active use, and need to be included for the plans for the new 
combined tool.

In addition following a meeting amoungst the instrument scientsts at ISIS we identified an additional use case for allowing slices along an elipse that would make this tool very useful for the SANS community.

### Usage of the existing interface of Sliceviewer at ISIS

We used a google form as a questionaire during a meeting as a way to capture which aspects were in use by the various interested techniques at ISIS.

#### Responses

The results of the questionaire are linked [here](https://docs.google.com/forms/d/1l4CLQXWHC03E2hKzADrRf96ZiTGCqfz0AW9VIB6ImsE/edit#responses).  
The questionaire is owned by the Mantidproject google account.

I've also included an [excel file of the responses]("ISIS Usage of Sliceviewer.xlsx")  formatted to make it easier to read.

#### Summary

A simple summary of the reponses is that pretty much all of the aspects of the current sliceviewer, lineviewer and peaksviewer are actively used by one technique or another.
Pascal and single crystal diffraction at ISIS are the most frequent users and use the widest range of functionality by far.  
Pascal expressed his concern at the rewrite of the tool that he relies on, and considers it essential to the single crystal work at ISIS.   
Most of the other groups aither used sliceviewer less frequently or in the case of SANS would dearly love to use sliceviewer if the new slice types they need could be included.

The only aspects that could be considered less essential (but still nice to have) were:

1. The ability to temporarily hide and return a peak list from the view, Assuming that you can still add and remove peaks lists.
1. The manual selection of different normalisation methods, but this is assuming that we can always automatically select the correct normalisation method.


### New slicing options

The SANS group would love to be able to perform slices of two new forms
1. a ring of an elipse, with control of the depth of the ring
1. a full elipse (this could be through of as a special case of the above)
1. Sectors of both of the above

![New slicing options](NewSlices.png)

The results of this slicing would be a plot of intesity, against the angle from the centre of the elipse. 
We already have a siliar algoithm [RingProfile](http://docs.mantidproject.org/nightly/algorithms/RingProfile-v1.html), 
but that only supports rings as opposed to elipses at present, and cuttenrly calcuates the answer for the full ring 
rather then sectors of it.
