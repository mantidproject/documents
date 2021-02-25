Motivation
==========

Overall the calibration is being used to calculate the time-of-flight
to d-spacing conversion factors. Using "GSAS" style parameters this is
```
TOF = (DIFC * d) + (DIFA * d * d) + TZERO
```
The preference is to use `DIFC`, then add `TZERO` and `DIFA` (in
order) if necessary.

Algorithms like
[GetDetectorOffsets](https://github.com/mantidproject/mantid/blob/v3.5.1/Code/Mantid/Framework/Algorithms/src/GetDetectorOffsets.cpp)
and
[GetDetOffsetsMultiPeaks](https://github.com/mantidproject/mantid/blob/v3.5.1/Code/Mantid/Framework/Algorithms/src/GetDetOffsetsMultiPeaks.cpp)
use the instrument geometry to convert the calibration data from
time-of-flight (`TOF`) to d-spacing then use cross-correlation or
single peak fitting to determine an `offset` which is nominally a
percentage difference of the conversion using the nominal `DIFC` and
what is actually needed.

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
     is representative.

   * Algorithm that performs bank-by-bank calibration to generate a
     multiplicative factor for each summed
     spectra. [EnggCalibrate](https://github.com/mantidproject/mantid/blob/v3.5.1/Code/Mantid/Framework/PythonInterface/plugins/algorithms/EnggCalibrate.py)
     is representative of this approach.

1. The code should work on any instrument that wants to calibrate
   using powder diffraction data. The instrument component hierarchy
   should be abstracted away as should the calibration
   sample/reference d-spacing.

1. The pixel-by-pixel option should produce `DIFC` for each
   pixel. Optionally (default is "on") it should allow for `DIFC`,
   `TZERO`, and `DIFA` with a preference for turning off extra terms
   for the smallest reduced chi-squared.

1. The resulting calibration should be usable in tools to update the
   `idf`. [AlignComponents](https://github.com/mantidproject/mantid/compare/master...rosswhitfield:AlignComponent)
   is an example of what would be needed. This is needed for better
   time-of-flight to wavelength conversion required by absorption
   corrections.

Design
======

In general there is a need to have a collection of
algorithms/functionality to calibrate the instrument. The calibration,
depending on whether operating on combined (in d-spacing) or
individual pixels (in time-of-flight).

Currently, much of the underlying peak finding/fitting is done in
`FindPeaks`. It may be better to move to a customized algorithm that
can make assumptions for powder diffraction. `FindPeaks` is the most
time-consuming, error-prone, and confusing step in the calibration
process.

Pixel-by-pixel
--------------

This calibration will work by converting information from d-spacing to
time-of-flight and determining the constants by calculating the
conversion from d-spacing (known positions) to time-of-flight
(observed positions).

1. Calculate fit windows and parameters. This would take a list of
   peaks in d-spacing, a calibration dataset, and a workspace
   index. The result is information about (in time-of-flight) the
   starting values for peak positions and fit windows. Ideally, this
   would also provide information for starting peak widths and
   heights. That is currently determined in `FindPeaks`.

1. Find the actual peak positions. The output (per spectrum) would be
   the peak positions, heights, and widths (in time-of-flight) as well
   as the reduced chi-squared for the peak fit.

1. Filter out spurious/unwanted observed peaks. The criteria in
   [GetDetOffsetsMultiPeaks](http://docs.mantidproject.org/v3.5.1/algorithms/GetDetOffsetsMultiPeaks-v1.html#criteria-on-peaks)
   should be used as possible/appropriate.

1. Calculate the calibration constants. For the pixel-by-pixel this
   would be `DIFC`, (up to) `TZERO` and `DIFA`. The
   [Gauss-Markov theorem](https://en.wikipedia.org/wiki/Gauss%E2%80%93Markov_theorem)
   should be used. Deciding which parameters will be used will be
   determined by using the reduced chi-squared to determine the "best"
   option. [FindPeakBackground](https://github.com/mantidproject/mantid/blob/v3.5.1/Code/Mantid/Framework/Algorithms/src/FindPeakBackground.cpp#L366)
   shows a way to compare.

Bank-by-bank
------------

This calibration determines a multiplicative constant, `need_name`,
which satisfies the equation (**CHECK THE MATH**)

```
d_exp = d_obs * need_name
```

This can then be factored into all of the pixel-by-pixel calibration
by simple multiplication, e.g. `DIFC_new = DIFC * need_name`. (**OTHER
EQUATION SHOULD CHANGE TO MAKE THIS CORRECT**)

1. The first three steps are the same as the pixel-by-pixel except for
   calculations and parameters are in d-spacing.

1. Calculate the calibration constants, `need_name`, which satisfy the
   equation above. Since it is a scalar, it can be calculated as the
   average `need_name` for each of the peaks in the observed
   spectrum. This is the 1-parameter version of the Gauss-Markov
   theorem.

Updating the `idf`
------------------

Most of this has been done. It involves merging
[AlignComponents](https://github.com/mantidproject/mantid/compare/master...rosswhitfield:AlignComponent)
into master, using
[ExportGeometry](https://github.com/mantidproject/mantid/blob/56237597171dfa7206e868e3eded497673d545cd/Framework/PythonInterface/plugins/algorithms/ExportGeometry.py),
and improving documentation on using the functionality.
