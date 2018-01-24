# Matrix Workspace

## Issues with the current workspace

Focussing on `MatrixWorkspace`. At present numbering below is not an indication of seriousness or priority. 

1. Constructed iteratively, i.e., workspaces start their life in an incomplete and dysfunctional state, vital information is added only later (size, instrument, spectrum to detector mapping).
1. No encapsulation for data it contains, thus violating invariants:
   - Access to X, Y, and E makes breaking or abusing internal data easy.
   - Access to spectrum numbers on `ISpectrum` prevents validation (e.g., duplicates).
   - Detector IDs can be set arbitrarily on `ISpectrum`, no check if this is in the instrument.
1. No support for mid-level concepts. Too few building blocks. i.e. `std::transform` on a workspace. Probably explains why Algorithms have become the basic building block in Mantid rather than being seen as they should be - the thing that allows you to expose your functionality to users via python and the workbench.
1. Not enough workspaces types (thus the aforementioned misappropriation of `MatrixWorkspace`).
   - In the current way workspaces and algorithms are built, adding new workspaces types is not very useful since existing algorithms will not work for them.
1. The virtual inheritance issues
   - Often `dynamic_cast` has to be used when working with workspaces, making client code bloated.
     - Not much that a base Workspace actually gives you, and it has lead to the widespread usage of down-casting.
   - Base class `MatrixWorkspace` for `Workspace2D` and `EventWorkspace` was meant to unify handling of the latter two workspaces in algorithms. In reality many algorithms simply have two big blocks for handling them individually.
   - The base class of `MatrixWorkspace`, `ExperimentInfo` is a complicated and holds a lot of complexity related to setting the instrument and loading parameter maps.
     - Provides a detector grouping mechanism based on externally set grouping (i.e., *not* the grouping used by `MatrixWorkspace`), used by `MDWorkspace`.
   - A `MatrixWorkspace` is also an `IMDWorkspace` so has a dimension api as well as axes. This is confusing. Should not have made a `MatrixWorkspace` and `IMDWorkspace`.  
   - Performance as highlighted by Steve [here](https://github.com/mantidproject/documents/files/1383875/2017-03-18-Highlights.pdf)
1. False concept that a Workspace subtypes are a pluggable thing. They really aren't and that has lead to `MatrixWorkspace` having to support very possible usage you might want for a data structure
1. `MatrixWorkspace` is meant to store histograms, but is used for many other purposes:
   - Single values.
   - Single data points in each histogram.
     - Leads to performance problems due to massive overhead from using histograms for this purpose, e.g., at ILL.
     - Need to use `Transpose` algorithm too often for processing/plotting, cutting connection to instrument.
   - Masking.
   - Grouping.
   - HKL values.
1. Support for vertical operations is not well supported in `MatrixWorkspace` and operating `Algorithms`. i.e. performing operations on the same bin across all spectra. You can transpose, but instrument links are lost.
1. Very complicated to copy / create output workspaces.
   - It is a bit mysterious which members need to be copied, unless `WorkspaceFactory` can be used.
   - For example, a fair number of algorithms copy units by hand, but it is not obvious or documented when this is necessary.
1. History can become huge and causes performance issues when working with workspace groups and merging them.
   - SNS, ask Andrei.
1. Pulls in around 120 include files, thus contributing a significant part to compile times for around 300 algorithms (plus their unit tests) that depend on it.
   - Compile times have been highlighted repeatedly as an issue by the development team.
1. Is made for holding "spectra", but is used for transformed data like in `SofQW`.
   - Data is still histograms, but not mappable to detectors, spectrum-detector mapping is useless.
   - Actual meaning of spectra is not supported by workspace, i.e., histogram workspace not in detector space, so spectra should not be mapped to positions via `SpectrumInfo` but to Q.
   - In general, there may be other workspaces containing histograms that do not map to detectors of an instrument.
1. Data in base classes, extended in child class.
   - Data both in base classes and child classes makes design brittle.
   - Should as par as possible use composition rather than inheritance
1. Bloated interface with an abundance of methods for different purposes, but lacking other essentials.
   - Different set of methods in each base class and derived classes.
   - No iterator support.
   - No proper definition of equality and other essential overloaded operators. No easy way to ask if a is equal to b without going through an Algorithm. We appreciate that for some operations we need to match with a tolerance. We would still like to see == operators overloaded more widely.
1. Composite pattern provided by `WorkspaceGroup` is too cumbersome and not flexible enough.
   - Horribly tied into the Analysis Data Service, i.e., cannot be used without.
     - Linking via string names is cumbersome 
     - Some 26 (known) edge cases that currently have to be considered in supporting WorkspaceGroups because of the ADS dependence, ask Lamar. There should be 0. 
   - Wasteful for multi-period workspaces since most of the information is duplicated. 
1. Provides few invariants that client code can rely on.
1. No way of defining a region of interest and inconsistent handling of masking.
   - Masking or bin masking may or may not be respected by algorithms.
   - Generalized 'selection' object attachable to workspace?
1. No design for associating workspaces. i.e. This Workspace is the transmission run associated with this sample run Workspace. Potentially, this would not need to be solved at the Workspace level, but we definitely need better functionality at the user level.
1. Efficient mechanism needed for serializing/deserializing workspaces.
