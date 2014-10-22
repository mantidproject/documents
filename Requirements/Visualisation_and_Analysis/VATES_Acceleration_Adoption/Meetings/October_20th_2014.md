Agenda
======

To discuss the findings from instrument scientist led testing of the exiting tools.

Missing Features
================
Creating MD Workspaces
----------------------
* Examples of how to create MDWorkspaces in script. Different usage examples.
* Inelastic diffraction groups have a strong preference for scripting.
* SC elastic diffraction request for a way of performing creating MD workspaces in a 'point and click' (GUI) style.
* Speed of creation/merge.
* Symmetrisation

Alignment tools
---------
* Alignment tools for the inelastic experiments.

Peaks Workspaces
-----------------
* Need to better support multiple UB matrixes.
* Need a way to tag a peak with a UB identifier.
* Better peak edititing features. Addition, subtraction. 
* All tools that work on PeaksWorkspaces should be synched.
* Need to support different conventions, currently only inelastic convention ki-kf.
* PeaksWorkspaces should 'remember' MDWorkspaces. Possibly two way interaction.

Slice Viewer
------------
* Need to apply viewing matrix and B matrix calculations to display non-orthogonal reciprocal lattice vectors.
* Peaks Viewer mode needs edit mode.
    - Add peak.
    - Delete peak.
    - Resize integration region.
* PeaksViewer needs a way to represent peak integration regions better, non-spherical (arbitrary shapes).
* Modifications to Peaks list need to be immediately reflected in the Peaks Viewer.
* Needs to work in step size mode and bin number mode.
* Buttons need to be combined where possible and better defined.
* More options for exporting data. 

VSI (VATES Simple Interface)
-------------------------------------
* Needs better default view (colour map, box splitting)
* Initial plot should be relevant
* Annotations need to be better. 
* Needs auto-rebin feature like SliceViewer
* Needs zoom to detail feature.
* VSI needs ability to plot when data is reduced from dimensionality 4 -> 3 -> 2 -> 1.
* View needs to be rearraged to increase space given to main display (reduce sidebar, top bar)

Simulation and Fitting
----------------------
This has been agreed to be outside the scope of what we are currently working on, but will be the focue of the next development effort after this project has finished.

Actions
=======
* Scientists to create gather examples and documentation to be shared. Example documentation should specifically highlight where things are not being displayed properly that should be displayed properly. Nick, Owen and Pete are to organise distributing these amongst the wider team.
* Requirements need to be prioritised. Nick to generate some form of ranking for these.
* Helen to continue to drive the validation work against Horace.
* Russell and Martyn to pass to Doug the current simulation work and example scripts.
* Owen to pass to Doug the existing Horace-Mantid syntax design.
* Russell and Pascal to act as points of contact for alignment.

