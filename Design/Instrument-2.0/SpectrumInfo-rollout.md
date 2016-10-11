SpectrumInfo Rollout
====================

`SpectrumInfo` will be part of Instrument-2.0 and recently it has been added to Mantid as a [wrapper class around existing functionality](https://github.com/mantidproject/mantid/pull/17394).
Early adoption and rollout of this wrapper class aids in the transition to the interface of Instrument-2.0.
Part of the implementation of Instrument-2.0 will then simply consist in replacing the *internals* of `SpectrumInfo` while the interface remains unchanged.

This document is not a design document but merely discusses the rollout methodology and process.

So far `SpectrumInfo` supports a limited set of key functionality and is used in relatively few algorithms.
All current functionality is read-only.


## Rollout Status and Hurdles

The rollout fraction of `SpectrumInfo` is roughly given the number of uses of `MatrixWorkspace::getDetector()`.
There are several cases where this is used:

1. `SpectrumInfo` has the required functionality but simply has not been rolled out to that algorithm yet.

2. `SpectrumInfo` has parts of the required functionality but not all. Using `SpectrumInfo` *and* `MatrixWorkspace::getDetector()` would be doubling the work.
  Rollout is postponed until remaining functionality is available.

3. Missing functionality in `SpectrumInfo` for advanced geometry access and shape access (see below).

4. Missing functionality in `SpectrumInfo` for `ParameterMap` access (see below).

5. Actual modification of the instrument at the detector (not spectrum) level.
  This would require `DetectorInfo` or the actual `InstrumentTree` from Instrument-2.0.


#### Read and write access to `ParameterMap`

Neither read nor write access to the underlying `ParameterMap` is currently supported by `SpectrumInfo`.
There is implicit read access for `isMasked` and `isMonitor` but in those cases the access is hidden behind the interface of `IDetector`.
The by far most frequent use of `ParameterMap` is to obtain the `EFixed` parameter for direct and indirect geometry instruments.


#### Advanced geometry access and shape access

`SpectrumInfo` does currently not provide access to the shape of a detector or things like the solid angle (`Object::solidAngle()`).
It is not clear whether or not providing this is beneficial.
The result would be a considerably bigger interface of `SpectrumInfo` that is used be relatively few clients.

We can avoid this by providing access to the `Detector` via `SpectrumInfo`.
Read access should not create difficulties, the only effect is that client code refactoring would be postponed until the introduction of Instrument-2.0.
The same goes for write access, but this may be slightly more risky once we start transitioning from `SpectrumInfo` as a pure wrapper object to an object that stores data.


## Masking

Masked detectors are currently stored in the `ParameterMap`.
This is very inefficient and slow (like all other access, but masking is one of those used most frequently).

If we add write access to the mask flags to `SpectrumInfo` we can in principle move the mask flags from `ParameterMap` to somewhere else.
Since masking in Mantid is only handled on the detector level right now, 'somewhere else' cannot be `SpectrumInfo` but must be `DetectorInfo`.

Masking in Nexus files is stored as part of `ParameterMap`, that is we need to be able to extract mask values from the `ParameterMap` after loading such a file and reinsert the mask values before saving.


## Proposed Strategy

- It is not obvious how much of advanced geometry and `ParameterMap` access we want to expose at the `SpectrumInfo` level, and how.
  Doing so now in a particular way is a risk since we might need to change things later.
  However, this is blocking item (2.).
  Providing `std::shared_ptr<Detector> SpectrumInfo::detector(size_t index)` will remove that roadblock, with really minor refactoring.

- Masking and the addition of `DetectorInfo` looks like a worthwhile next step to push things closer towards the ultimate Instrument-2.0 design.
  Masks are written to in relatively few places so this could be achieved within a reasonable time frame.
