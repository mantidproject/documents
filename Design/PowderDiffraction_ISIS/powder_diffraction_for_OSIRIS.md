
# OSIRIS diffraction: status and requirements

## Introduction

Description of requirements for reducing OSIRIS powder diffraction
data. This is at the moment based on a first meeting with Sanghamitra
(2016/7/26).

The status as of this writing is as follows.

* Current OSIRIS routines for powder diffraction are included in the
workflow algorithm
[OSIRISDiffractionReduction](http://docs.mantidproject.org/nightly/algorithms/OSIRISDiffractionReduction-v1.html)

* The routines are used from the Indirect custom interface
(Indirect->Diffraction) which in principle supports IRIS, OSIRIS,
TOSCA and VESUVIO. It may be that only OSIRIS uses this interface in
practice. It seems that the integration with the GUI has some issues
and the algorithm does not work well when used from the GUI.

* For OSIRIS (possibly the other indirect instruments as well?)
  diffraction data can be acquired and processed in two modes:
  - Diffraction (powder) mode (**"diffonly"**)
  - Diffraction in spectroscopy mode (**"diffspec"**)

From ISIS diffraction instruments we currently have the following
[scripts](http://docs.mantidproject.org/nightly/api/python/techniques/PowderDiffractionISIS-v1.html):
* [Crystallography (CRY) scripts](http://docs.mantidproject.org/nightly/api/python/techniques/CryPowderDiffractionISIS-v1.html#cry-powder-diffraction-ref)
* [PEARL scripts](http://docs.mantidproject.org/nightly/api/python/techniques/PearlPowderDiffractionISIS-v1.html#pearl-powder-diffraction-ref)

Different variants of the CRY scripts are being used for the
instruments POLARIS, HRPD, and GEM. Diagrams and further details on
the CRY scripts can be found in several documents [available in the
documents
repository](https://github.com/mantidproject/documents/tree/master/Design/PowderDiffraction_ISIS). For
example, see this [list of algorithms used in the
workflow](https://github.com/mantidproject/documents/blob/master/Design/PowderDiffraction_ISIS/PowderDifIntro.md#mantid-algorithms-used).

At present PEARL scripts are used only for the instrument PEARL. These
are preferred long-term because they are simpler to understand and
consider absorption corrections in their workflow.


## Objectives for OSIRIS

Initially the focus is on the **"diffonly"** mode. **"diffspec"** is left for
later, when we have made some progress.

### General objective

1. Use (or harmonize) and extend the ISIS powder diffraction routines for OSIRIS

### More specific objectives

1. Support absorption corrections
2. Support calibration
3. Integrate with GUI (Interfaces->Indirect->Diffraction)

The first two steps are not currently well supported in the [OSIRIS
diffraction reduction
algorithm](http://docs.mantidproject.org/nightly/algorithms/OSIRISDiffractionReduction-v1.html).
There is a calibration file for OSIRIS (in .cal / ariel format), but
it is not being updated. There is no support at all for absorption
corrections. This could be the file `osiris_041_RES10.cal` which we
have in our test data.

### Longer term objectives

1. Produce a GSAS instrument parameters file (.prm/.par/.iparm) for
OSIRIS. Ideally it should work with GSAS I and II
1. Harmonize the two modes for OSIRIS diffraction: **"diffonly"**
(powder) and **"diffspec"** (spectroscopy)


## Requirements

OSIRIS will need cylinder and flat absorption corrections.

[PearlMCAbsorption](http://docs.mantidproject.org/nightly/algorithms/PearlMCAbsorption-v1.html)
does not seem to support what OSIRIS needs. Most likely we need to use
the newer algorithm
[AbsorptionCorrection](http://docs.mantidproject.org/nightly/algorithms/AbsorptionCorrection-v1.html)

A solution to calculate new calibrations is required. Sanghamitra
would like to draw from the calibration routines of other powder
diffraction instruments.

For diffraction experiments OSIRIS uses 11 modules. Every module
produces data in a different range of wavelength. All the wavelength
need to be combined (stitched together).

It seems that the [current workflow
algorithm](http://docs.mantidproject.org/nightly/algorithms/OSIRISDiffractionReduction-v1.html)
and the user interface are particularly inconvienent in that they will
process every module or wavelength range separately. Users need to
reduce the data for every module and then stitch. A higher level
workflow and graphical interface would be desirable.

Spectroscopy mode (**"diffspec"**) uses one single module / no modules
which implies that there are no issues with stitching in this mode.

According to Sanghamitra there is something in
[OSIRISDiffractionReduction](http://docs.mantidproject.org/nightly/algorithms/OSIRISDiffractionReduction-v1.html)
to handle the stitching. I might have misunderstood this point, or it
may be just that the data for each module is processed in a way that
the stitching is then trivial and does not require any
correction. There is no explicit stitching in the algorithm. We would
need to double-check how are users stitching the wavelength ranges.

### Inputs and outputs

Inputs that need to be processed include at least:
- Sample run (number and different extensions, including the n* and s* files)
- Container/empty can run
- Vanadium
- Attenuation
- Calibration (for [AlignDetectors](http://docs.mantidproject.org/nightly/algorithms/AlignDetectors-v1.html))

Some additional input (file(s)) will need to be introduced to specify
the list of modules and the corresponding ranges of
detectors/spectra. Alternatively this could be a default value for a
list of mininmum/maximum spectrun numbers for each module. A first
rough impression is that generalizing the inputs `SpectraMin` and
`SpectraMax` of the algorithm
[OSIRISDiffractionReduction](http://docs.mantidproject.org/nightly/algorithms/OSIRISDiffractionReduction-v1.html)
as vectors of min/max for every module could be all that is needed.


The outputs of the CRY and PEARL scripts seem to match the needs of
OSIRIS. The outputs would be saved into focused files in different
formats such as:
- [GSAS](http://docs.mantidproject.org/nightly/algorithms/SaveGSS-v1.html)
- [NeXus](http://docs.mantidproject.org/nightly/algorithms/SaveNexus-v1.html)
- XYE for TOPAS, FullProf or MAUD (algorithm
  [SaveFocusedXYE](http://docs.mantidproject.org/nightly/algorithms/SaveFocusedXYE-v1.html)).
