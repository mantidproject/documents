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

## Proposal

The proposed solution is centered on using the Monte Carlo approach to provide the calculation engine for the corrections. This will allow it to
work for any shape. The complexity involved mostly surrounds the interface required for a user to enter the details regarding the sample & environment.

## Solution Details

The key parts of the proposal are described in the following sections:

* [Running the calculation](#S-running-calculation)
* [Defining shapes & materials](#S-defining-shapes-and-materials)

* [Combining shape & material](#S-shape-material)
* [Definition of interface to input sample properties](#S-sample-properties)
* [Definition of interface to input sample holder properties](#S-sample-holder-properties)
* [Mechanism to store predefined sample holder geometries/properties](#S-predefined-sample-holder)

## <a name="S-running-calculation"></a> Running the calculation

The main calculation will take place in the existing [`MonteCarloAbsorption`](http://docs.mantidproject.org/nightly/algorithms/MonteCarloAbsorption-v1.html), algorithm
which is currently able to cope with sample/can environments. Upgrades required:

* support for inelastic data

Users will be given a new algorithm called `CalculateSampleCorrection` that will form the interface to running different correction algorithms. These algorithms will assume
that the metadata required, such as geometry and material properties is all completely defined on the workspace. An example of running the algorithm would be:

```python
# assume w1 has metadata already set
w1 = ConvertUnits(w1, Target="Wavelength")
w1_abs = CalculateSampleCorrection(w1, Method="MonteCarlo",
    MethodArgs={"NLambda": 500, "NEvents": 300})
```

The calculation of the correction and application of the correction will be kept separate so that

* the same correction can be applied to main data sets;
* the correction can be persisted to a file if necessary
* more complex procedures for applying the correction, such as Paalman & Pings, can be used.

##<a name="S-defining-shapes-and-materials"></a>Defining shapes & materials

The complex part of this is defining the syntax that users will need to specify the geometry & material for the sample + can setup. The cans available to
an experiment generally come from a list of known geometries. It is proposed that these geometries are defined in files
that can be distributed with Mantid and added to by users along a similar mechanism to the python extensions,
i.e. some user-defined set of locations to search for additional files.

To avoid having to invent a completely new syntax we can instead extend the current [XML-based syntax](http://docs.mantidproject.org/nightly/concepts/HowToDefineGeometricShape.html#howtodefinegeometricshape) 
to define the geometry. It will require new fields for:

* material definitions of each shape
* combining multiple components into a single environment.

The current list of "primitive" shapes can also be extended to cover frequently used cases, e.g. annulus.

The can definitions are split into 2 categories:

1. the can geometry constrains the sample geometry and simply fills a proportion of the fill volume, e.g. a powder/liquid in a cylinder
2. the can geometry does not constrain the sample geometry, e.g. a 'lumpy' sample where
  * its difficult to make a powder, if the material is too strong, or has some safety issue like radio toxicity
  * if the sample is a crystal. For isis spectrometers it's quite common to put the crystals on a mount in a can.

## <a name=""></a>Constrained sample geometry

[Example - 50mm Orange Cryostat with V tail (POWGEN)](https://neutrons.ornl.gov/sites/default/files/Powgen%20sample%20cans.pdf)

Liquid and powder samples will assume the geometry of the vessel that contains them. The definition of the can will define
the nominal sample geometry assuming the sample fills the whole space. The user-provided command would then allow 
for customization of unconstrained portions of the geometry:

**Filename: instrument/SNS/POWGEN/sample-environments/CRYO-004.xml**

```xml
<sample-environment>
  <materials>
    <material id="vanadium">
      <formula>V</formula>
    </material>
    <material id="inner-mat">
      <formula>XXX</formula>
    </material>
    <material id="outer-mat">
      <formula>XXX</formula>
    </material>
  </materials>

  <components>
    <cans>
     <can id="6mm" material="vanadium">
       <annulus id="an-1">
       <inner-radius val="0.0030"/>
       <outer-radius val="0.0031"/>
       <length val="0.05"/>
       <axis x="0.0" y="1.0" z="0.0"/>
       </annulus>
     </can>
     <can id="8mm" material="vanadium">
       <annulus id="an-1">
       <inner-radius val="0.0076"/>
       <outer-radius val="0.0080"/>
       <length val="0.05"/>
       <axis x="0.0" y="1.0" z="0.0"/>
       </annulus>
     </can>
     <can id="10mm" material="vanadium">
       <annulus id="an-1">
       <inner-radius val="0.0092"/>
       <outer-radius val="0.0100"/>
       <length val="0.05"/>
       <axis x="0.0" y="1.0" z="0.0"/>
       </annulus>
     </can>
     </cans>

    <sample-geometry>
      <cylinder>
      <centre-of-bottom-base x="0.0" y="0.0" z="0.0" />
      <axis x="0.0" y="1.0" z="0" />
      <radius link="can-inner-radius" />
      <height max="0.05" />
      </cylinder>
    </sample-geometry>
   
   <component id="inner-shield" material="inner-mat">
      <annulus id="an-2">
      <inner-radius val="0.006"/>
      <outer-radius val="0.0065"/>
      <length val="0.05"/>
      <axis x="0.0" y="1.0" z="0.0"/>
      </annulus>
   </component>

   <component id="outer-shield" material="outer-mat">
      <annulus id="an-3">
      <inner-radius val="0.007"/>
      <outer-radius val="0.0071"/>
      <length val="0.05"/>
      <axis x="0.0" y="1.0" z="0.0"/>
      </annulus>
   </component>
  </components>

</sample-environment>
```

An example usage in a script would be:

```python
SetSample(w1, Material={'ChemicalFormula': 'SomePowder'},
    Environment={'Name': 'CRYO-004', 'Can': '6mm'},
    SampleGeometry={'height': 0.025})
```
