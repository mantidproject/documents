# Mapping of the GUI variables

## Abreviations

The following abbreviations and synonymns will be used below:
* `ISISCammondInterface` : ICI
* Graphical User Interface: GUI
* the word "reducer" will be used in places for `ReductionSingleton`

## Purpose
This document tries to scope the level of connectedness of the GUI with the
reducer back-end. The initial design goal of the ISIS SANS reduction interface (and back-end)
was to have a single communication layer which should be provided by the ICI. Currently
there is tight coupling between the GUI and the back-end. This document tries to show to which level these two elements are coupled. 

For gravity:

| Gui Name                | Variable in back-end  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| `gravity_check`         |  `use_gravity`(`ConvertToQISIS`) | `get_gravity`(`ConvertToQISIS`), `Gravity`(ICI)| -|
| `gravity_extra_length_line_edit` | `_use_gravity`(`ConvertToQISIS`) | `get_extra_length`(`ConvertToQISIS`), `Gravity`(ICI)| -|

For limits:

| Gui Name                | Variable in back-end  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| rad_min | `min_radius`(`Mask_ISIS`) | direct, `readLimitValues`(`UserFile`)| -|
| rad_max | `max_radius`(`Mask_ISIS`) | direct, `readLimitValues`(`UserFile`)| -|
| wav_min | `wav_low`(`ConvertUnits`) | direct, `LimitsWav`(ICI)| -|
| wav_max | `wav_high`(`ConvertUnits`) | direct, `LimitsWav`(ICI)| -|
| wav_dw  | `wav_step`(`ConvertUnits`) | direct, `LimitsWav`(ICI)| -|
| wav_dw_opt | translated into a rebin string by (`readLimitValues`)`UserFile` | `UnitsConvert` | -|
| q_min | `binning`(`ConvertToQISIS`)| direct, `readLimitValues`(`UserFile`) | `binning` is a comma separated string of variables |
| q_max | `binning`(`ConvertToQISIS`)| direct, `readLimitValues`(`UserFile`) | `binning` is a comma separated string of variables |
| q_dq  | `binning`(`ConvertToQISIS`)| direct, `readLimitValues`(`UserFile`) | `binning` is a comma separated string of variables |
| q_dq_opt |ranslated into a rebin string by (`readLimitValues`)`UserFile` | `ConvertToQISIS` | -|
| qy_max | `QXY2`(reducer) | direct, `LimitsQXY`(ICI)| the min seems to always start from 0|
| qy_dqy | `DQXY`(reducer) | direct, `LimitsQXY`(ICI)| -|
| qy_dqy_opt | part of `DQXY`(reducer) | `ConvertToQISIS`|-|
| trans_selector_opt| `fit_settings`(`TransmissionCalc`)| `isSeparate`(`TransmissionCalc`) + ?| -|
| transFitOnOff| `fit_settings`(`TransmissionCalc`)| `TransFit`(ICI), `fitMethod`(`TransmissionCalc`)| -|
| transFit_ck| ?| ?| -|
| trans_min| `fit_settings`(`TransmissionCalc`) | lamdaMin(`TransmissionCalc`), `TransFit`(ICI)| -|
| trans_max| `fit_settings`(`TransmissionCalc`)| lamdaMax(`TransmissionCalc`), `TransFit`(ICI)| -|
| trans_opt| not clear yet | not clear yet | not clear yet|
|transFitOnOff_can| same as sample| same as sample| -|
| transFit_ck_can| same as sample| same as sample| -|
| trans_min_can| same as sample| same as sample| -|
| trans_max_can| same as sample| same as sample| -|
| trans_opt_can| same as sample| same as sample| -|

For efficacy correction:

| Gui Name                | Variable in back-end  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| direct_file             | `correction_file`(`DetectorBank`)| direct | read only|
| direct_file_front             | `correction_file`(`DetectorBank`)| direct | read only|

For flood file:

| Gui Name                | Variable in back-end  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| enableRearFlood_ck      | indirectly "pixel" fieles in `CalculateNormISIS` | `SetDetectorFloodFile`(ICI), `getPixelCorrFile`(`CalculateNormISIS`)| -|
| floodRearFile |"pixel" fieles in `CalculateNormISIS` | `SetDetectorFloodFile`(ICI), `getPixelCorrFile`(`CalculateNormISIS`)| -|
| enableFrontFlood_ck      | indirectly "pixel" fieles in `CalculateNormISIS` | `SetDetectorFloodFile`(ICI), `getPixelCorrFile`(`CalculateNormISIS`)| -|
| floodFrontFile |"pixel" fieles in `CalculateNormISIS` | `SetDetectorFloodFile`(ICI), `getPixelCorrFile`(`CalculateNormISIS`)| -|

For Q Resolution:

| Gui Name                | Variable in back-end  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| q_resolution_group_box |  `use_q_resolution`(`ConvertToQISIS`) | `get_q_resolution_use`(ICI), `set_q_resolution_use`(ICI)| -|
| q_resolution_combo_box |  internal | internal| -|
| q_resolution_a1_input |  `_q_resolution_a1`(`ConvertToQISIS`) | `set_q_resolution_a1`(ICI), `get_q_resolution_a1`(ICI)|-|
| q_resolution_a2_input | equivalent to a1 | equivalent to a1 |-|
| q_resolution_h1_input | equivalent to a1 | equivalent to a1 |-|
| q_resolution_h2_input | equivalent to a1 | equivalent to a1 |-|
| q_resolution_w1_input | equivalent to a1 | equivalent to a1 |-|
| q_resolution_w2_input | equivalent to a1 | equivalent to a1 |-|
| q_resolution_collimation_length_input | equivalent to a1 | equivalent to a1 |-|
| q_resolution_delta_r_input | equivalent to a1 | equivalent to a1 |-|
| q_resolution_moderator_input | equivalent to a1 | equivalent to a1 |-|

For Incident Monitors:

| Gui Name                | Variable in back-end  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| monitor_spec      |   `_incident_monitor`(`instrument`)         | `get_incident_mon`(`instrument`), `SpetMonitorSpectrum`(ICI)| -|
| monitor_interp | `use_interpol_norm`(`instrument`)| `is_interpolatin_norm`(`instrument`), `SpetMonitorSpectrum`(ICI)|
| trans_monitor    | `incid_mon_4_trans_calc`(`instrument`)|direct, `SetTransSpectrum`(ICI)|-|
| trans_interp| `interpolate`(`TransmissionCalc`) | direct, `SetTransSpectrum`(ICI)|-|


For Transmission Settings:

| Gui Name                | Variable in back-end  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| trans_M3_checkbox       |  `trans_mon`(`TransmissionCalc`)   | `SetTransmissionMonitorSpectrum`(ICI), `GetTransmissionMonitorSpectrum`(ICI), `UnsetTransmissionMonitorSpectrum`(ICI)| -|
| trans_M4_checkbox       |  `trans_mon`(`TransmissionCalc`)   | `SetTransmissionMonitorSpectrum`(ICI), `GetTransmissionMonitorSpectrum`(ICI), `UnsetTransmissionMonitorSpectrum`(ICI)| -|
| trans_M3M4_line_edit    | `monitor_4_offset`(`instrument`)  | `SetTransmissionMonitorSpectrumShift`(ICI), `GetTransmissionMonitorSpectrumShift`(ICI)|-|
| trans_radius_check_box   | internal | internal |-|
| trans_radius_line_edit  | `radius`(`TransmissionCalc`)|`GetTransmissionRadiusInMM`(ICI), `SetTransmissionRadiusInMM`(ICI)|-|
| trans_roi_files_checkbox | internal | internal | -|
|trans_roi_files_line_edit | `roi_files`(`TransmissionCalc`)| `SetTransmissionROI`(ICI), GetTransmissionROI(ICI) | -|
| trans_masking_line_edit | `mask_files`(`TransmissionCalc`)|  `SetTransmissionMask`(ICI), `GetTransmissionMask`(ICI)| -|



For Detector Selection:

| Gui Name                | Variable in back-end  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| detbank_sel             |  `det_selection`(`instrument`) | direct, `setDetector`(`instrument`), `CompWavRanges`(ICI), `WavRangeReduction`(ICI), beam centre finder procedure, during saving| seems to be very spread out in the GUI|
| phi_min | `phi_min`(`Mask_ISIS`) | direct, `SetPhiLimit`(ICI)| -|
| phi_max | `phi_max`(`Mask_ISIS`) | direct, `SetPhiLimit`(ICI)| -|
| mirror_phi| `phi_mirror`(`Mask_ISIS`)     | direct,  `SetPhiLimit`(ICI)| -|
| frontDetRescale | `scale`(`DetectorBank`) in Single Mode, `fit_settings` in Batch Mode  | direc, `TransFit`(ICI)|-|
| fronDetRescaleCB | internal | internal |-|
| frontDetShift | `shift`(`DetectorBank`) in Single Mode, `fit_settings` in Batch Mode  | direct, `TransFit`(ICI)|-|
| fronDetShiftCB | internal | internal |-|
| frontDetQmin | `qMin`(`DetectorBank`) in Single Mode, `fit_settings` in Batch Mode  | direct, `TransFit`(ICI)|-|
| frontDetQmax | `qMax`(`DetectorBank`) in Single Mode, `fit_settings` in Batch Mode  | direct, `TransFit`(ICI)|-|
| frontDetQRangeOnOFf | `qRangeUserSelected`(`DetectorBank`) | direct|-|


For Data Range:

| Gui Name                | Variable in back-end  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| tof_min | while loading reads from workspace | -| read only|
| tof_max | while loading reads from workspace | -| read only|
| scale_factor| `rescale`(`AbsoluteUnitsISIS`)|,  direct | -|

For Sample Details:

| Gui Name                | Variable in back-end  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| sample_geomid | `shape`(`GetSampleGeom`) | direct |-|
| sample_height | `height`(`GetSampleGeom`) | direct |-|
| sample_width | `width`(`GetSampleGeom`) | direct |-|
| sample_thick | `thickness`(`GetSampleGeom`) | direct |-|
| smpl_offset | `SAMPLE_Z_CORR`(`ISISInstrument`) | `SetSampleOffset`(ICI)|-|

For Beam Centre:

Look at only these elements which directly affect the redcution.

| Gui Name                | Variable in back-end  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| rear_beam_x             | `_beam_center_x`(`BaseBeamFinder`)  | `SetCentre`(ICI), `get_beam_center`(reducer)| -|
| rear_beam_y             | `_beam_center_y`(`BaseBeamFinder`)  | `SetCentre`(ICI), `get_beam_center`(reducer)| -|
| front_beam_x             | `_beam_center_x`(`BaseBeamFinder`)  | `SetCentre`(ICI), `get_beam_center`(reducer)| -|
| front_beam_y             | `_beam_center_y`(`BaseBeamFinder`)  | `SetCentre`(ICI), `get_beam_center`(reducer)| -|


For Front Tab:

| Gui Name                | Variable in back-end  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| sliceEvent   | `_slices_def`(reducer)   | `SetEventSlices`(ICI) |-|
