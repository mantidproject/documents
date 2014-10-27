Agenda
======

To propritise the requirements discussed in the previous meeting, using the output of the survey and further discussion.

Prioritised Requirements
------------------------
With items at the top being more important
Creating MD Workspaces
----------------------
1. Correct event normalisation across multiple files
1. Horace style syntax for extracting cuts etc
1. Inelastic diffraction groups have a strong preference for scripting for creating MD workdpaces.
1. Speed of creation/merge.
1. Harmonised plotting syntax for all plots
1. Good usage examples of how to create MDWorkspaces in script. Both diffraction and Inelastic.
1. Validation of cuts / plots from large SQW datasets
1. Improve the MD syntax for defining non-orthogonal axes
1. Speed of loading saved MD files
1. Alignment tools for the inelastic experiments.
1. Symmetrisation
1. SC elastic diffraction request for a way of performing creating MD workspaces in a 'point and click' (GUI) style.

Peaks Workspaces (Yet to be prioritised)
-----------------
1. Need to better support multiple UB matrixes.
1. Need a way to tag a peak with a UB identifier.
1. Better peak edititing features. Addition, subtraction. 
1. All tools that work on PeaksWorkspaces should be synched.
1. Need to support different conventions, currently only inelastic convention ki-kf.
1. PeaksWorkspaces should 'remember' MDWorkspaces. Possibly two way interaction.

Slice Viewer
------------
1. Need to apply viewing matrix and B matrix calculations to display non-orthogonal reciprocal lattice vectors.
1. Needs to work in step size mode and bin number mode.
1. More options for exporting data. 
1. Slice viewer UI and button improvements
1. Modifications to Peaks list need to be immediately reflected in the Peaks & slice Viewer.
1. Peaks Viewer mode needs edit mode.
    - Add peak.
    - Delete peak.
    - Resize integration region.
1. PeaksViewer needs a way to represent peak integration regions better, non-spherical (arbitrary shapes).
1. Link peaks lists to workspaces better (& link in plots)

VSI (VATES Simple Interface)
-------------------------------------
1. Allow slice axes to be fixed to Q, or crstal axes if required 
1. Needs better default view (colour map, box splitting)
1. Initial plot should be relevant
1. Axes and plot annotations improvements
1. Update view in response to peak list (& possibly workspace) changes 
1. VSI needs ability to plot when data is reduced from dimensionality 4 -> 3 -> 2 -> 1.
1. Needs auto-rebin feature like SliceViewer
1. Edit peak lists (add, remove, Resize integration region)
1. Needs zoom to detail feature.
1. View needs to be rearraged to increase space given to main display (reduce sidebar, top bar)

Others (not prioritised yet)
-------
1. Develop training meterials for inelsatic and SX diffraction
1. Peak integration areas viewable from the instrument view (detector area and tof once you click on a pixel). 
1. Planning tools. A good start, which would not take long to implement, would be to be able to create an empty peaksworkspace, attach a lattice to it and generatepeaks on an empty instrument (so q range are known) or a masked one (eg with a pressure cell or magnet obstructing the view). - New
1. Easy accessible masking options for peaks, areas, volumes, which are connected or not, and masks that can be displayed in the various viewers and saved and reused - New  - Question would these be defined in detector or Q space?


Actions
=======
1. Scientists to craise any further requirements or changes in priorities at the next meeting.
1. Development team to discuss and provide estimates
