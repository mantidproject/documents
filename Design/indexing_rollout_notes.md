# Indexing rollout

This is not a design document, but an addendum to the [Indexing design document](https://github.com/mantidproject/documents/blob/master/Design/spectrum_number_and_workspace_index_abstraction.md).
This document contains notes and is meant for planning the rollout of indexing changes, in particular removing spectrum number and detector IDs from `ISpectrum`.

## Remarks

It has been discussed more than once that the term *workspace index* is misleading.
The only argument for keeping it is consistency.
Throughout this document the better term *spectrum index* or simply *index* will be used.
The nomenclature in the Mantid code base could be changed together with this major change.
Note that this does not necessarily imply that the nomenclature on user-interface side changes as well.

## Statistics

Most relevant methods that need to be removed are part of `ISpectrum`.
The following table gives and estimate of the number of occurrences of the respective methods.

| Method        | Occurrences | Files  |
| ------------- |:-------------:|:-----:|
| `ISpectrum::getSpectrumNo()` | 271 | 99 |
| `ISpectrum::setSpectrumNo()` | 153 | 104 |
| `ISpectrum::copyInfoFrom()` | 26 | 17 |
| `ISpectrum::ISpectrum()` | ? | ? |
| `ISpectrum::operator=()` | ? | ? |
| `???DetectorID?()` | ~900 | ~300 |
| `EventList::operator+=(const EventList &)` | ? | ? |

An initial survey shows that almost half of the occurrences are for workspace initialization.
Those cases are usually comparatively easy and straightforward to replace by the new style of workspace factory functions defined in `DataObjects/WorkspaceCreation.h` that use `IndexInfo` to create a workspace.

Other significant fractions of the occurrences are made up by logging and exceptions and by tests that initialize individual spectra.
Furthermore there are comparisons between the respective spectrum and detector information in two workspaces.


## General goals

- Quite a few algorithms take an input workspace, extract information about spectrum numbers and detector IDs, and initialize a new workspace based on those data. Example include `SumSpectra`, `DiffractionFocussing`, and `ExtractSpectra`.
  One goal of the indexing library is to remove explicit uses of spectrum numbers and detector IDs in as much code as possible.
  Since we need to refactor algorithms similar to those mentioned above, it is probably a good idea to do it properly right away.
  That is, we should *not* just refactor the manipulation of spectrum numbers and detector IDs via `IndexInfo`.
  Instead, we should provide functionality for grouping and extraction of spectra to create a new `IndexInfo`, without the need for explicit handling of spectrum numbers and detector IDs.

  As an example, consider

  ```cpp
  namespace Indexing {
  IndexInfo extract(const IndexInfo &, const SpectrumIndexSet &);
  IndexInfo group(const IndexInfo &, const std::vector<SpectrumIndexSet> &);
  }
  ```

- Should we set default detector IDs?
  This is was workspaces are doing currently, but it does not really make sense.
  Probably we should find a better way if setting sensible detector IDs once an instrument has been set.
  This is something that potentially needs to be decided together with other decisions regarding Instrument-2.0.


## NearestNeighbours

- Uses `specnum_t` as map key.
- Should simply use spectrum index?
- Would that make trouble with MPI? Need to have a detailed look.
- See issue [#17372](https://github.com/mantidproject/mantid/issues/17372).


## Logging and exception messages

- Frequently spectrum numbers are included in log messages or exceptions.

- Probably the easiest (overall) solution is to add means of getting this information automatically, e.g., with a helper function

  ```cpp
  namespace Logging {
  std::string spectrumNumber(const MatrixWorkspace &workspace, size_t index);
  }
  ```

## File- and UI output

Similar to logging, there are also several algorithms that write, e.g., detector IDs to a file.
Maybe a similar or even the same helper function as suggested above in the logging section could be used.


## Obtaining detector information

Frequently, detector IDs are used to obtain detector pointers or other detector-related information from the instrument.
The IDs are not actually required here.
Refactoring would be significantly easier (and would avoid the need to revisit and incrementally refactor) if such information was available via, e.g., `MatrixWorkspace::SpectrumInfo`.

Commonly used functionality includes:

```cpp
class SpectrumInfo {
  bool isMasked(const size_t index) const;
  bool isMonitor(const size_t index) const;
  double l2(const size_t index) const;
  Detector_sptr uniqueDetector(const size_t index) const; // Throws if no or more than 1 detector
  bool hasUniqueDetector(const size_t index) const; // Should this be part of IndexInfo instead?
};
```

There is also another (special?) case (example from current code):

```cpp
Geometry::IDetector_const_sptr det;
size_t numDetectors = workspace->getSpectrum(wi).getDetectorIDs().size();
if (numDetectors > 1) {
  Instrument_const_sptr inst = workspace->getInstrument();
  det = inst->getDetector(*workspace->getSpectrum(wi).getDetectorIDs().begin());
} else {
  det = workspace->getDetector(wi);
}
```

## Duplicate spectrum numbers

Currently quite a few algorithms or tests use or create workspaces with non-unique spectrum numbers.
Ultimately we want to forbid this, but it is not yet clear if we should attempt to clean this up right away, or wait until `IndexInfo` has developed into a more stable state.


## Standards

#### Spectrum numbers starting at 0

Currently quite a few algorithms that create workspaces where spectrum numbers do not start at 1 but at 0.
This is non standard.
Should this be cleaned up as part of this refactoring effort?

Examples:

- `AppendSpectra`


## MatrixWorkspace

There is a considerable number of methods in `MatrixWorkspace` that could potentially be replaced or removed during this refactoring effort.
The detailed strategy should depend on how and where these methods are used.

```cpp
class MatrixWorkspace {
public:
  void updateSpectraUsing(const SpectrumDetectorMapping &map);
  void rebuildSpectraMapping(const bool includeMonitors);
  spec2index_map getSpectrumToWorkspaceIndexMap() const;
  detid2index_map getDetectorIDToWorkspaceIndexMap(bool throwIfMultipleDets) const;
  std::vector<size_t> getDetectorIDToWorkspaceIndexVector(detid_t &offset, bool throwIfMultipleDets) const;
  std::vector<size_t> getSpectrumToWorkspaceIndexVector(specnum_t &offset) const;
  std::vector<size_t> getIndicesFromSpectra(const std::vector<specnum_t> &spectraList) const;
  size_t getIndexFromSpectrumNumber(const specnum_t specNo) const;
  std::vector<size_t> getIndicesFromDetectorIDs(const std::vector<detid_t> &detIdList) const;
  std::vector<specnum_t> getSpectraFromDetectorIDs(const std::vector<detid_t> &detIdList) const;
};
```


## Notes about individual algorithms

The following is a more or less random selection/collection about specific algorithms or classes and how the could or should change.

#### SumSpectra

Uses smallest spectrum number in sum as spectrum number for output.
This does not seem to make much sense, maybe it is just an arbitrary requirement by an individual piece of client code.
It would probably be easier and cleaner to simply remove special handling of spectrum numbers from `SumSpectra` and adapt the client code in question.

#### MDWorkspace

`ConvertToDiffractionMDWorkspace::convertEventList` takes an `EventList` and its its events to an `MDWorkspace`.
This procedure requires the position of the `EventList`.
Currently this is determined by the detector IDs stored in the `EventList`.
A different mechanism is required here, probably with a change in the function signature.

#### SpectrumDetectorMapping

This class is used in a few algorithms, e.g., `SofQWNormalisedPolygon`, to set/update the detector IDs in a workspace via `MatrixWorkspace::updateSpectraUsing`.
Probably this functionality can simply be replaced by basic `IndexInfo` functionality.
Ultimately, it might be possible to remove the class `SpectrumDetectorMapping`.

#### BinaryOperation

`BinaryOperation` attempts to match detector IDs from two workspaces.
Do we need such functionality in `IndexInfo`?
What about the MPI case?
The distribution of detectors onto MPI ranks could be different for each workspace.

#### ConvertDiffCal

Uses detector IDs to get detector for spectrum.
Does not actually need detector ID itself?
`SpectrumInfo` should be able to provide such functionality, but how do we deal with this until it is available?


## Refactoring strategies

1. Check if the code in question can be removed. This is the case, e.g., when setting spectrum numbers that either match the default or when the actual values do not matter (some tests).


## Python exports

The methods from the `ISpectrum` interface are exported to Python.
They seem to be used in relatively few scripts, but we should make sure that scripts outside our repository keep working, or fail in a way that suggests a solution.
We seem to have two options:

1. The `MatrixWorkspace::getSpectrum` export could be modified to return a wrapper around the actual spectrum and a reference/pointer to the containing workspace.
  Access via the old interface to spectrum numbers and detector ID can then internally forward to the respective replacements via `MatrixWorkspace::indexInfo()`.
  The disadvantage of this are potential performance issues.

2. Simply replace the exports by dummy versions that print errors containing information on how to fix scripts.
