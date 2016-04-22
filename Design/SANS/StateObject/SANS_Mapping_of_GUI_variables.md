# Mapping of the GUI variables

## Abreviations

The following abreviations will be used below:
* `ISISCammondInterface` : ICI
* in-place: i-p
* Graphical User Interface. Essentially the `C++` part: GUI

## Purpose
This document tries to scope the level of connectedness of the GUI with the
reducer backend. The initial design of the ISIS SANS redcution interface (and backend)
was to have a single communication layer which should be provided by the ICI. Currently
there is tight coupling between the GUI and the backend. This will be scoped out here.




For gravity:

| Gui Name                | Variable in Backend  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| `gravity_check`         |  `use_gravity`(`ConvertToQISIS`) | `get_gravity`(`ConvertToQISIS`), `Gravity`(ICI)| -|
| `gravity_extra_length_line_edit` | `_use_gravity`(`ConvertToQISIS`) | `get_extra_length`(`ConvertToQISIS`), `Gravity`(ICI)| -|

For limits:

| Gui Name                | Variable in Backend  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| rad_min | `min_radius`(`Mask_ISIS`) | direct, `readLimitValues`(`UserFile`)| -|
| rad_max | `max_radius`(`Mask_ISIS`) | direct, `readLimitValues`(`UserFile`)| -|
| wav_min | `wav_low`(`ConvertUnits`) | direct, `LimitsWav`(ICI)| -|
| wav_max | `wav_high`(`ConvertUnits`) | direct, `LimitsWav`(ICI)| -|
| wav_dw  | `wav_step`(`ConvertUnits`) | direct, `LimitsWav`(ICI)| -|
| wav_dw_opt | TODO | - | not clear yet|
| q_min | `binning`(`ConvertToQISIS`)| direct, `readLimitValues`(`UserFile`) | `binning` is a comma separated string of variables |
| q_max | `binning`(`ConvertToQISIS`)| direct, `readLimitValues`(`UserFile`) | `binning` is a comma separated string of variables |
| q_dq  | `binning`(`ConvertToQISIS`)| direct, `readLimitValues`(`UserFile`) | `binning` is a comma separated string of variables |
| q_dq_opt | TODO | TOD0| TODO|
| qy_max | `QXY2`(reducer) | direct, `LimitsQXY`(ICI)| the min seems to always start from 0|
| qy_dqy | `DQXY`(reducer) | direct, `LimitsQXY`(ICI)| -|
| qy_dqy_opt | TODO | TOD0| TODO|
| trans_selector_opt| `fit_settings`(`TransmissionCalc`)| `isSeparate`(`TransmissionCalc`) + ?| -|
| transFitOnOff| `fit_settings`(`TransmissionCalc`)| `TransFit`(ICI), `fitMethod`(`TransmissionCalc`)| -|
| transFit_ck| ?| ?| -|
| trans_min| `fit_settings`(`TransmissionCalc`) | lamdaMin(`TransmissionCalc`), `TransFit`(ICI)| -|
| trans_max| `fit_settings`(`TransmissionCalc`)| lamdaMax(`TransmissionCalc`), `TransFit`(ICI)| -|
| trans_opt| TODO | TODO | -|
|transFitOnOff_can| same as sample| same as sample| -|
| transFit_ck_can| same as sample| same as sample| -|
| trans_min_can| same as sample| same as sample| -|
| trans_max_can| same as sample| same as sample| -|
| trans_opt_can| same as sample| same as sample| -|

For efficacy correction:

| Gui Name                | Variable in Backend  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| direct_file             | `correction_file`(`DetectorBank`)| direct | read only|
| direct_file_front             | `correction_file`(`DetectorBank`)| direct | read only|

For flood file:

| Gui Name                | Variable in Backend  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| enableRearFlood_ck      | indirectly "pixel" fieles in `CalculateNormISIS` | `SetDetectorFloodFile`(ICI), `getPixelCorrFile`(`CalculateNormISIS`)| -|
| floodRearFile |"pixel" fieles in `CalculateNormISIS` | `SetDetectorFloodFile`(ICI), `getPixelCorrFile`(`CalculateNormISIS`)| -|
| enableFrontFlood_ck      | indirectly "pixel" fieles in `CalculateNormISIS` | `SetDetectorFloodFile`(ICI), `getPixelCorrFile`(`CalculateNormISIS`)| -|
| floodFrontFile |"pixel" fieles in `CalculateNormISIS` | `SetDetectorFloodFile`(ICI), `getPixelCorrFile`(`CalculateNormISIS`)| -|

For Q Resolution:

| Gui Name                | Variable in Backend  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|

TODO

For Incident Monitors:

| Gui Name                | Variable in Backend  |  Interacts  via | Comment |
|-------------------------|----------------------|-----------------|---------|
| monitor_spec      |               | `SpetMonitorSpectrum`(ICI),
