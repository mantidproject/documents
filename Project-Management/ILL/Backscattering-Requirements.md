## Backscattering Requirements

Original requirements documents:
 * [BS discussion](TOF_and_BS/Bastille_TOF_Discussion_Doc_020415.pdf)
 * [BS discussion notes](TOF_and_BS/Bastille_TOF_Discussion_Notes_020415.pdf)

A lot of work has already been implemented in Mantid for IN16b by Elliot Oram and Spencer Howells. Hence the time required on this should be relatively short, and much of it will focus on adding in similar functionality for IN13, filling in any gaps found, and verifying Mantid and Lamp give the same results.

For more information on the IN16b reduction see [Indirect Data Reduction](http://docs.mantidproject.org/nightly/interfaces/Indirect_DataReduction.html) and [IIndirectILLReduction](http://docs.mantidproject.org/nightly/algorithms/IndirectILLReduction-v1.html) document.

### General Algorithms Used

| Lamp Algorithm | Lamp Description | Mantid Equivalent | Mantid Description | Notes |
|---|---|---|---|---|
| <sub> bsnorm | <sub> Normalize with monitor spectrum for IN10, IN16, IN13 | <sub> [NormaliseToMonitor](http://docs.mantidproject.org/nightly/algorithms/NormaliseToMonitor-v1.html) | <sub> Normalizes a 2D workspace by a specified spectrum, spectrum, described by a monitor ID or spectrun provided in a separate worskspace. | <sub> Need to work out differences between Lamp's normalise and bsnorm |
| <sub> cylindercor | <sub> Absorption correction for annular cylinder | <sub> [CylinderAbsorption](http://docs.mantidproject.org/nightly/algorithms/CylinderAbsorption)* | <sub> Calculates bin-by-bin correction factors for attenuation due to absorption and single scattering in a ‘cylindrical’ sample. | <sub> No comparison has been made of these yet. |
| <sub> slab_tof | <sub> Takes a 2-D time-of-flight workspace and corrects for sample attenuation of the scattered neutrons assuming slab sample geometry.  | <sub> [FlatPlateAbsorption](http://docs.mantidproject.org/nightly/algorithms/FlatPlateAbsorption)* | <sub>  Calculates bin-by-bin correction factors for attenuation due to absorption and single scattering in a ‘cylindrical’ sample. | <sub> No comparison has been made of these yet. |
| <sub> tee | <sub> Perform conversion from channels to energy | <sub> [ConvertUnits](http://docs.mantidproject.org/nightly/algorithms/ConvertUnits-v1.html) | <sub> Performs a unit change on the X values of a workspace. | <sub> Need to determine any differences between Lamp's t2e and tee |
| <sub> rdset| <sub> Read and integrate PSD data | <sub> [GroupDetectors](http://docs.mantidproject.org/nightly/algorithms/GroupDetectors-v2.html)| <sub> Sums spectra bin-by-bin, equivalent to grouping the data from a set of detectors. | <sub> Sum over detector height of PSD |
| <sub> sqw_rebin | <sub> Rebins data to regular-grid S(Q,&#969;) covering the entire measured Q-E region | <sub> [SofQW](http://docs.mantidproject.org/nightly/algorithms/SofQW-v1.html) | <sub> Computes S(Q,&#969;) using a either centre point or parallel-piped rebinning. | <sub> Some minor differences exist here. See report by Wilcke for more information on the comparison. |

\* Note that CylinderAbsorption and FlatPlateAbsorption both inherit from the more general method [AbsoprtionCorrection](http://docs.mantidproject.org/nightly/algorithms/AbsorptionCorrection).

## Requirements for Mantid

Normalisation, absorption and SofQW should be addressed in the Time of Flight Spectroscopy work.

1. Verify loaders are still compatible with current data
1. Compare bsnorm to normalise in Lamp, compare this with Mantid
1. Compare tee and t2e in Lamp, and compare with ConvertUnits in Mantid
1. Compare integration of PSD data
1. Verify workflows for IN16b
1. Finalise workflows:
 * IN16b - already implemented
 * IN13
