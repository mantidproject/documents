No engineering diffraction people were present
ORNL is not doing imaging in mantid
ISIS moved their imaging out of mantid

Powder diffraction/PDF
----------------------
ILL is using D2B for tradional powder diffraction (with calibration) and writing to FullProf
ILL doesn't have PDF cabilities yet
ISIS diffraction is mostly small issues
- any shape absorption, can read in the mesh, but haven't tried to use the result
- would like to try first on PEARL
- powder is using absorption corrections for simple shapes when then see issues in the data
ISIS pdf liquids is not currently using mantid
ISIS engeneering just needs a gui worked out
POLARIS is having some issues comparing to GURUN - they may be using `ConvertUnits` rather than `AlignDetectors`
 
Single crystal diffraction
--------------------------
Single crystal extension path length added to Jana output format
ISIS would like to start testing incomensurate and modulated structures
ISIS complex shape absorption again
ORNL would like interactive interface for finding peaks in modulated structures
ORNL is asking for visualizing 3D volumes of reciprocal space with
- responsive interaction
- feedback on what the user is looking at
- ideally in the workbench
SXD doesn't use mantid
HRPD is using "old" mantid
Need structures for handing multiple UB matrices for twinned crystals - not easy - maybe done by creating a copy of the data and determining which peaks are found by the two UB

Engineering
-----------
ISIS Bragg edges

VSI/Paraview
------------
Neither ISIS nor ORNL use VSI - would like to know when/if it gets moved into VSI
The default view after having added data does not give the user a good idea where the data is
The responsiveness is bad - giving less data to the tool may be a better solution

Generic/Question
----------------
How is workbench
- looks ready for powder
- want a library of ways to do plots
- would like setting for plotting lines or points by default
What do you like about workbench
- sorting of plots
- maybe a single plot window with a list of all the plots to look at that is selectable
Missing/obstacles from workbench
- advanced plots are needed for powders
- definitely need the slice viewer
- custom interfaces
Random notes
- something in mantid that warns if too much memory is being used, maybe attached to algorithm cancellation
- all ISIS powder diffraction users are using mantid
- all SNS instruments, WAND, POWDER is ready but beam went down before acceptance testing
- adding workflow diagrams to workflow algorithms would be useful
- determining workflow for how a workspace was generated would be useful as well
- user documentation would benefit from assumption/applicability section
