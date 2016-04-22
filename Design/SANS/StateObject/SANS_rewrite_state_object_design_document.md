# State Object of the new SANS reduction workflow

## Abreviations

The following abreviations will be used below:
* `ISISCammondInterface` : ICI
* in-place: i-p
* Graphical User Interface. Essentially the `C++` part: GUI
* CentreFinder: CF

## Motivation

The SANS reduction workflow makes use of the so-called `ReductionSingleton`, which
essentially stores the configurational state either directly or in an `ISISInstrument`
object. The individual reduction steps extract their required state from this
`RedcutionSingleton`. The reduction steps are deeply coupled to the  `ReductionSingleton`,
which makes it hard to unit test them (and probably explains why such tests do not exist).
In addition there is a strong coupling of this `ReductionSingleton` to the
GUI logic, which essentially renders the ISIS SANS reduction a monolithic block.

A more modern approach is to use Mantid WorkflowAlgorithms. This mechanism avoids
the deep coupling. Individual steps would be supplied the required workspaces
and additional information and they return an adequate output workspace.
This would create an ideal environment for unit testing and documentation.

## Current status

As described above the state is stored in the `ReductionSingleton`, the `ISISInstrument`
and its implementations and partially also in the `ReductionSteps` themselves.
Below we provide a mapping of the entire state of the current reduction workflow.

### Location of state in the current SANS reducer/instrument/steps

#### State stored in `ReductionStep`s and their dependence on the `ReductionSingleton`

Most of the state is stored in the reduction steps which in turn are managed by
the reducer. We will go through each reduction step and also through other units of
work, e.g. `Sample` which are not technically `ReductionStep`s but contain state
information.


### `SliceEvent`

This step converts an `EventWorkspace` into a `Workspace2D`. It can either convert
the entire data set or it can convert a slice.

| Variable  |  Origin        | Usage                     | Other comment  |
|-----------|----------------|---------------------------|----------------|
| scale     | calc. i-p      | records fraction of charge| not true state |

The `SliceEvent` does not directly store a true state. The produced scale, which
is the fraction of the total charge in the slice is important for `NormalizeToMonitor`.

**`ReductionSingleton` dependence**:
* from `settings` the *events.binning* are queried
* from `getCurrSliceLimits` the start and stop limits are extracted
* `is_can` is being queried
* via the `Sample` the monitor is queried

### `CropDetBank`

The SANS reduction workflow deals with a detector bank at a time. After the data
set has been loaded and potentially sliced, the spectra corresponding to detector
banks which are not currently being investigated are removed.

This `ReductionStep` does not store any direct state.

**`ReductionSingleton` dependence**:
* from `instrument` the current detector is selected and the `crop_to_detector`
  method is being used to crop the workspace


### `Mask_ISIS`

Marks some spectra so that they are not included in the analysis
Provides ISIS specific mask functionality (e.g. parsing
MASK commands from user files).

| Variable  |  Origin        | Usage                     | Other comment  |
|-----------|----------------|---------------------------|----------------|
| _xml         | internal | internal | - |
| _detect_list |  -       | -          | not used|
| masked_pixels | -      |   -        | not used
| time_mask | via `init`, `parse_instruction` | internal and `updateMaskTable`(GUI) | -|
| time_mask_r | via `init`, `parse_instruction` | internal and `updateMaskTable`(GUI) | -|
| time_mask_f | via `init`, `parse_instruction` | internal and `updateMaskTable`(GUI) | -|
| spec_mask_r | via `init`, `parse_instruction` | internal and `updateMaskTable`(GUI) | -|
| spec_mask_f | via `init`, `parse_instruction` | internal and `updateMaskTable`(GUI) | -|
| mask_phi    | via `init`, `parse_instruction`, `SetPhiLimit`(ICI), SeekCentre(CF), `readLimitValues`(`UserFile`) | `get_phi_limits_tag` called by reducer | -|
| mask_phi    | via `init`, `parse_instruction`, `set_phi_limit`, SeekCentre(CF), `readLimitValues`(`UserFile`) | `LoadUserFile`(GUI) | -|
| _lim_phi_xml | internal | internal |-|
| phi_min |  via `init`, `parse_instruction`, `set_phi_limit`,`SetPhiLimit`(ICI) | `get_phi_limits_tag` called by reducer, `loadUserFile`(`GUI`) | -|
| phi_max  | via `init`, `parse_instruction`, `set_phi_limit`, `SetPhiLimit`(ICI) | `get_phi_limits_tag` called by reducer, `loadUserFile`(`GUI`) |-|
| _readonly_phi | via `init`, `set_phi_limit`, | internal | -|
|_numberOfTimesSetPhiLimitBeenCalled| -|-| not used|
| spec_list| internal | internal |-|
|arm_width | via `init`, `parse_instruction` | internal and `updateMaskTable`(GUI)| -|
|arm_angle | via `init`, `parse_instruction` | internal and `updateMaskTable`(GUI)| -|
|arm_x | via `init`, `parse_instruction` | internal and `updateMaskTable`(GUI)| -|
|arm_y | via `init`, `parse_instruction` | internal and `updateMaskTable`(GUI)| -|
|min_radius | via `init`, `set_radi` used by `readLimitValues`(`UserFile`) and `LimitsR`(ICI) | internal, `createColleteScript`(ICI), `loadUserFile`(GUI)| -|
|max_radius | via `init`, `set_radi` used by `readLimitValues`(`UserFile`) and `LimitsR`(ICI) | internal, `createColleteScript`(ICI), `loadUserFile`(GUI)| -|

**`ReductionSingleton` dependence**:
* obtains the `instrument`
* obtains the current detector via `cur_detector`
* gets "MaskFiles" from `settings`
* obtains the idf path from the `instrument` via `idf_path`
* uses `name` from the `instrument`
* uses `isAlias` on the current detector
* uses `spectrum_block` on current detector


The `Mask_ISIS` redcution step is also responsible for viewing the masking in the *InstrumentView*. The `ReductionSingleton` dependence for this is:
* obtains the `instrument`
* gets names of all detectors (`cur_detector` and `other_detector`)
* resets detectors on the `instrument`
* deletes workspaces via `deleteWorkspaces`



### `UnitsConvert`

Converts the units from TOF to Wavelength and provides additional rebinning.


| Variable    |  Origin          | Used in                               | Other comment  |
|-----------  |------------------|--------------------------------------|----------------|
| _units      | set via `init`    | target unit for `ConvertUnits`                        | -|
| wav_low     |`LimitsWav`(ICI), `WavRangeReduction`(ICI), `readLimitValues`(`UserFile`) | `TransmissionCalc`, `createColleteScript`(ICI), `get_out_ws_name`(`ReductionSingleton`)| Lower wavelength limit|
|wav_high   | see wav_log     | see wav_low     | Upper wavelength limit|
|wav_step   | see wav_log     | see wav_low     | Wavelength step for rebinning|        
|rebin_alg  | set via `init` default to *Rebin* | selects bin algorithm | contained in step |
|_bin_alg   | -| -|   Not used |

**`ReductionSingleton` dependence**:
None

### `NormalizeToMonitor`

Creates an incident monitor workspace. It removes the prompt peak for LOQ and
does a flat background correction. At this point we also correct the monitor counts
by the scale obtained in `SliceEvent`. Finally the a rebin to wavelength is performed (using
the same bin parameters as above). The result is later on used by the `CalculateNormISIS` in `ConvertToQISIS`.

| Variable    |  Origin          | Used in                               | Other comment  |
|-----------  |------------------|--------------------------------------|----------------|
| _normalization_spectrum | set via `init` to default (none)   |  internal    | This is being reset by the `execute` method. Appears to be unnecessary.|
| output_wksp | internal |  `CalculateNormISIS` | -|

**`ReductionSingleton` dependence**:
* obtains the scale from `SliceEvent`
* obtains the incident monitor spectrum number via `instrument` and the `get_incident_mon` method
* obtains a reference to the monitor via the `Sample` object and the `get_monitor` method
* obtains the name of the `instrument` (to perform corrections for LOQ)
* obtains information for the LOQ correction from `TransmissionCalc` (`loq_removePromptPeakMin`) via the `RedcutionSingleton`
* obtains the TOF via `instrument` and the `get_TOFs` method
* obtains information wether we have a an interpolating norm via `instrument` and the `is_interpolating_norm` method
* obtains the `UnitsConvert` step to perform unit conversion

### `TransmissionCalc`

Calculates the proportion of neutrons that are transmitted through the sample
as a function of wavelength. The results are stored as a separate workspace and later on used by
`CalculateNormISIS` in `ConvertToQISIS`.

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| trans_mon   | `_read_transpec`(`UserFile`), `SetTransmissionMonitorSpectrum`(ICI), `UnsetTransmissionMonitorSpectrum`(ICI)| `GetTransmissionMonitorSpectrum`(ICI) and internal | -|
| trans_roi   | internal          | internal           | -|
| radius      | `_read_trans_line`(`UserFile`), `SetTransmissionRadiusInMM`(ICI) | `GetTransmissionRadiusInMM`(ICI) and internal | -|
|roi_files    | `_read_trans_line`(`UserFile`), `SetTransmissionROI`(ICI) |`GetTransmissionROI`(ICI) and internal |-|
| mask_files  |  `set_trans_spectrum`(`UserFile`), `SetTransmissionMask`(ICI) | `GetTransmissionROI`(ICI)| -|
| interpolate | `_read_mon_line`(`UserFile`), `set_trans_spectrum`(reducer), `SetTransSpectrum`(ICI)  `loadUserFile`(GUI)| internal |-|
|calculated_samp | `_read_trans_samplews`(`UserFile`), `TransWorkspace`(ICI) | internal| - |
|calculated_can | `_read_trans_samplews`(`UserFile`), `TransWorkspace`(ICI) | internal| - |
|output_wksp  | internal | `ConvertToQISIS`(SANSWideAngelCorrection), `reduce_can`(reducer), post_process(reducer)| what a mess|
|loq_removePromptPeakMin | `read_line`(`UserFile`) | RemoveBins(`NormalizeToMonitor`), internal | -|

**`ReductionSingleton` dependence**:
* checks if is can via `is_can`
* gets transmission workspaces via `get_transmissions` (for either can or sample)
* from `instrument` gets the incident monitor (`incid_mon_4_trans_calc`)
* from `instrument` gets a default transmission spectrum (`default_trans_spec`)
* checks if instrument default range should be used via `full_trans_wav`
* obtains instrument default range from `instrument` via `WAV_RANGE_MIN` and `WAV_RANGE_MAX`
* obtains wavelength min, step and max from `UnitsConvert`: `wav_low` and `wav_high`, `wav_step`
* obtains rebin method of `UnitsConvert` via `get_rebin`
* deletes workspaces via `deleteWorkspaces`
* gets the TOF from the `instrument` via `get_TOFs` and `get_TOFs_for_ROI`
* gets the instrument name (for LOQ - peak correction)
* used for `DarkRunSubtraction` of transmission data set
* gets IDF information from `instrument` via `idf_path`

### `AbsoluteUnitsISIS`

Scales the cross section calculation.


| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| rescale| `_initialize_mas`(`UserFile`), `restore_defaults`(`UserFile`), `read_line`(`UserFile`)                         |GUI and internal | -|

**`ReductionSingleton` dependence**:
* from `instrument` gets name (for LOQ Colette script correction)


### `SampleGeomCorr`

Correct the neutron count rates for the size of the sample.

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| volume      | internal         | internal                              | -  |

**`ReductionSingleton` dependence**:
* checks if it is can `is_can`
* gets the `GetSampleGeom` step from the `Sample` and uses shape information to calculate the volume

### `GetSampleGeom`

Loads, stores, retrieves, etc. data about the geometry of the sample.On initialisation
this class will return default geometry values (compatible with the Colette software)
If there is geometry information in the sample workspace this will override any
unset attributes.

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| _shape      | `readSampleObjectChanges`(GUI) and internal from workspace sample logs | `calculate_volume`(`SampleGeomCorr`) |-|
| _width     | `readSampleObjectChanges`(GUI) and internal from workspace sample logs | `calculate_volume`(`SampleGeomCorr`) |-|
| _thickness   | `readSampleObjectChanges`(GUI) and internal from workspace sample logs | `calculate_volume`(`SampleGeomCorr`) |-|
| _height     | `readSampleObjectChanges`(GUI) and internal from workspace sample logs | `calculate_volume`(`SampleGeomCorr`) |-|
| _use_wksp_shape| internal | internal | -|
| _use_wksp_width| internal | internal | -|
| _use_wksp_thickness| internal | internal | -|
| _use_wksp_height| internal | internal | -|

Note that this "`ReductionStep`" is not part of the actual reduction chain but is part of the
`Sample` which is manged by the `ReductionSingleton`.

**`ReductionSingleton` dependence**:
None


### `CalculateNormISIS`

This is not a reduction step but it uses the result of two steps to calculate the
normalization workspaces which is used by `ConvertToQISIS`.

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| _wave_steps | `init`           | internal               |-|
| _high_angle_pixel_file | via `setPixelCorrFile` in `execute`(`UserFile`) and `read_mon_line`(`UserFile`) and `SetDetectorFloodFile`(ICI)|-|
| _low_angle_pixel_file | via `setPixelCorrFile` in `execute`(`UserFile`) and `read_mon_line`(`UserFile`) and `SetDetectorFloodFile`(ICI)|-|
| _pixel_file | internal  | internal | -|


**`ReductionSingleton` dependence**:
* gets the correction file from `instrument` -> `cur_detector` via `correction_file`
* gets the name of the current detector from `instrument` -> `cur_detector` via `name`
* gets the output workspace name `output_wksp`
* crops to the detector with `crop_to_detector`
* deletes workspaces with `deleteWorkspaces`


### `ConvertToQISIS`
Runs the Q1D or Qxy algorithms to convert wavelength data into momentum transfer.
It also applies the wide angle correction and performs normalization. This is where
everything comes together.

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| _norms      | via `init`       | internal                              | is a `CalculateNormISIS` object|
| _output_type| TODO | TODO | TODO
| _Q_alg | TODO | TODO | TODO|
| _use_gravity | `set_gravity` used by `Gravity`(ICI) and `read_line`(`UserFile`) | `loadUserFile`(GUI) and internal | -|
| _grav_set | internal | interanl |-|
| _grav_extra_length | `set_extra_length` used by `Gravity`(ICI) and `read_line`(`UserFile`) | `loadUserFile`(GUI) and internal | -|
| _grav_extra_length_set | internal | internal | -|
| binning | `readLimitValues`(`UserFile`), internal | `Q_string`(reducer), `loadUserFile`(GUI) and internal | -|
| r_cut | `intializeMask`(`UserFile`), `readLimitValues`(`UserFile`) | internal | -|
| w_cut | see r_cut | see r_cut | -|
| outputParts | WavRangeReduction(ICI) | internal | this is used for merged reduction|
| use_q_resolution | set via `UserFile` and ICI function | ICI for GUI, internal | -|
| _q_resolution_moderator_file_name | set via `UserFile` and ICI function | ICI for GUI, internal | -|
| _q_resolution_delta_r | set via `UserFile` and ICI function | ICI for GUI, internal | -|
| _q_resolution_a1 | set via `UserFile` and ICI function | ICI for GUI, internal | -|
| _q_resolution_a2 | set via `UserFile` and ICI function | ICI for GUI, internal | -|
| _q_resolution_h1 | set via `UserFile` and ICI function | ICI for GUI, internal | -|
| _q_resolution_w1 | set via `UserFile` and ICI function | ICI for GUI, internal | -|
| _q_resolution_h2 | set via `UserFile` and ICI function | ICI for GUI, internal | -|
| _q_resolution_w2 | set via `UserFile` and ICI function | ICI for GUI, internal | -|
| _q_resolution_collimation_length | set via `UserFile` and ICI function | ICI for GUI, internal | -|

**`ReductionSingleton` dependence**:
* get flat for wide angle correction: `wide_angle_correction`
* check if transmission output exists on `TransmissionCalc` via `output_wksp`
* get `QXY2` and `DQXY`
* remove unused workspaces with `deleteWorkspaces`


### `CanSubtraction`

Applies the same corrections to the can that were applied to the sample and
then subtracts this can from the sample.

Does not contain internal state, since it mainly uses the already existing
reduction chain.

**`ReductionSingleton` dependence**:
* check if can exists with `get_can`
* runs the reduction with `reduce_can`
* check if `output_type` of `ConvertToQISIS` is 1D

### `StripEndNans`

For 1D workspaces removes NANs from the head and the tail of the workspace.
This step does not have any state variables nor any dependency on the `ReductionSingleton`.


### `DarkRunSubtraction`

TODO


### `UserFile`
Reads an ISIS SANS mask file of the format described here mantidproject.org/SANS_User_File_Commands

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| filename    | via `init`, `MaskFile`(ICI) | used extensively in the GUI | -|
| _incid_monitor_lckd | internal | internal | -|
| executed | internal | `set_sample`(reducer)| -|

The dependence on the `ReductionSingleton` is huge, since for each parsed entry
in the user file information is stored either in the `ReductionSingleton`, the `instrument`
or the `ReductionStep`s. It wouldn't make much sense to map out this dependency, since
it is being mapped out via the recipients of the information.

### `BaseBeamFinder`

TODO


#### State stored in Loaders

The reduction workflow needs information and handles on the different data files, ie.
Sample_Scatter, Sample_Transmission, Sample_Direct, Can_Scatter, Can_Transmission, Can_Direct.

### `LoadRun`
Loads a data file, moves its detector to the right position according
to the beam center and normalizes the data.

TODO

### `LoadSample`
TODO
### `LoadTransmissions`
TODO
### `Sample`
TODO
### `Can`
TODO

##### State stored in `ReductionSingleton`

The `RedcutionSingleton` stores not only indirectly state via the `instrument`,
the loaders and the `ReductionStep`s, but it contains state by itself as well.



##### State stored in instrument

One of the more tangled elements is the `ISISinstrument` which is being used in many places
and contains instrument specific information. It is derived from `BaseInstrument`. All of
these elements do not depend on the `ReductionSingleton`.

###### `BaseInstrument`

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| _definition_file | via `init`, | indirectly by calls to `get_idf_path` | this is the path to the IDF|
| definition | via `init` | internal | loads the instrument to get the instrument parameters, uses `LoadEmptyInstrument`|

###### `DetectorBank`

The detector bank contains integral geometry information about either the high-angle or
low angle bank



###### LOQ

###### SANS2D

###### LARMOR


##### State in the GUI

For a detailed analysis of the GUI and its coupling to the reducer backend see *SANS_Mapping_of_GUI_variables.md*




## State Object approach

### Sub State approach

### Using Mantid's `PropertyManager` as maps

### Mapping of old state to new State Object
