## Time of Flight Spectroscopy Requirements

ISIS and SNS take two different approaches. ISIS relies mostly on Python scripts while the SNS use workflow algorithms. The SNS approach is more likely to be the one to follow. See [Data Reduction for Direct Geometry Neutron Spectrometers](https://github.com/mantidproject/documents/raw/master/Help/DGSReduction/DGSmain_v1_0.pdf) for more information on the workflow algorithms used.

Tasks:
* Evaluate what exists in LAMP and Mantid
 * Look at both SNS and ISIS workflows to determine which is the most useful approach
 * See if any extra work is required on the loaders - e.g. with configence levels, check format of NeXuS files
* Create requirements document for missing features
 * This will require working closely with instrument scientists at ILL
* Implement missing features
 * This will require working closely with instrument scientists at ILL
* Evaluate Mantid results against LAMP and resolve any major discrepancies

Relevant contacts are Alex Buts at ISIS and Stuart Campbell at SNS.

### General Algorithms Used

| Lamp Algorithm | Lamp Description | Mantid Equivalent | Mantid Description | Notes |
|---|---|---|---|---|
| <sub> rdsum | <sub> read and sum sample runs | <sub> (1) Load/LoadILL and  (2) MergeRuns | <sub> (1) Loads a ILL nexus file. (2) Combines the data contained in an arbitrary number of input workspaces. | <sub> Loaders exist for IN4, IN5 and IN6 already. Gives identical results to Lamp, but requires start and end points for each channel. |
| <sub> normalise | <sub> Normalises data to monitor or counting time. This should always be the first routine called after reading in the data. | <sub> NormaliseToMonitor | <sub> Normalizes a 2D workspace by a specified spectrum, spectrum, described by a monitor ID or spectrun provided in a separate worskspace. | <sub> No normalisation by time currently exists. |
| <sub> remove_spectra | <sub> Removes suspect spectra from a workspace. | <sub> MaskDetectors | <sub> In Mantid the spectra for the masked detectors are zeroed. In Lamp the unwanted spectra are removed completely. In Mantid the three monitor detectors are included in the workspace. Offsets aside, these results are otherwise identical. |
| <sub> vnorm | <sub>  Normalises data to vanadium. | <sub> NormaliseVanadium | <sub> Normalises all spectra to a specified wavelength. | <sub> Small discrepancy in normalaisations found by Wilcke. |
| <sub> cylindercor | <sub> Absorption correction for annular cylinder | <sub> [CylinderAbsorption](http://docs.mantidproject.org/nightly/algorithms/CylinderAbsorption)* | <sub> Calculates bin-by-bin correction factors for attenuation due to absorption and single scattering in a ‘cylindrical’ sample. | <sub> No comparison has been made of these yet. |
| <sub> slab_tof | <sub> Takes a 2-D time-of-flight workspace and corrects for sample attenuation of the scattered neutrons assuming slab sample geometry.  | <sub> [FlatPlateAbsorption](http://docs.mantidproject.org/nightly/algorithms/FlatPlateAbsorption)* | <sub>  Calculates bin-by-bin correction factors for attenuation due to absorption and single scattering in a ‘cylindrical’ sample. | <sub> No comparison has been made of these yet. |
| <sub> corr_tof | <sub> Corrects data in TOF for energy-dependence of detector efficiency, frame overlap and time-independent background. | <sub> [DetectorEfficiencyCorUser]() | <sub> This algorithm calculates the detector efficiency according the formula set in the instrument definition file/parameters. | <sub> These are not identical between Lamp and Mantid, despite DetectorEfficiencyCorUser attempting to replicate the Lamp behaviour. |
| <sub> t2e | <sub> Transforms time-of-flight data to energy transfer h &#969;. | <sub> ConvertUnits | <sub> Performs a unit change on the X values of a workspace. | <sub> The Lamp algorithm performs three steps - convert to dE, correct for Ki/Kf, correct for dT/dE. Mantid treats these separately, but does not have a separate dT/dE correction. The dT/dE correction seems to be done in the SofQW step in Mantid. Without the corrections in Lamp t2e and ConvertUnits are identical. |
| <sub> t2e - Ki/Kf | <sub> In Lamp Ki/Kf is part of t2e algorithm. | <sub> [CorrectKiKf](http://docs.mantidproject.org/nightly/algorithms/ConvertUnits-v1.html) | <sub> Performs k_i/k_f multiplication, in order to transform differential scattering cross section into dynamic structure factor. | <sub> A small difference was found between Lamp and Mantid, which is proporitonal to the counts. |
| <sub> sqw_rebin | <sub> Rebins data to regular-grid S(Q,&#969;) covering the entire measured Q-E region | <sub> [SofQW]() | <sub> Computes S(Q,&#969;) using a either centre point or parallel-piped rebinning. | <sub> Some minor differences exist here. See report by Wilcke for more information on the comparison. |
| <sub> reb | <sub> reb - Rebins data to regular steps in  with error bar propagation. | <sub> [Rebin](http://docs.mantidproject.org/nightly/algorithms/Rebin-v1.html)/[Rebin2D](http://docs.mantidproject.org/nightly/algorithms/Rebin2D-v1.html) | <sub> Rebins data with new X bin boundaries./Rebins both axes of a 2D workspace using the given parameters | <sub> Some minor differences exist here. See report by Wilcke for more information on the comparison. Note that the comments by Wilcke about preserving the count/integral should be resolvable, for plotting this is configurable under Preferences -> 2D plots -> Normalize histograms to bin width. |
| <sub> kis | <sub> Calculation of the susceptibility/omega (correction of the Bose population). | <sub> Not present | | |
| <sub> gdos | <sub> Calculate the generalised density of states using the P(alpha, beta) method | <sub> Not present | | <sub> A similar algorithm might be [simulated density of states](http://docs.mantidproject.org/nightly/algorithms/SimulatedDensityOfState). This requires simulation input. |
| <sub> muphcor | <sub> multiphonon contribution | <sub> Not present | | |

Also desirable is multiple scattering corrections. There is planned work on this by Martyn Gigg at ISIS.

\* Note that CylinderAbsorption and FlatPlateAbsorption both inherit from the more general method [AbsoprtionCorrection](http://docs.mantidproject.org/nightly/algorithms/AbsorptionCorrection).

### Instrument Specific Algorithms

| Lamp Algorithm | Lamp Description | Mantid Equivalent | Mantid Description | Notes |
|---|---|---|---|---|
| <sub> in4strip | <sub> Extracts sectors of the IN4 detector bank | <sub> Not present | | |
| <sub> in5_DebyeScherrer | <sub> Radial integration over Debye-Scherrer cones. | <sub> Not present | | |
| <sub> sumbank | <sub> Adds spectra together to improve statistics. Used on IN6 | <sub> Not present | <sub> ? | <sub> Should be straightforward to implement |

## Requirements for Mantid

1. Verify loaders are still compatible with current data
1. Time normalisation
1. Investigate discrepancy in vanadium normalisation
1. Compare cylinder and slab absorption corrections
1. Investigate differences in detector efficency corrections
1. Investigate difference in Ki/Kf correction in Mantid
1. Investigate SofQW differences
1. Investigate rebinning differences
1. Mantid kis equivalent
1. Mantid gdos equivalent
1. Mantid muphcor equivalent
1. Debye-Scherrer integration for IN5
1. Minor instrument routines
1. Investigate using DGS Workflow Algorithms, with modifications as required for ILL
