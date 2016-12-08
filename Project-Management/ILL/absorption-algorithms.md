### Self-shielding correction algorithms in Mantid

This is merely a listing of the different algorithms available in Mantid for direct and indirect geometry spectrometers. For more information, see the algorithm documentation and references therein.

### Generic sample shapes

## [`AbsorptionCorrection`](http://docs.mantidproject.org/nightly/algorithms/AbsorptionCorrection-v1.html)

  + Calculates attenuation factors resulting from absorption and single scattering.
  + Uses numerical integration.
  + For generic sample shapes.
    - For the usual sample geometries, such as slab, using a specific algorithm is recommended.
  + A *gauge volume* can be defined (by [`DefineGaugeVolume`](http://docs.mantidproject.org/nightly/algorithms/DefineGaugeVolume-v1.html#algm-definegaugevolume) or [`CuboidGaugeVolumeAbsorption`](http://docs.mantidproject.org/nightly/algorithms/CuboidGaugeVolumeAbsorption-v1.html#algm-cuboidgaugevolumeabsorption)) algorithms if the neutron beam does not illuminate the entire sample.

## [`MonteCarloAbsorption`](http://docs.mantidproject.org/nightly/algorithms/MonteCarloAbsorption-v1.html#algm-montecarloabsorption)

  + Calculates self-attenuation factors resulting from absorption and single scattering.
  + Uses Monte Carlo simulation.
  + For generic sample shapes.
  + Beam shape and size can be defined.

### Slab geometry

## [`FlatPlateAbsorption`](http://docs.mantidproject.org/nightly/algorithms/FlatPlateAbsorption-v1.html#algm-flatplateabsorption)

## [`HRPDSlabCanAbsorption`](http://docs.mantidproject.org/nightly/algorithms/HRPDSlabCanAbsorption-v1.html#algm-hrpdslabcanabsorption)

  + Takes into account the HRPD sample holder as well.

## [`IndirectFlatPlateAbsorption`](http://docs.mantidproject.org/nightly/algorithms/IndirectFlatPlateAbsorption-v1.html)

## [`FlatPlatePaalmanPingsCorrection`](http://docs.mantidproject.org/nightly/algorithms/FlatPlatePaalmanPingsCorrection-v1.html)

### Cylinder geometry

## [`CylinderAbsorption`](http://docs.mantidproject.org/nightly/algorithms/CylinderAbsorption-v1.html)

  + Does not support annular shapes, that is, hollow cylinders.
  
## [`MultipleScatteringCylinderAbsorption`](http://docs.mantidproject.org/nightly/algorithms/MultipleScatteringCylinderAbsorption-v1.html)

  + Multiple scattering absorption correction.
  + See the documentation for references on how the calculation is done.
  + Originally used to correct the vanadium spectrum for the GPPD instrument at IPNS.
  
## [`IndirectCylinderAbsorption`](http://docs.mantidproject.org/nightly/algorithms/IndirectCylinderAbsorption-v1.html)

## [`IndirectAnnulusAbsorption`](http://docs.mantidproject.org/nightly/algorithms/IndirectAnnulusAbsorption-v1.html)

## [`CylinderPaalmanPingsCorrection`](http://docs.mantidproject.org/nightly/algorithms/CylinderPaalmanPingsCorrection-v2.html)

  + For cylinder and annulus geometry.

## [`MayersSampleCorrection`](http://docs.mantidproject.org/nightly/algorithms/MayersSampleCorrection-v1.html)

  + Calculates absorption corrections and optionally multiple scattering.

### Spherical geometry

## [`AnvredCorrection`](http://docs.mantidproject.org/nightly/algorithms/AnvredCorrection-v1.html#algm-anvredcorrection)

## [`SphericalAbsorption`](http://docs.mantidproject.org/nightly/algorithms/SphericalAbsorption-v1.html)

  + Uses the `AnvredCorrection` algorithm mentioned previously.

### To apply PaalmanPings Corrections

## [`ApplyPaalmanPingsCorrection`](http://docs.mantidproject.org/nightly/algorithms/ApplyPaalmanPingsCorrection-v1.html)
