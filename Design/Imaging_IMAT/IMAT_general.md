
Introduction
============

This document describes all the components required for processing
image data from IMAT, including pre-/post-processing, tomographic
reconstruction, visualization and related functionality.

This document is in an extremely early stage of development. More
detailed documents will be possibly added about topics such as the
FITS format being defined for IMAT, the different data replicas (ISIS
archive, SCARF), etc.

Objectives
==========

The new IMAT instrument (ISIS facility) will start its scientific
commissioning in September 2015. The objective of this document is to
keep track of all the relevant components being put in place to
support data analysis and visualization. It should also help to keep
the overall system as consistent as possible as we move into the
testing and operation phases and requirements evolve.

Functionality provided
======================

* Reconstruction via third party tools on remote compute resources
  (compute clusters, etc.).

* Visualization, very simple at this point. Also possible with third
  party tools.

Remote compute resource used at ISIS: SCARF
===========================================

General information on the SCARF cluster, which uses the Platform LSF
scheduler, can be found at http://www.scarf.rl.ac.uk. It can be used
via:

* remote login
* a web portal: https://portal.scarf.rl.ac.uk
* a web service

The IMAT GUI utilizes a RESTFul web service provided by Platforms
LSF's Platform Application Center, as described here:
https://github.com/mantidproject/documents/tree/master/Design/Imaging_IMAT/SCARF_Platform_LSF/
(with Python client scripts).

Data locations and copying
==========================

As data is produced by IMAT and it becomes available at the IMAT
control machine, it will be copied to several locations: IMAT data
analysis machine, ISIS archive, and SCARF disk space for the imat
project. In principle all these locations will be identical replicas,
although there are plans to store a subset of the reconstructions
generated in the archive.

* Archive. TODO: structure to be defined.

* IMAT data analysis machine (NDAIMAT) which is NDW1520 at the moment.

* Replica on SCARF. TODO: all the details, storage levels, capacity,
times.

TODO. Practicalities. Data volumes. Bandwidth requirements, etc.

Data formats
============

Relevant data formats are described for example in the Tomographic
Reconstruction custom interface of Mantid.

TODO: include here details not relevant to users, such as
specificities of the IMAT FITS format, versioning information, etc.

* FITS format for IMAT: currently being defined by IMAT scientists and
  also in consultation with other groups. Mantid algorithm LoadFITS:
  http://docs.mantidproject.org/nightly/algorithms/LoadFITS-v1.html.

* DLS NXTomo: currently supported in several algorithms included in
  Mantid. Example mantid algorithms:
  http://docs.mantidproject.org/nightly/algorithms/LoadSavuTomoConfig-v1.html,
  http://docs.mantidproject.org/nightly/algorithms/SaveSavuTomoConfig-v1.html,
  http://docs.mantidproject.org/nightly/algorithms/SaveNXTomo-v1.html.

Reconstruction and imaging tools
================================

Tools being used and/or considered include:

* [Octopus](http://octopusimaging.eu) which includes reconstruction
  and visualization tools. Closed source. IMAT scientists have
  licence(s). The visualization tool (Octopus visualization) can be
  downloaded for free.

* [TomoPy](https://www1.aps.anl.gov/Science/Scientific-Software/TomoPy).
  Open source, installed on SCARF.

* [Astra Toolbox](http://sourceforge.net/p/astra-toolbox/wiki/Home/),
  open source, Python and matlab interfaces to C++ code (with CUDA
  acceleration), installed on SCARF.

* [Savu](https://github.com/DiamondLightSource/Savu), open source,
  being developed at the Diamond Light Source.

* [MuhRec](https://www.psi.ch/niag/muhrec): developed at PSI. See also
  [ImagingScience.ch](http://imagingscience.ch/muhrechome/index.html)
  for downloads, further information and additional complementary
  tools.

Image processing
----------------

In addition to reconstruction tools, another tools will be used by
scientists to process images and/or stacks of images. It may be
required to integrate data formats, and packages, or to provide
similar and/or complementary functionality to process stacks of
images. These third party tools include:

* [imagej](http://imagej.nih.gov/ij/), open source, very widespread and
  included in Linux distributions.


Practical issues
----------------

At first, both TomoPy and AstraToolbox are not necessarily easy to
use, or easy to use to their full potential. Using them from Mantid
requires some practical knowledge of these tools and the methods that
they implement.

TODO: how to run them, steps needed, all-important
pre-/post-processing steps.
