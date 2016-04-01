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

### Masking

Masking is an operation on the data not on the Instrument. Masking will therfore not feature in the `Detector` only in the `DetectorInfo` and `SpectrumINfo` layers. Other meta-data should follow the same protocol.

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
  - To facilitate the free data layout, the interface should be `SpectrumInfo::twoTheta(size_t index)` and *not* along the lines of the current implementation with `Workspace::getDteector(size_t index)::twoTheta()`. Going further, the **high-level facades should make direct access to the Detector difficult, but not impossible**
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
- 
### Construction

The `DetectorInfo` should be constructible only with an `InstrumentTree_uptr` as an argument.
Because:

* DetectorInfo doesn't make much sense without an InstrumentTree
* We want IOC, so the contents of the DetectorInfo should be injectable as far as possible
The InstrumentTree is freely copied. So it's a reasonable assumption that we're going to make our DetectorInfo from an existing pre-loaded instrument. At the Workspace level, this means that we copy a Workspace and we also get a smart copy of our InstrumentTree too. I think that is the right semantics.

### Constness

Both the `Node` and `InstrumentTree` are fully immutable. This is a very important aspect of the design. If a future developer starts adding non-const methods to either, the design will break because our ability to detect the `modify` operations is the fundamental aspect that has allowed us to kill the ParameterMap. We should emphaises this where possible by holding `InstrumentTree_const_uptr` over a non-const `uptr`, that way adding non-const methods will cause compile-time failure.

### Ownership - Where are our COW(s)?

In the new deisgn the DetectorInfo holds the `InstrumentTree` the Workspace does not. Given that the `Workspace` holds the `SpectrumInfo`, which holds the `DetectorInfo` which holds the `InstrumentTree`, we may wish to make the `SpectrumInfo` `COW` even though there is nothing to gain by making the InstrumentTree COW (at the client level, because it is internally). DetectorInfo and SpectrumInfo hold `GeometryInfo`. This data may well be the same across multiple workspaces. The `InstrumentTree` does not need to be COW (or rather it is, but via an internal mechanism and not simply by a cow_ptr). However, it can be the same accross multiple DetectorInfo objects, i.e., **it should be held via a shared_ptr, not a unique_ptr**.

### DetectorInfo is not a SpectrumInfo

`DetectorInfo` is not a `SpectrumInfo` even thought they have very similar interfaces. We intend to apply the CRTP pattern to build such types using a common template.

### SOA vs AOS

VTK have now adopted an `Structure of Arrays` approach to their fundamental array types. That has been discussed here, specifically, do we return a `V3D` from a detector, (AOS) or multiple arrays (x, y, z) that can be assembled into a SOA?

See [this](https://gitlab.kitware.com/vtk/vtk/blob/master/Documentation/Doxygen/ArrayDispatch-VTK-7-1.md) for details on how VTK do this. The SOA approach seems to make a lot of sense, and given that VTK have been able to take generic compile-time approaches to handling these is encouraging. However, I (Owen) have several issues with taking the SOA approach when it comes to V3D.

* We have situations where we want to take a polymorphic approach to `Components`, of which `Detectors` are a subclass. Currently `Detectors` are "discovered" and registered at runtime in to the `InstrumentTree` as a AOS (see [here](https://github.com/DMSC-Instrument-Data/instrument-prototype/blob/master/cow_instrument/InstrumentTree.h#L37)). To do the equivalent using the SOA approach, and maintain the ability to return an individual `Detector` such as is done [here](https://github.com/DMSC-Instrument-Data/instrument-prototype/blob/master/cow_instrument/InstrumentTree.h#L26) we'd need some way to slice through our SOA and create the `Detectors` on the fly. 
* Certain geometric operations are still the responsibility of `Components` such as positioning and rotating. Adding two `V3D`s together seems like a sensible operation and provides a nice encapsulation. The same would be true of `Quat` for the equivalent rotation matrix. Furthermore the new `InstrumentTree` relies on knowing and walking sub-trees for write operations. How does one handle this in a SOA configuration. Currently each detector has an index, so it is possible to walk the tree and index into the SOA.

If there is some really heavy Geometry calculation that is not bandwidth-bound the conversion to and from SOA could be done on-the-fly before and after that calculation (with some overhead).
All in all, the advantages of SOA in practice (in Mantid) are right now probably few, so we should not inflict other headaches upon us, i.e., keep the current AOS approach.

As a further note CPUs have slowly (over the last decade) become better at dealing with unaligned or scattered data in combination with the SIMD units, so it may be that the advantages of aligned SOA data are gradually diminishing. 
