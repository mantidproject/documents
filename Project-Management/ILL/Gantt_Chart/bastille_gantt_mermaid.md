gantt
dateFormat  YYYY-MM-DD
title Bastille Project - Phase 1

section Release Cycle
Mantid 3.6				: 2016-02-05, 2016-06-05
Mantid 3.7				: 2016-06-06, 2016-10-16
Mantid 3.8				: 2016-10-17, 2017-02-12
Mantid 3.9				: 2017-02-13, 16w

section .
Startup Activities (all)		: done, start1, 2016-05-05, 2016-05-20

section Scanning Instruments (IB)
Define requirements and design		: scan1, 2016-06-16, 8w
Implementation in Mantid framework	: scan2, after scan1, 10w
Verification				: scan3, after scan2, 6w
Loader for D2b				: scan4, after scan3, 8w
Loader for D4				: scan5, after scan4, 8w
Loader for D7				: scan6, after scan5, 4w

section ToF Spectoscopy (AS & IB)
Evaluate LAMP and Mantid		: active, tof1, 2016-05-23, 6w
Determine new requirements		: tof2, after tof1, 4w
Implementation of new featuers		: tof3, after tof2, 5w
Validation of results			: tof4, after tof3, 4w
GUI Interface				: tof5, after tof4, 5w

section Powder Diffraction (AS)
Evaluate LAMP and Mantid		: pow1, 2016-11-07, 6w
Determine new requirements		: pow2, after pow1, 4w
Implementation of new featuers		: pow3, after pow2, 5w
Validation of results			: pow4, after pow3, 5w
GUI Interface				: pow5, after pow4, 5w

section Liquid Diffraction (AS)
TBD					: liq, 2017-05-01, 2017-11-26

section Inverted Geometry (AS)
TBD					: invg, 2017-11-27, 13w

section Strain Scattering (AS)
TBD					: strain, 2018-02-27, 2018-05-27

section Backscattering (VR & GV)
Evaluate LAMP and Mantid		: active, bs1, 2016-05-23, 2w
Determine new requirements		: bs2, after bs1, 1w
Implementation of new featuers		: bs3, after bs2, 3w
Validation of results			: bs4, after bs3, 4w
GUI Interface				: bs5, after bs4, 3w

section SANS (GV)
Evaluate LAMP and Mantid		: sans1, 2016-08-22, 7w
Determine new requirements		: sans2, after sans1, 5w
Implementation of new featuers		: sans3, after sans2, 6w
Validation of results			: sans4, after sans3, 6w
GUI Interface				: sans5, after sans4, 10w
SANS event mode				: sans6, after sans5, 16w

section Diffuse Scattering (GV)
TBD					: diffuse, 2017-08-07, 26w

section ToF Spectroscopy Event Mode (GV)
TBD					: tofe, 2018-02-05, 2018-09-30

section Tof Reflectometry (VR)
Evaluate LAMP and Mantid		: tofref1, 2016-08-22, 5w
Determine new requirements		: tofref2, after tofref1, 3w
Implementation of new featuers		: tofref3, after tofref2, 4w
Validation of results			: tofref4, after tofref3, 4w
Reflectometry UI			: tofref5, after tofref4, 8w

section Monochromatic Reflectometry (VR)
Evaluate LAMP and Mantid		: monref1, 2017-02-06, 5w
Determine new requirements		: monref2, after monref1, 3w
Implementation of new featuers		: monref3, after monref2, 4w
Validation of results			: monref4, after monref3, 4w
Reflectometry UI			: monref5, after monref4, 8w

section Live Data Analysis server (VR)
Investigate Nomad			: live1, 2017-07-24, 4w
Evaluate systems at SNS and ISIS 	: live2, after live1, 4w
Live Data Design			: live3, after live2, 4w
Live Data Implementation		: live4, after live3, 20w
Live Data Validation			: live5, after live4, 8w

section NXSTools (EP)
NXStools - 1				: nxs1, 2016-05-02, 2016-12-09
NXSTools - 2				: nxs2, 2017-05-01, 2017-12-08
NXSTools - 3				: nxs3, 2018-05-01, 2018-12-10

