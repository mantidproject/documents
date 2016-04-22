# Mapping of the backend variables

The state of the current reduction workflow is spread across the `ReductionSingleton`,
the `ReductionStep`s, the `ISISInstrument` and some loaders. This is an attempt
to get a clearer understanding which settings need to be maintained by a state object.

It also tries to capture the dependency of the elements on the `ReductionSingleton`.

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

Base beam finder. Holds the position of the beam center. This is used by the `BeamCentreFinder` and the general reduction workflow.

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| _beam_center_x  | via `init`, `update_beam_center`(reducer) | in loaders and `BeamCentreFinder` | -|
| _beam_center_y  | via `init`, `update_beam_center`(reducer) | in loaders and `BeamCentreFinder` | -|
| _beam_radius  | -|-| not used|
| _data_file | -|-| not used|
| _persistent| -|-| not used|

#### State stored in Loaders

The reduction workflow needs information and handles on the different data files, ie.
Sample_Scatter, Sample_Transmission, Sample_Direct, Can_Scatter, Can_Transmission, Can_Direct.

### `LoadRun`
Loads a data file, moves its detector to the right position according
to the beam center and normalizes the data.

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| _data_file | via `init` ( essentially`LoadSample`) | internal | essentially the file name|
| _is_trans  | via `init`| internal |-|
| _reload   | via `init` | internal |-|
| _period   | via `init` | internal | also set in tests|
| _index_of_group   | via `init` and `move2ws` |  internal, `execute`(`LoadSample`), `_setUpPeriod`(ICI) | also used in tests |
| periods_in_file   | via `init` and when workspaces are being loaded| internally ?| -|
| ext   | via `init` and when workspaces are being loaded| internal | -|
| shortrun_no   | via `init` and when workspaces are being loaded| internal? | -|
| _wksp_name   | via `init` and when workspaces are being loaded| internal and in several other places| -|

**`ReductionSingleton` dependence**:
* in `getCorrspondingPeriod` the number of periods of `Sample` is compared with the periods of the `LoadRun` object (which can be in `Can` too)
* in `_assignHelper` the name of `ISISInstrument` is queried
* in `_assignHelper`  `ISISInstrument` is extracted and pass on to query instrument details


### `LoadSample`

This class inherits from `LoadRun` and hence contains all its connections.

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| _scatter_sample |  -      | -| not used|
| _SAMPLE_RUN | - |- | not used|
| maskpt_rmin| - |- | not used |
| entries | internal | interanl and tests | used by tests|

**`ReductionSingleton` dependence**:
* passes reducer to `_assignHelper` of `LoadRun`
* calls `on_load_sample` of the `ISISinstrument`
* calls `update_beam_center`


### `LoadTransmissions`

Loads the file used to apply the transmission correction to the
sample or can.

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| _direct_name |  `set_trans_sample`(reducer) and `set_trans_can`(reducer) | internal| -|
| _trans_name | `set_trans_sample`(reducer) and `set_trans_can`(reducer) | internal| -|
| trans | internal | `get_transmissions`(reducer) |-|
| direct| internal | `get_transmissions`(reducer) |-|
| _reload | via `init` | internal | -|
| _period_t | via `init` and `set_trans_can`(reducer) | internal |-|
| _period_d | via `init` and `set_trans_can`(reducer) | internal |-|
| can | via `init` | - | not used|


**`ReductionSingleton` dependence**:
* passed on to `_assignHelper`  of underlying loaders for transmission and direct
* calls `load_transmission_inst` of `ISISinstrument`


### `Sample`

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| ISSAMPLE |  internal | passed on to loaders  and internal | -|
| loader | via `init` and `set_run` which is called by reducer | reducer in several places |this is heavily used since it provides the name of the workspace, period numbers etc.|
|geometry| internal | internal and in `SampleGeomCorr`| -|
| run_option| via `set_run` | internal |-|
| reload_option | via `set_run` | internal |-|
| period_option | via `set_run` | internal |-|


**`ReductionSingleton` dependence**:
* passed on to the loader when it is being executed


### `Can`

See `Sample` description



##### State stored in `ReductionSingleton`

The `RedcutionSingleton` stores not only indirectly state via the `instrument`,
the loaders and the `ReductionStep`s, but it contains state by itself as well.

TODO

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

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| _names | internal | `isAlias` and `name` are used all over the place | -|
| _shape | internal | used by `spectrum_block` and `set_first_spec` which are used by `Mask_ISIS` and the concrete instruments
| n_columns | internal | queried by `GetInstrumentDetails`(ICI) | -|
| correction_file | via `UserFile` | `read_mon_lin`(`UserFile`), `SetCorrectionFile`(ICI), `calculate`(`CalculateNormISIS`),  GUI via `detector_file`(`ISISinstrument`) |-|
| z_corr | `_readDetectorCorrections`(`UserFile`), `SetDetectorOffsets`(ICI)| individual insturments |-|
| x_corr | see z_corr| see z_corr| -|
| _y_corr | see z_corr| see z_corr |-|
| _rot_corr| see z_corr| see z_corr |-|
| _side_corr| see z_corr| see z_corr |-|
| x_tilt| see z_corr| see z_corr |-|
| y_tilt| see z_corr| see z_corr |-|
| rescaleAndShift| `_readFrontRescaleShiftSetup`(`UserFile`), `SetFronDetRescaleShift`(ICI), `WavRangeReduction`(ICI)| `WavRangeReduction`(ICI), several places in GUI| -|
| _orientation | set by individial instruments | internal| -|


###### `ISISInstrument`

This is dereived from `BaseInstrument`, hence it contains its members too.

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| idf_path | `_defintion_file` from `BaseInstrument`| reducer to reset IDF | -|
| _incid_monitor | extracted from `definition`, ``set_incident_mon` called by `SANS2D` instrument | `loadUserFile`(GUI), `execute`(`NormalizeToMonitor`)
| cen_find_step |  extracted from `definition` | used in `BeamCentreFinder`| -|
| cen_find_step2|  extracted from `definition` | used in `BeamCentreFinder`| -|
| beam_centre_scale_factor1 | extracted from `definition` | used in `BeamCentreFinder`| -|
| beam_centre_scale_factor2 | extracted from `definition` | used in `BeamCentreFinder`| -|
| det_selection | via `setDetector` all over the place | direct in GUI and internal |-|
| DETECTORS | many accessor methods in the concrete instruments | all over the place | contains the names of the banks|
| _use_interpol_norm | `SpetMonitorSpectrum`(ICI) directly through reducer | `is_interpolating_norm` used by `NormalizeToMonitor` and GUI | - |
| use_interpol_trans_calc | - |- |not used|
| SAMPLE_Z_CORR | `read_line`(`UserFile`), `SetSampleOffset`(ICI)| GUI | used for moving the components|
| FRONT_DET_RADIUS | internal | `SANS2D` | should be in `SANS2D`|
| FRONT_DET_DEFAULT_SD_M | internal | `SANS2D` | should be in `SANS2D`|
| FRONT_DET_DEFAULT_X_M | internal | `SANS2D` | should be in `SANS2D`|
| REAR_DET_DEFAULT_SD_M | internal | `SANS2D` | should be in `SANS2D`|
| FRONT_DET_X | internal | `SANS2D` | should be in `SANS2D`|
| FRONT_DET_Z | internal | `SANS2D` | should be in `SANS2D`|
| FRONT_DET_ROT | internal | `SANS2D` | should be in `SANS2D`|
| REAR_DET_Z | internal | `SANS2D` | should be in `SANS2D`|
| REAR_DET_X | internal | `SANS2D` | should be in `SANS2D`|
| BENCH_ROT | internal | `LARMOR` | should be in `LARMOR`|
| default_trans_spec | extracted from `definition` | used by `TransmissionCalc`|-|
| incid_mon_4_trans_calc | extracted from `definition`, `SetTransSpectrum`(ICI) | used by `TransmissionCalc`, directly by GUI|-|
| run_number_width| internal|-| not used|
| _del_incidient_set | internal | internal | see not usefull anymore|
| _back_ground | `setTOFs` via `UserFile` | `NormalizeToMonitor`, `TransmissionCalc`| -|
| _back_start| `setTOFs` via `UserFile` | `NormalizeToMonitor`, `TransmissionCalc`| -|
| _back_start_ROI| `setTOFs` via `UserFile` | `NormalizeToMonitor`, `TransmissionCalc`| -|
| _back_end_ROI| `setTOFs` via `UserFile` | `NormalizeToMonitor`, `TransmissionCalc`| -|
| monitor_zs | -| internal| not really used|
| _newCalibrationWS | `UserFile` and when workspace is loaded | internal |-|
| beam_centre_pos1_after_move| internal | `BeamCentreFinder` and reducer |-|
| beam_centre_pos2_after_move| internal | `BeamCentreFinder` and reducer |-|



###### LOQ

Contains specifics for the LOQ instrument

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| _NAME |  internal | reducer and `WavRangeReduction`(ICI) |-|
| WAV_RANGE_MIN |  internal | GUI, `TransmissionCalc`  |-|
| WAV_RANGE_MAX | internal | GUI, `TransmissionCalc`  |-|
| monitor_names | internal | internal |-|



###### SANS2D

Contains specifics for the LOQ instrument

| Variable    |  Origin          | Used in                               | Other comment  |
|-------------|------------------|--------------------------------------|----------------|
| _NAME |  internal | reducer and `WavRangeReduction`(ICI) |-|
| WAV_RANGE_MIN |  internal | GUI, `TransmissionCalc`  |-|
| WAV_RANGE_MAX | internal | GUI, `TransmissionCalc`  |-|
| _marked_dets | internal | internal |-|
| corrections_applied | internal, when loading a workspace| internal |-|
| _can_logs | 






###### LARMOR
