# Absorption Corrections for a General Shape


## Motivation

Mantid currently contains many different types of algorithm to correct for absorption. It is desired to have a consistent
approach to correcting for absorption within the sample/can.

## Requirements

### Must Haves

1. Able to define a list of available sample holders per instrument
1. A simple but extensible method for setting the geometry of the container (sample environment), including selection from the above list
1. A simple but extensible method for setting the geometry of the sample
1. A method to set the cross-section properties of the sample
1. A method to set the cross-section properties of the container
1. Be able to handle elastic/inelastic scattering
1. Sample should be able to be offset from centre
1. Separate algorithms to calculate the correction and then apply them, re Paalman & Pings

## Selected Use cases

Add a selection of use cases

## Current Structure

There are currently 16 algorithms that relate to different methods for calculating the absorption corrections:

* AbsorptionCorrection
* AnnularRingAbsorption
* AnvredCorrection
* CuboidGaugeVolumeAbsorption
* CylinderAbsorption
* CylinderPaalmanPingsCorrection
* FlatPlateAbsorption
* FlatPlatePaalmanPingsCorrection
* HRPDSlabCanAbsorption
* IndirectAnnulusAbsorption
* IndirectCylinderAbsorption
* IndirectFlatPlateAbsorption
* MayersSampleCorrection
* MonteCarloAbsorption
* PearlMCAbsorption
* SphericalAbsorption

Most are numerical methods defined for some specific shape. The `MonteCarloAbsorption` algorithm in theory has all of the required parts to allow
the absorption to be computed but it currently only works for elastic data. Also, the can environment must be defined in C++.

## Proposed Solution

The proposed solution is centered on using the Monte Carlo approach to provide the calculational engine for the corrections. This will allow it to
work for any shape. The complexity involved mostly surrounds the interface required for a user to enter the details regarding the sample & environment.

## Solution Details


### Example Script


#### Cylinder sample, no can

```python
# Units in wavelength
w1 = ConvertUnits(w1, Target="Wavelength")
w1 = SetSampleGeometry(w1, Shape="Cylinder",
                       ShapeParameters={"Radius": 40, "Height": 2.5})
w1 = SetSampleMaterial(w1, ChemicalFormula="V")

w1_abs = CalculateSampleCorrection(w1, Method="MonteCarlo",
                                   MethodArgs={"NLambda": 500, "NEvents": 300})
```
