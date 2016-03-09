# Spectrum Number and Workspace Index Abstraction Layer


## Motivation

There are two main motivations for this design proposal:
1. We need to provide a consistent user interface that allows users to specify which spectrums in a workspace an algorithm should modify.
2. Developers of algorithms should not have to deal with conversions between spectrum number and other index types.


## Current situation and future problems

#### Definitions:
1. Workspace index = linear index starting at zero, corresponds to memory offset in vector of spectra
2. Spectrum number = user defined index for spectra in certain workspace

#### Current situation:

- Conversion methods between index types (spectrum number and workspace index) are part of the workspace interface.
- There is no consistent way of defining index ranges or lists for algorithms. This is done individually in each algorithm, and properties may be defined for spectrum number or workspace indices, and sometimes the interpretation of index properties even seems to depend on the facility.
- Validation of index ranges and behavior on errors such as out-of-range indices is likewise done individually in all algorithms. Algorithms behave inconsistently depending on errors (throw and error, print a warning, ignore silently). There are bugs in some range validations.

#### Future problems:

When running Mantid with MPI we will most likely store different spectra on different MPI ranks.
As a consequence the workspace index will not longer correspond to the memory offset in the local vector of spectra.
Basically we will have a global index and a local index on each rank.
The local indices from all ranks are disjoint sets that together make up all global indices.

This introduces additional complexity in the index handling and will require definition of new terms.


## Detailed goals

- All algorithms should have a consistent interface.
- Eliminate duplicated code for declaring properties for index ranges and list.
- Eliminate duplicated code for validating indices and converting them to the desired type.
- Developers should generally not have to deal with spectrum number at all. Spectrum number is important for the user interface, but irrelevant for the internals of most algorithms.
- Developers should in the future be isolated from dealing explicitly with the local and global indices that come with an MPI implementation of Mantid.


## User interface

- The interface of algorithms should make it possible to specify spectrum number ranges and lists.
- For better compatibility for the current interface and for users who do not like to deal with spectrum number it should also be possible to specify workspace index ranges and lists.

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
