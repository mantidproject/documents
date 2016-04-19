Monte Carlo Absorption & Single Scattering Correction Procedure
---------------------------------------------------------------

This document describes the intended procedure for calculating the correction factors due
to attenuation & single scattering within a sample plus its sample environment.

The algorithm will compute the correction factors on a bin-by-bin basis for each spectrum within
the input workspace. The following assumptions on the input workspace will be made:

* X units are in wavelength
* the instrument is fully defined
* a shape & material for the sample has been defined
* the \'size\' of the beam has been defined. Currently assumed to be a width & height with no divergence
* a series of shapes & materials for the can + other sample environment components is defined  (optional)

The additional inputs to the algorithm are:

* `NumberOfWavelengthPoints` - the number of wavelength points per spectrum for which to calculate the correction factor. An interpolation
                             will fill in the missing values
* `NEvents` - the number of monte carlo "events" to generate for each simulated wavelength point

The algorithm will proceed as follows. For each spectrum:

1. find the associated detector position
1. find the associated efixed value (if applicable) & convert to wavelength (lambdaFixed)
1. loop over the bins in steps defined by `NumberOfWavelengthPoints` and for each step (`lambdaStep`)
    * define `lambdaIn` as the wavelength before scattering & `lambdaOut` as wavelength after scattering:
      - Direct: `lambdaIn` = `lambdaFixed`, `lambdaOut` = `lambdaStep`
      - Indirect: `lambdaIn` = `lambdaStep`, `lambdaOut` = `lambdaFixed`
      - Elastic: `lambdaIn` = `lambdaOut` = `lambdaStep`
    * for each event in `NEvents`:
      - generate a random point on the beam face define by the input height & width
	  - assume the neutron travels in the direction defined by the `samplePos - srcPos` and define a `Track`
	  - test for intersections of the track & sample object, giving the number of subsections (for example 2 in an annulus)
	    and corresponding distances within the sample for each section
      - choose a random section and depth for the scatter point
