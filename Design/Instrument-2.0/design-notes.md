# Instrument-2.0 Design Notes

The primary focus of this document is to describe and design the top level interface to the `InstrumentTree`. How will the clients of the `Instrument` access the information they need? How will the performance issues associated with fast reads be addressed?

## Overview

- Copy-on-write `InstrumentTree`, similar to the [prototype](https://github.com/DMSC-Instrument-Data/instrument-prototype). The design of this component is not the core focus of this document.
- `DetectorInfo`, a class that stores (and provides access to) basic parameters of detectors, such as L2, twoTheta, position, masking flags, monitor flags, ....
- `SpectrumInfo`, a class that stores (and provides access to) basic parameters of spectra, such as L2, twoTheta, position, masking flags, monitor flags, .... The values hare are derived from those on `DetectorInfo`. This class reflects the common case in Mantid that a spectrum can represent more than one detector, e.g., due to grouping of detectors or after summing spectra.


## Notes

### Spectrum-number and detector ID

Mantid currently works with `SpectrumNumber` and `DetectorID` in many places.
As discussed in detail in this [design proposal](https://github.com/mantidproject/documents/blob/spectrum_number_and_workspace_index_abstraction/Design/spectrum_number_and_workspace_index_abstraction.md), these concepts should not be spread accross our codebase.
Apart from the arguments presented there, early tests with the [prototype](https://github.com/DMSC-Instrument-Data/instrument-prototype) showed that using `DetectorID` as an index for accessing detector data is inefficient, since the resulting `std::map` lookups slow things down significantly.

Therefore, neither `SpectrumNumber` nor `DetectorID` should be part of the core mechanics of the instrument.
Translation to a plain index, e.g., for accessing a `std::vector` should happen as close to the user interface as possible.
Mechanism for this translation would probably be part of the workspace interface, but separate from, e.g., `SpectrumInfo`.
The remainder of this document is thus not concerned with `SpectrumNumber` or `DetectorID`.

### Naming

All class names in this document are preliminary and just for the sake of discussion.
Better names are needed in several cases.


## Design

### Structure

Algorithms that work with workspaces need to access information about spectra.
Therefore:

- `SpectrumInfo` should be a member of workspace.
- `SpectrumInfo` owns `DetectorInfo`.
- `DetectorInfo` owns `InstrumentTree`.

If no detectors are grouped, there is a 1:1 mapping between spectrum and detector.
`SpectrumInfo` and `DetectorInfo` should thus share data, to avoid waste of memory and CPU resources.
This can be facilitated by:

- `GeometryDataArray` is used to store vectors of data, such as L2, twoTheta, position, masking flags, monitor flags, ....
- `SpectrumInfo` and `DetectorInfo` have a field `std::shared_ptr<GeometryDataArray>`. By default both point to the same instance. If detectors are grouped, `SpectrumInfo` allocates its own `GeometryDataArray`.

### Interface

The interface to `SpectrumInfo` and `DetectorInfo` would be almost identical.
The most typical examples for public methods include:

```cpp
bool isMonitor(size_t index);
bool isMasked(size_t index);
double L2(size_t index);
double twoTheta(size_t index);
V3D position(size_t index);
```

Furthermore, we need to provide access to lower-level data, e.g., via a method `const Detector &DetectorInfo::detector(size_t index)`.
For `SpectrumInfo` we could have `const std::vector<const Detector *> detectors(size_t index)`.

Note that although the index in the public interface is the same. They relate to two different indexing mechanisms. For example, on `SpectraInfo::isMonitor(size_t index)` the `index` is the spectrum index, which goes from 0 to the maximum number of spectra. On the other hand `DetectorInfo::isMonitor(size_t index)` the `index` is the detector index. This can be larger than the available number of spectra when mapping is not 1:1. 

### Read access

- Access functions take an index which is used for accessing an underlying `std::vector` of data.
  - The data layout in `GeoemtryDataArray` is not defined, and could be changed in the future.
  - To facilitate the free data layout, the interface should be `SpectrumInfo::twoTheta(size_t index)` and *not* along the lines of the current implementation with `Workspace::getDteector(size_t index)::twoTheta()`.
  - Accessors should probably be declared inline for performance reasons.

### Write access

Write access requires modification of all three data structures, `InstrumentTree`, `DetectorInfo`, and `SpectrumInfo`.
I (Simon) do not yet have an entirely clear picture of this.
Notes:

- Do we always go via `InstrumentTree` upon modification? For example, masking a spectrum or a detector could be handled at the `SpectrumInfo` or `DetectorInfo` level. These components could also have a copy-on-write mechanism. We would then still share the same `InstrumentTree` for workspaces that have different masking.
- See the `Command` mechanism in the [prototype](https://github.com/DMSC-Instrument-Data/instrument-prototype). These could be filtered through `SpectrumInfo` and `DetectorInfo`.
- When changing, e.g., the position of a bank, we will subsequently change the position of all pixels in that bank. We have to make sure that we do not trigger a full update of `SpectrumInfo` with each position change of a pixel. Instead, the derived position in `SpectrumInfo` should be computed only once after the update is complete.
- Since writes are relatively rare, it may be plausible to proceed with an instrument modification as follows:
  1. Invalidate `SpectrumInfo` and `DetectorInfo`
  2. Update `InstrumentTree`.
  3. Update/rebuild `DetectorInfo`.
  4. Rebuild `SpectrumInfo`.
  It has to be clarified how this could happen transparently to clients. Ideally we would like to avoid the need for manual calls to something like `invalidateSpectrumInfo()` and `rebuildSpectrumInfo()`. One option might be to just let modifying clients *set* a new `InstrumentTree` (based on a copy of the current tree), which would then trigger the updates.
- Writes to `InstrumentTree` may need to update, e.g., the position of a detector. A detector should thus have a field `size_t index` that allows upgraded the corresponding data in `DetectorInfo`.
