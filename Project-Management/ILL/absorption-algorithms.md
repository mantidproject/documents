# Self-shielding correction algorithms in Mantid

This is merely a listing of the different algorithms available in Mantid for direct and indirect geometry spectrometers. For more information, see the algorithm documentation and references therein.

## Generic sample shapes

### [`AbsorptionCorrection`](http://docs.mantidproject.org/nightly/algorithms/AbsorptionCorrection-v1.html)

  + Calculates attenuation factors resulting from absorption and single scattering.
  + Uses numerical integration.
  + For generic sample shapes.
    - For the usual sample geometries, such as slab, using a specific algorithm is recommended.
  + A *gauge volume* can be defined (by [`DefineGaugeVolume`](http://docs.mantidproject.org/nightly/algorithms/DefineGaugeVolume-v1.html#algm-definegaugevolume) or [`CuboidGaugeVolumeAbsorption`](http://docs.mantidproject.org/nightly/algorithms/CuboidGaugeVolumeAbsorption-v1.html#algm-cuboidgaugevolumeabsorption)) algorithms if the neutron beam does not illuminate the entire sample.
  + Input workspace must have units of wavelength.

### [`MonteCarloAbsorption`](http://docs.mantidproject.org/nightly/algorithms/MonteCarloAbsorption-v1.html#algm-montecarloabsorption)

  + Calculates attenuation factors resulting from absorption and single scattering.
  + Uses Monte Carlo simulation.
  + For generic sample shapes.
  + Beam shape and size can be defined.
  + Input workspace must have units of wavelenght.

## Slab geometry

## [`FlatPlateAbsorption`](http://docs.mantidproject.org/nightly/algorithms/FlatPlateAbsorption-v1.html#algm-flatplateabsorption)

  + Calculates attenuation factors resulting from absorption and single scattering.
  + Uses numerical integration.
  + For slab geometry.
  + Input workspace must have units of wavelength.
  + A special version [`HRPDSlabCanAbsorption`](http://docs.mantidproject.org/nightly/algorithms/HRPDSlabCanAbsorption-v1.html#algm-hrpdslabcanabsorption) is available for HRPD sample holders. Takes into account the sample holder itself.

### [`FlatPlatePaalmanPingsCorrection`](http://docs.mantidproject.org/nightly/algorithms/FlatPlatePaalmanPingsCorrection-v1.html)

  + Calculates absorption corrections using the Paalman & Pings format.
  + For slab geometry.

## Cylinder geometry

### [`CylinderAbsorption`](http://docs.mantidproject.org/nightly/algorithms/CylinderAbsorption-v1.html)

  + Calculates attenuation factors resulting from absorption and single scattering.
  + Uses numerical integration.
  + For cylinder geometry.
    - Does not support annular shapes, that is, hollow cylinders.
  + Input workspace must have units of wavelength.

### [`CylinderPaalmanPingsCorrection`](http://docs.mantidproject.org/nightly/algorithms/CylinderPaalmanPingsCorrection-v2.html)

  + Calculates absorption corrections using the Paalman & Pings format.
  + For cylinder and annulus geometry.

### [`MultipleScatteringCylinderAbsorption`](http://docs.mantidproject.org/nightly/algorithms/MultipleScatteringCylinderAbsorption-v1.html)

  + Multiple scattering absorption correction.
  + See the documentation for references on how the calculation is done.
  + Originally used to correct the vanadium spectrum for the GPPD instrument at IPNS.

### [`MayersSampleCorrection`](http://docs.mantidproject.org/nightly/algorithms/MayersSampleCorrection-v1.html)

  + Calculates absorption corrections and optionally multiple scattering.
  + Uses numeric integration.
  + For cylinder geometry.

## Spherical geometry

### [`AnvredCorrection`](http://docs.mantidproject.org/nightly/algorithms/AnvredCorrection-v1.html#algm-anvredcorrection)

  + Calculates anvred correction factors resulting from absorption and scattering.
  + For spherical geometry.

### [`SphericalAbsorption`](http://docs.mantidproject.org/nightly/algorithms/SphericalAbsorption-v1.html)

  + Calculates attenuation factors due to absorption and single scattering.
  + Uses the `AnvredCorrection` algorithm mentioned previously.
  + For sphere geometry.

## Indirect geometry instruments

### [`IndirectFlatPlateAbsorption`](http://docs.mantidproject.org/nightly/algorithms/IndirectFlatPlateAbsorption-v1.html)

  + Calculates absorption corrections using the Paalman & Pings format.
  + For slab geometry.

### [`IndirectCylinderAbsorption`](http://docs.mantidproject.org/nightly/algorithms/IndirectCylinderAbsorption-v1.html)

  + Calculates absorption corrections using the Paalman & Pings format.
  + For cylinder geometry.

### [`IndirectAnnulusAbsorption`](http://docs.mantidproject.org/nightly/algorithms/IndirectAnnulusAbsorption-v1.html)

  + Calculates absorption corrections using the Paalman & Pings format.
  + For annulus geometry.

## Others

### [`ApplyPaalmanPingsCorrection`](http://docs.mantidproject.org/nightly/algorithms/ApplyPaalmanPingsCorrection-v1.html)

  + Used to apply corrections in the Paalman & Pings format.
