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

The key parts of the proposal are as follows:

* [Definition of interface to input sample properties](#S-sample-properties)
* [Definition of interface to input sample holder properties](#S-sample-holder-properties)
* [Definition of interface to run the calculational algorithm](#S-calculational-algorithm)
* [Definition of backend to store known sample holder geometry/properties](#S-backend-sample-holder)

### <a name="S-sample-properties"></a> Definition of Interface for Input of Sample Properties

**Idea 1**: Separate algorithms for setting sample geometry/material.

```python
w1 = SetSampleGeometry(w1, Type="Cylinder",
                       TypeArgs={"Radius": 40, "Height": 2.5})
w1 = SetSampleMaterial(w1, ChemicalFormula="V", SampleNumberDensity=0.072)
```

**Idea 2**: Single algorithm for setting both.

```python
# Simple cylindrical sample, no can
# Material dictionary would accept the same arguments as current SetSampleMaterial
w1 = SetSample(w1, Geometry={"Shape": "Cylinder", "Radius": 40, "Height": 2.5}
    Material={"Formula": "V", "SampleNumberDensity"=0.072})
w1_abs = CalculateSampleCorrection(w1, Method="MonteCarlo",
    MethodArgs={"NLambda": 500, "NEvents": 300})
```

More complex shapes would have to be defined through [CSG](http://docs.mantidproject.org/nightly/concepts/HowToDefineGeometricShape.html#howtodefinegeometricshape) algebra in both approaches, e.g.

```python
sphere = '''
<sphere id="sphere1">
  <centre x="0" y="0" z="0"/>
  <radius val="0.1" />
</sphere>'''
w1 = SetSample(w1, Geometry={"Shape": "CSG", "Value": sphere},
    Material={"Formula": "V", "SampleNumberDensity"=0.072})
```

### <a name="S-sample-holder-properties"></a> Definition of interface to input sample holder properties

Assuming we have a way of defining a [repository of known sample holders](#S-backend-sample-holder) the user could just select from them by name:

```python
# given sample holder from instrument
w1 = SetSampleHolder(w1, Name="POLARIS-Can-6mm")
w1_abs = CalculateSampleCorrection(w1, Method="MonteCarlo",
    MethodArgs={"NLambda": 500, "NEvents": 300})
```

The properties, geometry & material, would be assumed to be defined elsewhere. They could however also be specified in a similar manner to the
sample properties:

```python
# given sample holder from instrument
w1 = SetSampleHolder(w1, Geometry={"Shape": "Annulus", "InnerRadius": 35, "OuterRadius": 40, "Height": 2.5},
    Material={"Formula": "V", "SampleNumberDensity"=0.072})
w1_abs = CalculateSampleCorrection(w1, Method="MonteCarlo",
    MethodArgs={"NLambda": 500, "NEvents": 300})
```


### <a name="S-calculation-algorithm"></a> Definition of interface to run the calculational algorithm

The main calculation will take place in the existing [`MonteCarloAbsorption`](http://docs.mantidproject.org/nightly/algorithms/MonteCarloAbsorption-v1.html), algorithm
which is currently able to cope with sample/can environments. Upgrades required:

* support for inelastic data

Users will be given a new algorithm called `CalculateSampleCorrection` that will form the interface to running different correction algorithms. These algorithms will assume
that the metadata required, such as geometry and material properties is all completely defined on the workspace. An example of running the algorithm would be:

```python
w1 = ConvertUnits(w1, Target="Wavelength")
w1_abs = CalculateSampleCorrection(w1, Method="MonteCarlo",
    MethodArgs={"NLambda": 500, "NEvents": 300})
```

### <a name="S-backend-sample-holder"></a> Definition of backend to store known sample holder geometry/properties

TODO
