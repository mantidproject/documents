# Cleanup of the Workspace tree

This document contains some notes on issues and assumptions made by the current workspace tree.
The purpose is to eventually develop a new design based on this, but so far this document contains only random notes.

## Problems in the current design

- `WorkspaceFactory::create(MatrixWorkspace_const_sptr)` will create a workspace of the same type, unless the type is an `EventWorkspace`, then it creates a `Workspace2D`.
  - Note that this implies that `EventWorkspace` should not have subtypes (and indeed it does not, but there is currently no guarantee for this).
  - Therefore, there is an asymmetry for code that actually needs to create an `EventWorkspace`, it has to call `WorkspaceFactory::initializeFromParent()` by hand.
- In many algorithms data is somehow copied from input to output. Typically this seems to neglect any potential data in subtypes of `Workspace2D`, for example `RebinnedOutput::readF()`. Note that due to the use of `WorkspaceFactory::create(MatrixWorkspace_const_sptr)` the output will still be, e.g., a `RebinnedOutput`, but the data may be incomplete.
- `ISpectrum` corresponds to `MatrixWorkspace`. Since most algorithms work with `MatrixWorkspace`, `ISpectrum` has a read-write interface. However, `EventList`, which is one of the subtypes of `ISpectrum` throws for writes to `Y` and `E`.
- `Integration` creates and output workspace from the input workspace, of the same type, unless it is a `RebinnedOutput`, then it creates a `Workspace2D`.
- `WorkspaceSingleValue` has only one histogram, and yet its interface is identical to `MatrixWorkspace`, where all the access routines take a spectrum index. THe spectrum index is ignored in the case of `WorkspaceSingleValue`.
- `SpecialWorkspace2D` is initialized with histograms of length one. Nothing keeps us from changing that later, contrary to the intention of the workspace.
- `EventList` copy constructor cannot be used for event lists in different workspaces since it copies the MRU pointer.
- `EventWorkspace::getEventList` does not call `invalidateCommonBinsFlag()`.
- `GroupingWorkspace`: single number for each workspace that indices to which group the workspace index belongs.
- `MaskWorkspace`: single number indicating mask status.
- `OffsetsWorkspace`: single number indicating something, e.g., offset for `AlignDetectors`.
- Algorithms that accept a `MatrixWorkspace` or `Workspace2D` generally assume that they can resize the histograms.
- `WorkspaceFactory::create` has a mechanism for checking for different-size workspaces, and then does, e.g., not copy the bin masking. The mechanism looks a bit broken (e.g., for different number for spectra but some y-length, or if the y-length is explicitly given but the same as the input).
