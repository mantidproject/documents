# TOF data reduction in Mantid: a draft

This document outlines a possible ILL TOF data reduction workflow in Mantid. The workflow is based on Björn Fåk's requests and is partially inspired by the TOFTOF workflow. Additionally, a comparison to the workflow algorithm `DgsReduction` is done.

## Workflow for the sample

1. Loading
  - Multiple runs are combined with `MergeRuns`.
  - Currently, metadata isn't handled correctly when merging.
    - TOFTOF uses its own `TOFTOFMergeRuns` to deal with the metadata. This could be extended to suit our needs as well.

2. Background subtraction
  - Basic subtraction using `CalculateFlatBackground`, takes care of monitors, as well.
  - Currently, it is not possible to use background from another dataset (e.g. low temperature measurement).
    - In any case, monitor background should always be calculated.
  - `DgsReduction` uses `CalculateFlatBackground` too.

3. Detector masking based on diagnostics
  - See below the discussion on the available algorithms.
  - `DgsReduction`: Done after vanadium normalization (step 9). A complex set of diagnostics is available.

4. Incident energy calibration (instrument dependent)
  - Currently, no suitable algorithm available.
  - `DgsReduction`: incident energy is always calculated using `GetEi` which is incompatible with ILL instruments.

5. Normalization to monitor
  - Default algorithm: `NormaliseToMonitor`. Additionally, monitor spectra could be corrected for efficiency using `MonitorEfficiencyCorUser`.
  - `DgsReduction`: ditto for `NormaliseToMonitor`.

6. Sample position fitting (optional, needs good quality elastic peaks or special vanadium run)
  - Currently, no suitable algorithm available.
  - If adjusting the TOF values would be enough, `CorrectTOF` could be used.
  - Proposal: have this as a separate algorithm whose output can be used during this workflow.

7. Transmission calculation
  - Several algorithms available, e.g. `AbsorptionCorrection` chooses a suitable one, or uses brute force.
  - `DgsReduction`: missing as no empty cell subtraction is included.

8. Empty can subtraction
  - Optionally, take Cd into account.
  - `DgsReduction`: not in this workflow.

9. Normalization to vanadium
  - Basic integration and division.
  - Or use `ComputeCalibrationCoefVan` which scales vanadium with regards to its temperature-dependent Debye-Waller factor.
  - `DgsReduction` just divides.

10. TOF to energy conversion
  - `ConvertUnits`
  - `DgsReduction`: done with `Rebin` between steps 4 and 5.

11. Correction for detector efficiency
  - ILL: `DetectorEfficiencyCorUser`
    - Note, that the formula provided for IN4 may be incorrect for the rosace detector.
    - There is also `NormaliseByDetector` which seems to use a per-component based correction formula.
  - SNS: `He3TubeEfficiency`
  - ISIS: `DetectorEfficiencyCor`

12. Differential scattering cross-section to dynamic structure factor conversion
  - Also known as `CorrectKiKf`.
  - 'DgsReduction': done with `Rebin` between steps 8 and 9.

13. Absolute normalization (optional)
  - `DgsReduction`: ditto.

## Detector diagnostics

The diagnostics should produce a mask workspace, used at the appropriate moment during the reduction.

* Hard-masking known problematic detectors
  - Proposal 1: include masked detectors in the IDF/IPF.
  - Proposal 2: forget about hard masks, rely solely on heuristics.

Note that the alogirthms below may expect the detectors to be of the same kind. Instruments like IN4 with its two detector types  may not work out-of-the-box.

* The following algorithms might be considered here:
  - `FindDetectorsOutsideLimits`
    - No heuristics, needs hard user-defined limits. Thus might be difficult to automatise.
    - Can be used to identify bad detectors based on both total counts and background levels.
  - `MedianDetectorTest`
    - Can be used to identify bad detectors based on both total counts and background levels.
  - `IdentifyNoisyDetectors`
    - Chooses bad detectors by statistical heuristics.
  - `DetectorEfficiencyVariation`
    - Needs two white beam vanadium runs, may not be applicable for ILL.
  - `CreatePSDBleedMask`
    - Is this applicable for ILL?

## Reduction steps not included in the above

* Data consistency check
  - An early visual inspection of data for unexpected changes, like sample flowing out of the neutron beam.
  - Proposal: have separate algorithm/GUI to visualise the data in the correct way.

* Frame overlap correction (optional)
  - Depends on sample physics.
  - Proposal: could be handled case-by-case using python scripts.

## Further tools/algorithms available in Mantid

* Rebinning
  - Done by `Rebin`.

* Detector grouping
  - Done by `GroupDetectors`.

* S(theta,w) -> S(Q,E)
  - Done by one of the `SofQW` algorithms and `CorrectKiKf`.
    - `SofQWNormalisedPolygon` seems to be closest to Lamp's `sqw_rebin`.

* Susceptibility (Bose population correction)
  - `ApplyDetailedBalance` seems to do the job.

* Generalized density of states
  - Done by `ComputeIncoherentDOS`.

## Missing data analysis tools

* Multiple scattering correction
  - At the moment has to be done post-reduction using external tools.

## Notes on other requested features

* Keeping the data of masked spectra intact
  - Mantid zeroes the masked data, but extraction to a separate workspace is possible.
