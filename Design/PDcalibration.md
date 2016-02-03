Motivation
==========

There are a few reasons why this is being done:

1. NOMAD data does not align/focus well enough using a simple
   `DIFC`/`offset` paradigm.

1. Current calibration happens "from scratch" using the instrument
   geometry as a starting point. This means that every calibration is
   (essentially) a global search.

1. Calibration requires a "long soak" type measurement where all of
   the pixels have enough statistics for either peak fitting or
   cross-correlation. This requires a fair amount of beamtime for
   things that could be handled with a smaller (multiplicative)
   correction.

Requirements
============

1. Two user facing algorithms for calibrating the instrument.

   * Algorithm that performs a pixel-by-pixel calibration by using a
     "many peaks" approach. GetDetOffsetsMultiPeaks
     ([docs](http://docs.mantidproject.org/v3.5.1/algorithms/GetDetOffsetsMultiPeaks-v1.html)
     and
     [github](https://github.com/mantidproject/mantid/blob/v3.5.1/Code/Mantid/Framework/Algorithms/src/GetDetOffsetsMultiPeaks.cpp))
     is the closest thing we have at the moment.

   * Algorithm that performs bank-by-bank calibration to generate a
     multiplicative factor for each summed
     spectra. [EnggCalibrate](https://github.com/mantidproject/mantid/blob/v3.5.1/Code/Mantid/Framework/PythonInterface/plugins/algorithms/EnggCalibrate.py)
     is representative of this approach.

1. The code should work on any instrument that wants to calibrate
   using powder diffraction data. The instrument component hierarchy
   should be abstracted away as should the calibration sample.

1. The pixel-by-pixel option should produce `DIFC` for each
   pixel. Optionally (default is "on") it should allow for `DIFC`,
   `TZERO`, and `DIFA` with a preference for turning off extra terms
   if the reduced chi-squared warrants.

1. The resulting calibration should be usable in tools to update the
   `IDF`. [AlignComponents](https://github.com/mantidproject/mantid/compare/master...rosswhitfield:AlignComponent)
   is an example of what would be needed.

Design
======
