# Save BinMasks from Instrument View Proposal

## Issue

Users are able to interactively create and store detector masks via the *Instrument View* of Mantid. A recently added feature allows the user to interactively create and add bin masks to workspaces, but we are currently lacking an option (and format) to save these bin masks.

Saving the bin masks created in the Instrument View in order to apply them later on has been requested by several users of the SANS group.

## Current situation

We are able to store detector masks in the form of xml files. This works as follows:

1. Apply a mask to a specified detector region of a temporary workspace

    * This workspace is used for viewing.

2. Call [*ExtractMask*](http://docs.mantidproject.org/nightly/algorithms/ExtractMask-v1.html) on this temporary workspace
  
    * This creates a Mask Workspace which contains only 0 and 1
 
3. Call [*SaveMask*](http://docs.mantidproject.org/nightly/algorithms/SaveMask-v1.html) on the Mask workspace

    * This will write the mask workspace information into an xml file with a defined *detector-masking* format.
    
    
## Extension for Bin Masks

Bin masks are treated differently in Mantid. Workspaces are currently not aware that a bin mask has been applied to them. The region which is to be masked is merely reset to 0. The *Instrument View* stores the information in a collection of BinMask objects which contain information regarding the bin mask region and which detectors are affected.

### Option1: Use the BinMask collection we have in the *Instrument View* directly to persist the required information

The necessary bin information already exists in form of the aforementioned collection of BinMask objects. This information could be saved out directory via a "helper" class. The helper class could share its saving mechanism with the internal logic of *SaveMask*, ie we could refactor the xml-saving part of the algorithm such that it can be used for the algorithm itself and when saving from the instrument view.

Requires:

* Minor refactoring of the *SaveMask* algorithm

Pro:

* should be fairly simple to achieve
* no impact on current workspace structure

Con:

* situation-specific solution
* difference between the way we treat detector masks and bin masks (this is already the case though)


### Option2: Create equivalent workflow for bin masks as exists for detector masks

The way detector masks are handled (at least for persisting to a file in the *Instrument View*) could be mimicked for bin masks. This means the algorithm and workspace infrastructure would be extended to be able to have bin mask information attached to a workspace and handle it accordingly in certain algorithms.

Requires:

* Mechanism for workspace to store bin mask information
* *ExtractBinMask* algorithm
* *SaveBinMask* algorithm

Pro:

* Is consistent with the workflow of detector masks (at least for saving in the *Instrument View*)

Con:

* Need to extend workspaces (memory overhead?)
* would have two ways of dealing with bin masks, the old set-to-zero way and the new additinal bin-mask-information way
* more time required to implement



In both cases we would also have to modify [*MaskBins*](http://docs.mantidproject.org/nightly/algorithms/MaskBins-v1.html) in order for it to accept and comprehend the new xml format for masked bins.

