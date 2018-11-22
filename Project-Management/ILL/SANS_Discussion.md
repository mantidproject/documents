## Default Q binning

* Q binning can be specified by the user, but what is the preferred default? And for TOF?

* Fraction of the resolution given by the user. Largest size of the pixel.

## Parallax correction (gondola effect) and detector efficiencies

* How to properly decouple the flight-path (2theta) dependence from actual efficiency through attenuation?

* Different empirical formula for D33 (y dependent) - Ask Charles

* D11 absorption in the aluminium

* Relative efficiencies for D33 front detector

* cross-check solid angle with tube detector

* parallax correction for D33

* [TOF] What about wavelength dependence of attenuation? - This is ignored, assuming constant.

## Beam stop masking

* This can be done graphically, but one can automatize by either finding the shadow on the detector, or using the shape and the position of the beam stop.

* Automatic masking is not reliable 

## Resolution

* Mildner-Carpenter? What about TOF resolution? - this is approximation (often enough)

* Kernel convolution - R based 

## [TOF] Wavelength axis

* Wavelength axes are adjusted for each pixel individually based on L2 distance. - good, but not much of improvement

## Dead time correction

* How to model flux and wavelength dependence? - Wavelenght dependence is ignored.

* small correction nowadays, D11 global correction, D22 & D33 tube based as a function of countrate (ask Charles)

## Stitching

* Which kind of stitching is desired? Is stitched data used only for visualisation, or actually in the analysis?

* some option for visualisation only (with filters on errors and resolution)

* stitched data should not be used in the analysis

## Beam center (gravity)

* Currently center of mass of the direct beam is calculated, then the detector is moved in vertical axis such that the beam center is at y=0. Is this a good approximation? - Yes.

* [TOF] Beam center can be calculated for each wavelength bin. Cannot move the detector, but can move the counts correspondingly.

* Is this a good approximation? Would analytical correction for gravity (essentially y+=gtˆ2/2) be applicable?

For L2=5 m, TOF=70 msec, gravity drop ~ 25 mm, so about 5 pixels.

* beam center per wavelength - good approximation, just pity of losing some data from the upmost stripes

## Actions

* Empirical formula for parallax corrections for D33 

* Dead time corrections for D11, D22, D33

* Beam center per wavelength for D33 TOF

* Error and resolution aware mixing in I(Q) in TOF mode

* Resolution by convoluted numerical kernels
