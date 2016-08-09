# Upcoming changes: Indexing


## Motivation

1. Consistent UI for specifying spectra or detectors in a workspace an algorithm should act on.
2. Developers of algorithms should not have to deal with conversions between spectrum number and other index types.
3. Index handling will get *significantly* more complex in MPI-based Mantid runs and it is absolutely crucial to provide a good abstraction.


## Design

The high level design document can be found in this [pull request](https://github.com/mantidproject/documents/pull/24) or in the current revision of the [markdown file](https://github.com/mantidproject/documents/blob/62763b839f8454a3452f662cfcb7d8b5d49190f5/Design/spectrum_number_and_workspace_index_abstraction.md).


## Examples: What changes how and why?

Disclaimer: Most of this is not implemented yet and subject to change.

#### Declaring properties

Declaring properties that allow specifying spectra (given by spectrum number, workspace index, or detector ID) or detectors (given by detector ID) should be possible with a single line of code:

```cpp
declareSpectrumProperty(Accept::SpectrumNumber | Accept::WorkspaceIndex);
```

#### User interface

The resulting properties in the UI could look like this:

```python
Spectrum range selection:
(*) Spectrum numbers
( ) Workspace indices

Min:  [      ]  Max: [      ]
List: [                     ] # 1,2,3,8-10
```

Leaving all fields empty will select all spectra.

#### Working with input from user interface

Validation will be done in a central place, *not* in every algorithm.

```cpp
auto translator = workspace.indexTranslator();
auto indices = translator.makeSpectrumIndexSet(getSpectrumProperty());

// Could also use OpenMP (PARALLEL_FOR macros)
for(const auto &index : indices) {
  workspace.mutableY(index) = 0.0;
}
```

#### IndexTranslator

- Currently spectrum number (`specnum_t`) and detector IDs (`std::set<detid_t>`) stored in `ISpectrum`.
- This is not compatible with the improved design (at least not without introducing significant code and performance overhead).
  - Simplest example: We cannot prevent duplicate spectrum numbers in a workspace if the spectrum number is stored and set via `ISpectrum`.
- A new object, `IndexTranslator`, will be added to `MatrixWorkspace` and will be responsible for storing and handling spectrum numbers and detector IDs in a central place.

#### New types for spectrum numbers and detector IDs

- `specnum_t` and `detid_t` are merely a `typedef`, i.e., there is no type safety.
- Most likely new types `SpectrumNumber` and `DetectorID` will be introduced for increased safety.

#### MPI, and how to hide it from a majority of algorithms

```
Spectrum number        1 2 3 7 8
MPI rank               0 0 0 1 1
Workspace index        0 1 2 0 1
Global workspace index 0 1 2 3 4
```

- Current situation: UI -> `WorkspaceIndex` -> use as index for obtaining data for spectrum
- MPI:
  - `GlobalWorkspaceIndex` corresponds to what user wants to see and input.
  - For accessing data in workspace we need a *local* workspace index.
  - Neither user nor (most) developers want to know or should have to know and deal with this complexity.

```cpp
// User input could be: WorkspaceIndexList={1,2,3}
auto translator = workspace.indexTranslator();
// Rank 0: indices = {1,2}
// Rank 1: indices = {0}
auto indices = translator.makeSpectrumIndexSet(getSpectrumProperty());

// No changes required!
for(const auto &index : indices) {
  workspace.mutableY(index) = 0.0;
}
```
