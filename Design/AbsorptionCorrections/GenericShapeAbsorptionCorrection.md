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

* [Combining shape & material](#S-shape-material)
* [Definition of interface to input sample properties](#S-sample-properties)
* [Definition of interface to input sample holder properties](#S-sample-holder-properties)
* [Definition of interface to run the calculational algorithm](#S-calculational-algorithm)
* [Mechanism to store predefined sample holder geometries/properties](#S-predefined-sample-holder)

### <a name="S-shape-material"> Combining shape & material

To support composite objects it will be necessary to combine a shape with its composition. The material is already well captured by the
existing `Material` class and is it proposed that we keep this interface and expose it to Python. Shapes are currently defined via [CSG](http://docs.mantidproject.org/nightly/concepts/HowToDefineGeometricShape.html#howtodefinegeometricshape) but this is only exposed through the XML definition. It is proposed that the primitive shapes & operations are exposed to Python to allow complex geometries to be defined in scripts without resorting constructing
complex XML defintions.

The final fusion of shape & material will occur inside a `Volume` object that simply binds a CSG object with its corresponding material. Composite objects with many materials will then simply
be defined as a list of `Volume` objects. A set of examples of increasing complexity is given below.

*Vanadium Cylinder*

```python
from mantid import mm, Csg, Material
shape = Csg.Cylinder(Axis=[0,1,0], BaseCenter=[0,0,0], Radius=40*mm, Length=2.5*mm)
mat = Material(ChemicalFormula="V", NumberDensity=0.072)
van_cyl = Volume(shape, mat)
```

*Double-toroid, non-encapsulated (e.g. SNAP)*

```python
from mantid import mm, Csg, Material

def TopToroid()
    return csg.Translate(Csg.Difference(Csg.Sphere(Radius=2.5*mm, Center=[0,0,0.634]),
                                        Csg.Cuboid([5.1,5.1,4.38])), [0,0,-2.19])

van = Material(ChemicalFormula="V", NumberDensity=0.072)
top = TopToroid()
bottom = Csg.Rotate(TopToroid(), Angle=[180,0,0])
sample_volume = Volume(Csg.Union(top, bottom), Material=van)
```

### <a name="S-sample-properties"></a> Definition of Interface for Input of Sample Properties

The current algorithms [CreateSampleShape](http://docs.mantidproject.org/nightly/algorithms/CreateSampleShape-v1.html) & [SetSampleShape](http://docs.mantidproject.org/nightly/algorithms/SetSampleMaterial-v1.html) will
merge to form `SetSample` that accepts a list of `Volume` objects.

```python
from mantid import mm, Csg, Material
from mantid.simpleapi import SetSample

shape = Csg.Cylinder(Axis=[0,1,0], BaseCenter=[0,0,0], Radius=40*mm, Length=2.5*mm)
mat = Material(ChemicalFormula="V", NumberDensity=0.072)
van_cyl = Volume(shape, mat)
SetSample(w1, Volumes=[van_cyl])
```

**Question**: Do we need a "shortcut" syntax to be able to more easily configure common shapes, e.g. flat place, cylinder, annulus ?

### <a name="S-sample-holder-properties"></a> Definition of interface to input sample holder properties

In general these would be set by a new algorithm called `SetSampleHolder` that also accepts the same `Volumes` type argument as `SetSample` above. In addition this could be extended to accept an identifer that
would be used to pick up from a set of predefined sample holders defined in a set of files - see [below](#S-predefined-sample-holder) for more details.

**Question**: Do we need a "shortcut" syntax to be able to more easily configure common shapes, e.g. flat place, cylinder, annulus ?

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

### <a name="S-predefined-sample-holder"></a> Mechanism to store predefined sample holder geometries/properties

It is proposed that the information regarding predefined sample holder properties be defined in a series of files. This provides the easiest route to extension and customisation. They
will live alongside the IDF files. The simplest option is extend the current XML syntax for defining shapes to handle materials.

**Current XML-based syntax 8mm Vanadium Can**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<type name="van-cyl-8mm">
  <cylinder id="body">
   <centre-of-bottom-base x="0.0" y="0.0" z="0.0" />
   <axis x="0.0" y="1.0" z="0.0" />
   <radius val="0.008"/>
   <height val="0.04"/>
  </cylinder>
  <material id="van">
    <formula>V</formula>
  </material>
</type>
```

Another proprosal would be to simply use the python syntax defined in [the above section](#S-shape-material) and store this as a straight Python file to be evaluated. There would most likely need to be some kind of registration
system along similar lines to the Python algorithms.

**Python-based file syntax**

```python
from mantid import mm, Csg, Material, SampleHolderFactory

def TopToroid()
    return csg.Translate(Csg.Difference(Csg.Sphere(Radius=2.5*mm, Center=[0,0,0.634]),
                                        Csg.Cuboid([5.1,5.1,4.38])), [0,0,-2.19])

van = Material(ChemicalFormula="V", NumberDensity=0.072)
top = TopToroid()
bottom = Csg.Rotate(TopToroid(), Angle=[180,0,0])
sample_volume = Volume(Csg.Union(top, bottom), Material=van)

SampleHolderFactory.subscribe("SNAP-Double-Toroid-Enclosed", sample_volume)
```

and then in a script

```python
w1 = SetSampleHolder(w1, Name="SNAP-Double-Toroid-Enclosed")
```

**Question**: How do we check the shape that we have defined? It would be best to design it in a CAD program like [OpenSCAD](http://www.openscad.org/) but this will not allow us to assign materials to each of the components.
