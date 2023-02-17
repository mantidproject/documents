# Supporting More Complex Beam Path Geometry

This document is not yet a full design document but is meant to serve as
notes capturing ideas that have been discussed regarding how Mantid might
support unit conversion for instruments where the neutron beam path is
more complicated than `source -> sample -> detector`.

## Current Status

The main Mantid unit conversion algorithm,
[ConvertUnits](https://github.com/mantidproject/mantid/blob/3f9b29fc243c6201f9a662b6a5e4500fdecece41/Framework/Algorithms/src/ConvertUnits.cpp#L374),
uses a set of [Unit](https://github.com/mantidproject/mantid/blob/3f9b29fc243c6201f9a662b6a5e4500fdecece41/Framework/Kernel/inc/MantidKernel/Unit.h)
classes that implement to/from time-of-flight conversions.
Using time-of-flight as a "base unit" that each unit understands allows conversion between
any arbitrary pair of units thereby avoiding the need to write an exhaustive list
of conversions for all combinations of conversion.

The unit class conversions are parametrized by:

- `l1`: Distance from source to sample scatter point
- `l2`: Distance from sample scatter point to centre of detector pixel
- `twoTheta`: Scattering angle into centre of detector pixel
- `efixed`: For inelastic scattering the fixed energy value of either the incident
  beam (direct mode) or final energy selected to hit the detector pixel (indirect mode)
- `difa`, `difc`, `tzero`: Optiona diffractometer calibration constants used to correct errors in detector positions

For each spectrum `ConvertUnits` computes the required parameters and the current implementation
linked above uses a simple beam path of `source -> sample -> detector`, where:

- `source` is the component marked as `source` in the IDF and returned by `Instrument::getSource`
- `sample` is the component marked as `samplePos` in the IDF and returned by `Instrument::getSample`
- `detector` is the pixel for a given spectrum who units are under conversion.

The IDF concepts are defined [here](https://github.com/mantidproject/mantid/blob/3f9b29fc243c6201f9a662b6a5e4500fdecece41/docs/source/concepts/InstrumentDefinitionFile.rst#special-types).

## Issues

The current implementation does not cater for additional components with the
flight path of the neutron between the source and sample points.
One example of this is the placement of supermirrors that "bounce" the
beam path and change the effective `l1` and `twoTheta` values for the
Reflectometers. For this case a custom conversion algorithm,
[`ConvertToReflectometryQ`](https://github.com/mantidproject/mantid/blob/3f9b29fc243c6201f9a662b6a5e4500fdecece41/Framework/Reflectometry/src/ConvertToReflectometryQ.cpp),
has been written that moves the detector components such that they see the "correct"
`twoTheta` angle. This is suboptimal and ends up with the `l1` being incorrect
but it is generally small enough not to matter.

Another downside of providing a custom conversion algorithm is that it cuts off
the suite of existing unit conversions from the workspace after this point as
using the standard routines will use the simple beam path and give unexpected
and inconsistent answers.

## Ideas

At this stage ideas are being explored around how to adapt Mantid to deal with
these issues, two have been proposed:

- Use the existing support for diffractometer contants to correct for `l1` and `twoTheta`.
  This would require input from some kind calibration to compute parameters like `difc`, `difa`
  and `offsets`. These constants fit more naturally in the diffraction world and might
  still be viewed as a "fudge".

- Allow multiple "source" components within the IDF and internal instrument representation.
  `ConvertUnits` would then use the sum of all of the distances between the components
  to give an an effective `l1` and use the final "source" component to compute the
  angle of incidence and then `twoTheta` for that spectrum.

### Multiple Sources

This solution should be minimally impactful in the code. It would involve:

- either adding a new tag or allowing multiple "source" tags in the IDF. This
  will require changes in the
  - [`InstrumentDefinitionParser`](https://github.com/mantidproject/mantid/blob/06e2fb459836d153a9c9bf857b32e5eb931791a3/Framework/Geometry/inc/MantidGeometry/Instrument/InstrumentDefinitionParser.h)
  - the [IDF schema](https://github.com/mantidproject/mantid/blob/main/instrument/Schema/IDF/1.0/IDFSchema.xsd)
  - the [Instrument](https://github.com/mantidproject/mantid/blob/06e2fb459836d153a9c9bf857b32e5eb931791a3/Framework/Geometry/inc/MantidGeometry/Instrument.h)
    class will need to understand and store an ordered vector of "source" components and `getSource()` will need to acquire an index that should default to `0`
    to preserve existing behaviour.
  - `ComponentInfo`, `DetectorInfo`, `SpectrumInfo` classes will need to be updated to cache
    [`l1`](https://github.com/mantidproject/mantid/blob/15ef1d68a3427cf52dbf91faa2072ca5c5bae02d/Framework/Beamline/src/DetectorInfo.cpp#L188)
    as the sum of the source paths instead of just the current `source -> sample` distance along with []`twoTheta`](https://github.com/mantidproject/mantid/blob/15ef1d68a3427cf52dbf91faa2072ca5c5bae02d/Framework/Geometry/src/Instrument/DetectorInfo.cpp)

In theory as long as the various `Info` classes are update accordingly then `ConvertUnits` should follow with the correct anwser for
the more complex paths. This has not been prototyped and needs further exploration to understand if this would satisfy all
of the requirements.
