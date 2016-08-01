# Spectrum Number and Workspace Index Abstraction Layer


## Motivation

There are three main motivations for this design proposal:

1. We need to provide a consistent user interface that allows users to specify which spectra in a workspace an algorithm should modify.
2. Developers of algorithms should not have to deal with conversions between spectrum number and other index types.
3. Index handling will get *significantly* more complex in MPI-based Mantid runs and it is crucial to provide a good abstraction.


## Current situation and future problems

#### Definitions:

1. *Workspace index* = linear index starting at zero, corresponds to memory offset in vector of spectra
2. *Spectrum number* = user defined index for spectra in a certain workspace
3. *Detector ID* = user defined index for detectors in a certain instrument

For an MPI-based Mantid run we need to extend this definition:

4. *Global workspace index* = linear index starting at zero, contiguously labeling all spectra on all MPI ranks.

The definition of *workspace index* stays the same, it still gives the memory offset in the (local) vector of spectra.
That is, the workspace index is an index in the local address space of an MPI rank, the global workspace index is an index in the (imaginary) global address space.
Examples:

```bash
# Without MPI (or single MPI rank)
Spectrum number        1 2 3 7 8
Workspace index        0 1 2 3 4
Global workspace index 0 1 2 3 4

# 2 MPI ranks (interleaved distribution of spectra)
Spectrum number        1 2 3 7 8
MPI rank               0 1 0 1 0
Workspace index        0 0 1 1 2
Global workspace index 0 1 2 3 4

# 3 MPI ranks (block-wise distribution of spectra)
Spectrum number        1 2 3 7 8
MPI rank               0 0 1 1 2
Workspace index        0 1 0 1 0
Global workspace index 0 1 2 3 4
```

#### Current situation:

- Spectrum numbers are stored in their corresponding spectra.
  This implies that there are no checks on the spectrum numbers that are set, e.g., it is possible to have two spectra with the same spectrum number (the `EventWorkspace` interface seems to be doing this for certain combinations of calls to its interface methods, see [17073](https://github.com/mantidproject/mantid/issues/17073)).
- Conversion methods between index types (spectrum number and workspace index) are part of the workspace interface.
  - Maps are build on-demand from the data stored in the vector of spectra and are returned by value.
  - In many cases the spectrum number is defined as `workspace_index + offset`, typically `offset = 1`.
    This definition will break down completely in the MPI case where instead the spectrum number would be defined as `global_workspace_index + offset`.
    The global workspace index is, however, now immidiately available at the level where such computations are currently done.
- There is no consistent way of defining index ranges or lists for algorithms.
  This is done individually in each algorithm, and properties may be defined for spectrum number or workspace indices, and sometimes the interpretation of index properties even seems to depend on the facility (`LoadEventNexus`, see [13475](https://github.com/mantidproject/mantid/issues/13475)).
- Validation of index ranges and behavior on errors such as out-of-range indices is likewise done individually in all algorithms.
  - Algorithms behave inconsistently depending on errors (throw and error, print a warning, ignore silently).
  - There are bugs in some range validations (see [15414](https://github.com/mantidproject/mantid/issues/15414)).
  - Some algorithms do not validate for duplicate spectrum numbers and double-process the corresponding spectra (see [16651](https://github.com/mantidproject/mantid/issues/16651)).
  - Validations are not unit-tested to a good extent.

#### Future problems:

When running Mantid with MPI we will store different spectra on different MPI ranks.
As a consequence the workspace index (as we would get it as user-input via an algorithm property) will no longer correspond to the memory offset in the local vector of spectra.
Basically we will have a global index and a local index on each rank, as exemplified above.
The local indices from all ranks are disjoint sets that together make up all global indices.

This introduces additional complexity in the index handling.
It is pretty clear that we should not and cannot put the burden of dealing with the global indexing scheme on all our (algorithm) developers.
A lot of care needs to be taken when translating between local and global indices since any mistake will lead to incorrect results that can be very hard notice and are very difficult to trace down.
It is thus absolutely crucial that this is done only in a single location in our code base and is unit tested really well.

#### Instrument 2.0:

Instrument 2.0 will come with MPI support.
Cleaning up our index handling is thus a prerequisite for its implementation.


## Detailed goals

- All algorithms should have a consistent interface.
- Eliminate duplicated code for declaring properties for index ranges and list.
- Eliminate duplicated code for validating indices and converting them to the desired type.
- Developers should generally not have to deal with spectrum number at all. Spectrum number is important for the user interface, but irrelevant for the internals of most algorithms.
- Developers should in the future be isolated from dealing explicitly with the local and global indices that come with an MPI implementation of Mantid.

## User interface

On the user-interface side it must be possible to specify certain spectra or detectors.

### SpectrumNumbersProperty

- The interface of algorithms should make it possible to specify spectrum number ranges and lists.
- For better compatibility for the current interface and for users who do not like to deal with spectrum number it should also be possible to specify workspace index ranges and lists.
  It is important to note that this is a **global** workspace index, in an MPI-based Mantid run this is **not** the same as the workspace index.
- Some algorithms also accept detector IDs and then identify corresponding spectrum numbers.

The details of the interface are an open question, I see three options:

1. Always show entry fields for both, spectrum number and workspace index properties.
2. Add a toggle to each algorithm dialog, to show either spectrum number or workspace index properties.
3. Have a setting that globally (for all algorithms) selects the interface with spectrum number or workspace index properties.


## Internals

My current understanding is that only relatively simple changes are required to reach the goals outlined above.
The biggest task may turn out to be rolling out the new user interface without breaking too many scripts.

The proposed design has the following components:

- Introduce a class that deals with translation and validation of indices. This will replace code that is now in `MatrixWorkspace` (translation) and in many algorithms (validation).
  - In contrast to the current situation this can be unit tested very well.
  - Defines a consistent way of dealing with errors in the index specification. This is basically also part of a consistent user interface.
  - Reduces amount of code in algorithms and makes them more readable.
- Provide a convenience function or method for declaring all relevant algorithm properties in a single statement.
  - Reduces amount of code in algorithms and makes them more readable.
  - Automatically gives consistent interface.
- Spectrum numbers can be defined differently in each workspace. As a consequence the object dealing with translation must be linked to a workspace. For example, it could be a member of the workspace.
- We should make sure that we do not negatively influence performance when a trivial set of indices is specified by the user. Trivial can mean either the full range or a range in combination with a trivial mapping from spectrum number to workspace index (such as a simple offset of 1).

A very basic example that covers some of the features described here (property declaration and range validation, but not translation from spectrum number) can be found as part of [this pull request](https://github.com/mantidproject/mantid/pull/15465).
