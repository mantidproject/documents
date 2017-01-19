### Self-shielding correction algorithms in Mantid

This is merely a listing of the different algorithms available in Mantid for direct and indirect geometry spectrometers. For more information, see the algorithm documentation and references therein.

### Summary

+ All of the algorithms expect a reduced sample workspace and separately the empty can workspace, when applicable.

+ Workspaces must have wavelength as x-axis unit, and raw spectrum number as y-axis. Some of the algorithms are able to automatically convert the x-axis to wavelength. But for consistency, it is probably better to accept wavelength as standard.

+ All of the algorithms, except the MonteCarloAbsorption, use numerical integration, the latter uses Monte Carlo integration.

+ When the sample has a simple geometry, it is recommended to use the corresponding algorithm directly, if possible.

+ None of the algorithms, except MultipleScatteringCylinderAbsorption and MayersSampleCorrection, take multiple scattering into account.

+ These are corrections that are applied in offline analysis, and some of them are time-consuming to compute. Moreover they require a lot of input parameters. Hence, these probably should not be calculated on-the-fly from the reduction algorithms. Instead one should produce the reduced sample (and empty can) workspaces separately, and then corrections can be computed and applied aposteriori. (This is at least what ISIS indirect does) 

+ ISIS indirect has Indirect->Corrections GUI, with 4 tabs:
  - Can subtraction (simple subtraction without corrections)
  - Calculate Paalman&Pings
  - Apply Paalman&Pings
  - Absorption

### Generic sample shapes

+ A *gauge volume* can be defined (by [`DefineGaugeVolume`](http://docs.mantidproject.org/nightly/algorithms/DefineGaugeVolume-v1.html#algm-definegaugevolume) or [`CuboidGaugeVolumeAbsorption`](http://docs.mantidproject.org/nightly/algorithms/CuboidGaugeVolumeAbsorption-v1.html#algm-cuboidgaugevolumeabsorption)) algorithms if the neutron beam does not illuminate the entire sample.

## [`AbsorptionCorrection`](http://docs.mantidproject.org/nightly/algorithms/AbsorptionCorrection-v1.html)

## [`MonteCarloAbsorption`](http://docs.mantidproject.org/nightly/algorithms/MonteCarloAbsorption-v1.html#algm-montecarloabsorption)

  + Does not take multiple scattering into account.
  + Does not give errors on the corrections.
  + Requires input workspace to have wavelength as x-axis unit.
  + Has 3 modes:
    - Elastic : lambdaIn = lambdaOut = lambdaStep
    - InDirect: lambdaIn = lambdaStep, lambdaOut = lambdaFixed
    - Direct  : lambdaIn = lambdaFixed, lambdaOut = lambdaStep
    - Do we need new EFixed mode ? lambdaIn = lambdaOut = lambdaFixed

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
