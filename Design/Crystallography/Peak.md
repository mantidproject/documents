# Making Peak Construction Different

## Motivation

`Peak` suffers from telescoping constructor anti pattern. Peak has many different
constructors to deal with the many different data that can be used to define a
peak. This is a negative for several reasons:

    1. It is very difficult to infer what constructor you need to use and the
       order of arguments from the interface alone.
    2. It overburdens peak with construction logic. A peak should ideally be a
       POD structure.
    3. Duplication of this construction logic occurs in the code base due to a
       chicken an egg problem: A need to compute a set of parameters that match
       a `Peak` constructor from whatever data is currently at hand.

## Current Implementation

Currently there are 6 constructors defined for `Peak`:
    
    1. instrument, Qlab, and optional detector distance.
    2. instrument, Qsample, goniometer matrix, and optional detector distance
    3. instrument, detid, wavelength
    4. instrument, detid, wavelength, hkl
    5. instrument, detid, wavelength, hkl, goniometer
    6. instrument, scattering angle, wavelength

Peak also has a default constructor which leaves the constructed peak in an
invalid state.

Across the code base peaks are either constructed directly (more common in
tests) or using one of these methods are commonly use the construction
functions in `PeaksWorkspace`. Here there are three functions:

 - `createPeak` - create a peak from a vector and a given coordinate frame.
   Calls one of the other three functions.
 - `createPeak` - create a peak from Qlab and an optional detector distance.
 - `createPeakHKL` - create a peak from a HKL vector.
 - `createPeakQSample` - create a peak from a Qsample vector.

Each of these use one of the constructors listed above and use the instrument
attached to the workspace as the instrument parameter.

### Usage of Instrument

With the creation of instrument 2.0 we should move away from holding instrument
objects as member variables. Internally, `Peak` needs access to the instrument
object for the following properties:

 - Getting a detector from a given detector id.
 - Getting the source position.
 - Getting the sample position.
 - Getting the reference frame.
 - Being passed as an argument to `InstrumentRayTracer`.
 - Getting parameters from the IPF (specifically the parameter for the `tube-gap` hack).

Crucially with the current implementation the instrument is needed to be held
for the lifetime of the peak because changing one property of peak requires the
recalculation of many other properties. For example, modifying Qlab requires a
recalculation of the detector id which requires a ray trace using the
instrument. Therefore access to instrument details cannot just be given at
construction time.

## Options for Refactoring

Ideally peak would be a constant POD structure. If a parameter needs to change
then a new peak should be constructed (because many of the internal values need
to be recomputed anyway). With this eventual goal in mind there are a couple of
options for refactoring peak construction.

There are a couple of different options for refactoring peak construction:

#### Use free functions.

Create a collection of `make_peak` functions that loosely match the
constructors of the current implementation. For example:

```cpp
auto peak1 = make_peak(experimentInfo, Qsample);
auto peak2 = make_peak(experimentInfo, detid, wavelength);
```

The immediate issue with this is that it still limits the interface to one of
several methods.

#### Use a builder design pattern. 

This would allow the user to throw whatever data they have at the builder and
retrieve a peak constructed with that info back. For example:

```cpp
PeakBuilder builder(experimentInfo);
builder.addQSample(qSample);
builder.addGoniometer(goniometer);
builder.addHKL(hkl);

auto peak = builder.build();
```

This allows greater flexibility in how to construct peak objects but with the
downside that it is much more verbose.

