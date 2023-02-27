# Supporting More Complex Beam Path Geometry

This document is not yet a full design document but is meant to serve as
notes capturing ideas that have been discussed regarding how Mantid might
support unit conversion for instruments where the neutron beam path is
more complicated than `source -> sample -> detector`.

Note that this document is focussed on calculations in the Mantid code
to implement geometry that is supplied via the existing [IDF](https://github.com/mantidproject/mantid/blob/3f9b29fc243c6201f9a662b6a5e4500fdecece41/docs/source/concepts/InstrumentDefinitionFile.rst)
mechanism; it does not consider other requirements such as alternative ways
to define the geometry outside of IDFs.

This document is focussed on ISIS requirements and does not therefore consider
limitations with data structures such as Workspace2D or issues with constant-wavelength
instruments.

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
Reflectometers. For this case a workaround is used where the source is placed at a
fake location whose position gives the expected incident angle (to do: check how
this is done and put together some test examples).

Custom unit conversion algorithms may be used (to do: find examples) but this
cuts off the suite of existing unit conversions from the workspace after this
point as using the standard routines will use the simple beam path and give
unexpected and inconsistent answers.

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

Other solutions have not yet been considered; any change to the underlying way
`ConvertUnits` works is likely to involve widespread changes throughout Mantid
and would therefore involve significantly more coding and testing effort.

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
the more complex paths. This has not been prototyped and needs further exploration to understand if this would work reliably in all current cases.

Additionally, this would only go so far as to re-implement current unit-conversion functionality with the new geometry; significant additional
investigation would need to be undertaken to see if this would meet the additional requirements for the new features that this is intended to support.

## Next steps

A rough outline of steps to scope the work based on the multiple-sources approach is suggested below. 

Significant effort will be required at all stages by both beamline scientists and Mantid developers, so careful consideration should be given to the
availablility of resources and the priority and timing of this scoping work. Several meetings may be required to discuss this whole process before
embarking on any detailed investigations.

- Scientists to clarify the full list of required features that are limited by the current geometry implementation, and their priorities and impact. *Outcome*: which features to continue to scoping stage.
- Scientists to undertake scoping work for selected new features to determine how the suggested new geometry components will be used. Include initial discussions with developers to discuss feasibility of each feature. *Outcome*: evidence that the multiple-sources approach is feasible from a **scientific perspective**.
- Developers to perform full investigation and prototyping of the multiple-sources approach for **existing functionality**. Requires examples and test data from scientists. Outcome: evidence that the multiple-sources approach is feasible from an **implementation perspective**.
- Scientists to provide full scope and test data for **new features** to the development team.
- Developers to undertake full investigation/prototyping work for **new features**. *Outcome*: implementation plan and estimates.
- Decision on whether to go ahead with implementation for some/all features.

