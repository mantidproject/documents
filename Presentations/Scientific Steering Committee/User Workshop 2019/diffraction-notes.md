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

Engineering
-----------
ISIS Bragg edges

VSI/Paraview
------------
Neither ISIS nor ORNL use VSI - would like to know when/if it gets moved into VSI
The default view after having added data does not give the user a good idea where the data is
The responsiveness is bad - giving less data to the tool may be a better solution
