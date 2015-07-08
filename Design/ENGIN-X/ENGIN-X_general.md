
Introduction
============

This is a convenient compilation of miscellaneous information required
to understand how support for ENGIN-X is being added in Mantid. The
objective of this document is to keep track of all the relevant
components being put in place to support ENGIN-X data analysis,
including data and file formats, third party software, etc.. It should
be useful as a reminder and reference resource for those working on
ENGIN-X support in Mantid, as well as new developers.

This document is in a very early stage of writing. Eventually it
should be replaced by the documentation of a yet to be added ENGIN-X
workflow algorithm, the ENGIN-X GUI, and other documents.

Processing steps
================

Pre-processing steps:

* Focusing. Calibrate Full.

* Calibrate

* Intensity calibration

* Masking

Analysis steps (2 types of analysis in principle):

* Whole pattern fitting

* Single peak fitting

ENGIN-X specific algorithms in Mantid:
======================================

The following algorithms were initially defined for EnginX:

* EnginXCalibrate
* EnginXCalibrateFull
* EnginXFitPeaks
* EnginXFocus

which have been renamed to:

* EnggCalibrate
* EnggCalibrateFull
* EnggFitPeaks
* EnggFocus

Other relevant Mantid algorithms:
=================================

Besides the EnginX algorithms currently included in Mantid
(EnggCalibrate, EnggCalibrateFull, EnggFitPeaks, EnggFocus),
there are other algorithms 

The exact way in which they could be used, extended or modified for
ENGIN-X is still to be clarified. These include:

* LoadGSASInstrumentFile, which could well be used to load GSAS .par
  files?

* LoadCalFile, SaveCalFile and other \*CalFile\* algorithms use a
  certain "calibration file" format which is described as "Ariel
  detector file" (for info on Ariel see
  http://www.isis.stfc.ac.uk/instruments/osiris/data-analysis/ariel-manual9033.pdf). This
  format does not seem to be equivalent enough to what ENGIN-X
  scientists need.

Datasets
========

These data files can be used for testing purposes and are being used
by scientists as of this writing:

* The current (long run) Ceria (CeO2) data is run number 193749 (from
  cycle_12_4). This is used for CalibrateFull as it contains enough
  data for every individual detector.

* A recent Ceria file that is used for calibration (not CalibrateFull
  is in run 241391 (from cycle_15_1).

* Vanadium (V-Nb) data is in run 236516 (from cycle_14_3).

GUI
===

Under the GUI subdirectory there is information specific to the
ENGIN-X GUI, including the (Balsamiq) mock-ups for the tabs being
developed as of this writing.

Third party software
====================

* GSAS, software for crystallographic studies:
  https://subversion.xor.aps.anl.gov/trac/pyGSAS

* OpenGenie, currently used by ENGIN-X scientists and users.

Data formats
============

* .par

* .his

* calibration files
