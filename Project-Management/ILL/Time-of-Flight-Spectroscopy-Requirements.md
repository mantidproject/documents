## Time of Flight Spectroscopy Requirements

ISIS and SNS take two different approaches. ISIS relies mostly on Python scripts while the SNS use workflow algorithms. The SNS approach is more likely to be the one to follow.

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

General Algorithms Used

| Lamp Algorithm | Lamp Description | Mantid Equivalent | Mantid Description | Notes |
|---|---|---|---|---|
| rdsum |read and sum sample runs | (1) Load/LoadILL and  (2) MergeRuns | (1) Loads a ILL nexus file. (2) Combines the data contained in an arbitrary number of input workspaces. | Loaders exist for IN4, IN5 and IN6 already. Gives identical results to Lamp, but requires start and end points for each channel. |
| normalise | Normalises data to monitor or counting time. This should always be the first routine called after reading in the data. | NormaliseToMonitor | Normalizes a 2D workspace by a specified spectrum, spectrum, described by a monitor ID or spectrun provided in a separate worskspace. | No normalisation by time currently exists. |
| remove_spectra | Removes suspect spectra from a workspace. | MaskDetectors | In Mantid the spectra for the masked detectors are zeroed. In Lamp the unwanted spectra are removed completely. In Mantid the three monitor detectors are included in the workspace. Offsets aside, these results are otherwise identical. |
| vnorm | Normalises data to vanadium. | NormaliseVanadium | Normalises all spectra to a specified wavelength. | Small discrepancy in normalaisations found by Wilcke. |
| cylindercor | Absorption correction for annular cylinder | [CylinderAbsorption](http://docs.mantidproject.org/nightly/algorithms/CylinderAbsorption)* | Calculates bin-by-bin correction factors for attenuation due to absorption and single scattering in a ‘cylindrical’ sample. | No comparison has been made of these yet. |
| slab_tof | Takes a 2-D time-of-flight workspace and corrects for sample attenuation of the scattered neutrons assuming slab sample geometry.  | [FlatPlateAbsorption](http://docs.mantidproject.org/nightly/algorithms/FlatPlateAbsorption)* | Calculates bin-by-bin correction factors for attenuation due to absorption and single scattering in a ‘cylindrical’ sample. | No comparison has been made of these yet. |
| corr_tof | Corrects data in TOF for energy-dependence of detector efficiency, frame overlap and time-independent background. | DetectorEfficiencyCorUser | This algorithm calculates the detector efficiency according the formula set in the instrument definition file/parameters. | These are not identical between Lamp and Mantid, despite DetectorEfficiencyCorUser attempting to replicate the Lamp behaviour. |
| t2e | Transforms time-of-flight data to energy transfer h &#969;. | ConvertUnits | Performs a unit change on the X values of a workspace. |  The Lamp algorithm performs three steps - convert to dE, correct for Ki/Kf, correct for dT/dE. Mantid treats these separately, but does not have a separate dT/dE correction. The dT/dE correction seems to be done in the SofQW step in Mantid. Without the corrections in Lamp t2e and ConvertUnits are identical. |
| t2e - Ki/Kf | In Lamp Ki/Kf is part of t2e algorithm. | CorrectKiKf | Performs k_i/k_f multiplication, in order to transform differential scattering cross section into dynamic structure factor. | A small difference was found between Lamp and Mantid, which is proporitonal to the counts. |
| sqw_rebin | Rebins data to regular-grid S(Q,&#969;) covering the entire measured Q-E region | SofQW | Computes S(Q,&#969;) using a either centre point or parallel-piped rebinning. | Some minor differences exist here. See report by Wilcke for more information on the comparison. |
| reb | reb - Rebins data to regular steps in  with error bar propagation. | SofQW | Computes S(Q,&#969;) using a either centre point or parallel-piped rebinning. | Some minor differences exist here. See report by Wilcke for more information on the comparison. |
| kis | Calculation of the susceptibility/omega (correction of the Bose population). | Not present | | |
| gdos | Calculate the generalised density of states using the P(alpha, beta) method | Not present | | A similar algorithm might be [simulated density of states](http://docs.mantidproject.org/nightly/algorithms/SimulatedDensityOfState). This requires simulation input. |
| muphcor | multiphonon contribution | Not present | | |

Also desirable is multiple scattering corrections. There is planned work on this by Martyn Gigg at ISIS.

* Note that CylinderAbsorption and FlatPlateAbsorption both inherit from the more general method [AbsoprtionCorrection](http://docs.mantidproject.org/nightly/algorithms/AbsorptionCorrection).


Instrument Specific Algorithms

| Lamp Algorithm | Lamp Description | Mantid Equivalent | Mantid Description | Notes |
|---|---|---|---|---|
| in4strip ||||
| in5_DebyeScherrer | Radial integration over Debye-Scherrer cones. ||||
| sumbank | Adds spectra together to improve statistics. Used on IN6 | ? | ? | ? |
