Minutes of the ILL SANS demo
============================

Points raised:
--------------

- Check with Franck C. if NeXus files have been changed or will be changed in next cycle. Make sure that all the metadata is written and is consistent.

    There will be a new version of nexus which is consistent accross the 3 SANS instruments. It is not yet in production, the SCI is working to deploy it. Once we have first test files, we will adapt the mantid loaders as per necessary.

- The issues with the instrument view: 

    - Easy method to mask lines? 
    
    No easy method to mask lines at the moment. Lines are just thinner rectangles. Consider possibility of line/tube masking.

    - Possibility to undo or remove a mask.
    
    Masks can not be easily undone after they are applied. Consider having an undo button to revert the last mask. 
    
    - Wavelength slider does not make sense for a monochromatic measurement
    
    Agreed. It should not be shown for monochromatic.
    
    - Freeze the view to XY projection; 3D view is useless.
    
    Agreed. 
    
    - Check that when the autoscaling option is selected, the image updates accordingly whenever a bad region is masked.
    
    This is actually done (will double check though), just we were looking into water data, which is flat inside across one panel, so change of autoscaling after masking was not noticed.

    - Check problem appearing when a pixel is selected in the pick option (very slow response).
    
    Identified, will be fixed. It was trying to show all the instrument parameters in the info block, which it should not.

- Should the script contain explicitly all the possible options for each algorithm (even when the default values are used)?

    No point in putting in the default options. The defaults can be checked from the documentation.

- Apart from standard log/lin plots, have options for Kratky plots, q^2*I(q) vs q, etc.

    This can be implemented rather quickly. Tools to make common plots are implemented for example for TOF spectroscopy users.

General Concerns
----------------

- **I(Q) of isotropic is only a small part of what is expected from SANS reduction software.**

  Need to discuss resourcing and priorities. First milestone was to target replacing LAMP. Replacing GRASP functionality will require more effort. While it should offer some fitting possibilities during data reduction, mantid is not supposed to serve as an analysis software.

- **Speed: On a personal laptop it took 5s for a sample of 5 summed numors (D33) to reduce and convert to I(Q). 2s is spent on loading the 5 numors.**

  All the corrections and transformations are implemented with multi-threaded C++, python layer is only the workflow logic.
  Note that since the code is parallelized, running on a 16 core machine which we provide in the instrument cabins should be a lot faster than on a 4 core personal laptop (scaling almost linearly).
  Which means the full reduction (loading, corrections and I(Q)) will take less than 1s per numor on the instrument machine.
  If mili-second performance is required, this might imply a change of technology and architecture (HPC, GPU, MPI), which is not in the current scope of Mantid.
  Event mode will not help since the produced data is much more. Will explore possibilities of speed up through compression modes of nexus files. Will profile the reduction and identify potentially slower parts of the reductions, but this will bring max 10-20% speed up.

- **GUI: can not use/test without a GUI**

  Prototype spreadsheet like GUI to be given priority to facilitate the adoption.
  
Actions
-------

Short term
==========

- Pick up one complete recent proposal per instrument (for the moment monochromatic isotropic), write the reduction script, make sure the results are consistent with LAMP/GRASP.

Mid term
========

- Put together a prototype spreadsheet GUI (similar to the ISIS SANS) to facilitate the pick up of Mantid.

Long term
=========

- Non-isotropic SANS with graphical functionality of GRASP (selecting sectors etc.)
- Parametrized reductions (i.e. the depth axis), rocking curves etc.

