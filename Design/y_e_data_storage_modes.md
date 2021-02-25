# Y and E data storage modes

## Introduction

- Currently our data structures for X, Y, and E (both the old ones and the new `Histogram` type) all have multiple personalities (`BinEdges` and `Points`, `Counts` and `Frequencies`, `StandardDeviations` and `Variances`).
  In particular, it is typically not clear what type of data a given `Histogram` is storing at a given point in time.
- Up to a certain point this is making development of an algorithm more convenient, since all data can just be dumped into anonymous container and be modified arbitrarily at will.
- However, there are several severe disadvantages:
  - We have no guarantee about an Algorithm's behavior unless only well trodden paths are followed.
  - Writing algorithms becomes harder since many checks have to be done to attempt determination of the storage modes.
  - Some checks may not be correct or even possible, e.g., it is impossible to figure out whether `E` stores variances or standard deviations.
  - Implied higher risk for bugs in algorithms due to more code to deal with several cases.
  - Work flows that appear to be working may actually yield incorrect results, even if they are constructed from algorithms that are correct when run individually.
- Ultimate goal: Remove those ambiguities in our data types.

Clearly this cannot be done any time soon, since not only the data structures (including the workspace hierarchy) need fixing, but all of our algorithms.
This document presents a first step that solves some of the issues, increases safety, and paves the way for future changes that bring us closer to the ultimate goal.

## Uncertainties

We start the discussion with the uncertainties (`E`).
In this case a simple internal change can fix the current ambiguity.
The effect is local in all cases and will be invisible on the API level and to the user.
This is thus not part of the design proposal, but due to the similarities we discuss it here as well.
Experience gained during refactoring `E` can be used to potentially uncover problems overlooked in the design for `Y`.

### Status

- Typically, `E` stores the standard deviation.
- For computations such as adding data, the variance is required, thus `E` is squared and converted back to standard deviation by taking the `sqrt` at a later points.
  Often this is done in-place, i.e., `E` temporarily stores the variance.
- In a few cases `E` is kept as a variance until just before the end of an algorithm for performance reasons.
  For example, `DiffractionFocussing2` needs to summing many spectra.
  To avoid repeated evaluation of the expensive `sqrt` function for the target spectrum, all spectra are added without converting back to standard deviation after every addition.
  `DiffractionFocusing2` calls `Kernel::VectorHelper::rebinHistogram()` where calculations between input and output E `vector` are performed in terms of variance.
  This also happens in `Kernel::VectorHelper::rebin()`.

### Discussion

For `E` data, the modification of the storage mode is typically very local and a fix should be rather easy.

- `Histogram` currently provides functions for obtaining variances as well as standard deviations, e.g., `countVariances()` and `countStandardDeviations()`.
  If the internal `E` vector were converted to variances by external means (as it is done currently), these access methods would do the wrong thing.
  For example, `countVariances()` assumes that the internal `E` vector stores standard deviations.
  If this is not the case due to an external conversion of this `E` vector to variances, `countVariances()` will still return the square of the `E` vector, i.e., the *square* of the variances.

- `HistogramData` provides means for converting between standard deviations and variances, in particular types that do the conversion automatically.
  These should be used by client code.

- If summing spectra were done using `Histogram::operator+()`, propagating the uncertainties would involve a `sqrt` computation for every `+` operation.
  In the example of `DiffractionFocussing2` this could yield a significant overhead, and it is not obvious how to solve this:

  - The algorithm could do the summing itself, summing `Y` and variances separately.
    This would cause no performance loss, and the code would be reasonably clean, e.g.,

    ```cpp
    for (size_t i=0; i<inputWS.getNumberHistograms(); ++i) {
      counts += inputWS.counts(i);
      variances += inputWS.countVariances(i);
    }
    ```

  - We could provide optimized means for summing many spectra as part of the `HistogramData` module.
    For example,

    ```cpp
    namespace HistogramData {
    Histogram sumHistograms(const std::vector<Histogram> &histograms);
    }
    ```

    This would be a clean solution without performance loss.
    Unfortunately, there will be an implicit performance and ressource issue if the input is an `EventWorkspace`.
    Obtaining a `Histogram` from the input workspace will create the `Y` and `E` data on the fly (this needs to be done in any solution).
    However, to create the vector of histograms as input for `sumHistograms()` we need to **store all histograms at the same time**.
    This will increase memory consumption and reduce cache locality of the computation.

  - `DiffractionFocussing2` also needs to rebin each spectrum and thus the `sqrt` cost may turn out to be irrelevant.
    There are only very few examples where the `sqrt` computation is postponed for performance reasons, so it might be less relevant to provide an direct solution for this.

  - This discussion highlights something important: If clients do not understand the storage mode used in `Histogram`, they may be making inefficient use of its interface.
    For example, `operator+()` for `Histogram` will not necessarily be the ideal (fastest) solution in some cases, so adding things like this to the interface will always be slightly ambivalent.

- Completely removing the direct access from the API (`e()` and `sharedE()` and the respective mutable variants) is not realistic.
  With direct access it is impossible to enforce (on a technical level) that `E` always stores standard deviations.
  This is also related to the similar issue for `Y`, since `E` may represent uncertainties of `Counts` or `Frequencies`.

In conclusion:

- `E` should always store standard deviations, never variances or anything else.
  Storing always variances could be a performance advantage, but the required amount of changes is too big to do this at the current point.
- We cannot realistically enforce this at a technical level.
  Providing a good interface to `Histogram` and a set of functions for dealing with uncertainties that covers most common cases will discourage developers from storing variances.
  Furthermore, a clear documentation and code review should be able to help catch violations.
- All code that currently stores anything but standard deviations as `E` in a histogram or workspace will be refactored.
- `Histogram` data will be extended with methods for manipulating standard deviations to eliminate the need for externally dealing with variances.


## Count and frequency data

### Status

- Data in `Workspace2D` be represent counts or frequencies.
- Conversions between the two are done with the algorithms `ConvertToDistribution` and `ConvertFromDistribution`, or the helper function `WorkspaceHelpers::makeDistribution()`.
- `MatrixWorkspace::isDistribution()` can be used for checking the state, and `MatrixWorkspace::setDistribution()` for setting the corresponding flag (note that this does not actually transform the data).
- There is a validator that verifies the state of a workspace, `RawCountValidator`, however it is used by relatively few algorithms.
- A considerable number of algorithms use `MatrixWorkspace::isDistribution()` to adapt their behavior, in most cases this adaption is a simple conversion to the desired data storage type.
- For a large number of algorithms there are no checks, and it is not documented whether or not they work only with counts, only with frequencies, or both.
- The `MatrixWorkspace::isDistribution()` flag is just a flag on the workspace.
  It could in principle lie, and there is currently no guarantee that all histograms in a workspace have the same state.

### Discussion

Parts of the problem under discussion is related to the fact that `Histogram` provides direct access to the underlying data.
This is currently required for three reasons:

- In-place modifications. Using the new interface, `Histogram::counts()` followed by `Histogram::setCounts()`, this is not possible, since we return a COW object by value, so modification will trigger a copy, making in-place modifications of workspaces inefficient.
- Some client code does not care if it works with `Counts` or `Frequencies`, so we cannot force it to use either of those.
  Examples include `ExtractSpectra` or other algorithms that simply chop off bits at the ends of the histogram and also `ConvertUnits` does not care in many cases.
- We currently have places where data is converted between various storage modes, so for now client code cannot always rely on `counts()` and `frequencies()` to return what they need.

We will solve the last point and at least parts of the second point if we come to a good solution for what is being discussed here.

Removing direct access to the underlying data, or rather removing direct type-agnostic access such as `Histogram::y()`, would ultimately solve this problem.
This would be an absolutely massive effort and would also require an improved workspace hierarchy.
Realistically, in my opinion, we can do that only by moving a lot of functionality into the `HistogramData` scope (or a new module for `Histogram` operations).
Basically most algorithms perform a per-histogram operation.
These operations could be extracted from the algorithm code and moved into a histogram module.
The algorithms themselves would then only perform operations with histograms, not with the X, Y, and E data:
1. Most algorithms should operate at the Histogram level.
2. Code relating to the internal manipulation of histograms should be migrated into the `HistogramData` scope
3. Access to aspects of the Histograms should be increasingly qualified. `X`, `Y`, `E` are internal.
4. We should aim to make these improvements as part of a longer programme of work.

This is again a massive effort, but it can easily done step by step over a longer period. That way we will eventually get to the point where the direct access interface is used little.

As an intermediate step that solves parts of our problems and paves the way for changes suggested in the previous paragraph, we must remove the ambiguity of what `Y` represents, counts or frequencies.
In contrast to the discussion regarding `E`, there are additional difficulties:
1. The difference between counts and frequencies is exposed on the API level, workspaces can be *histogram-data* or *distribution-data*.
2. If the histogram stores *point-data*, i.e., not bin edges, the conversion from frequencies to counts is not reversible without a loss in precision.
  To compute frequencies from counts, we need the bin widths, which in turn are not uniquely determined by points, since there is one degree of freedom too many.





If we permit storing either counts or frequencies...

1. **Current solution**:
   - Data in `Histogram` can be in two states counts or frequencies, but the histogram does not know its state.
   - `Histogram::counts()` and `Histogram::frequencies()` will thus not return the correct thing if the workspace stores distribution data.
   - `Histogram::y()` references data that has no fixed interpretation that client code can rely on.

2. **Switchable Y-storage mode with direct Y access**
   - `Histogram` can be in two states `YMode::Counts` and `YMode::Frequencies`.
   - `Histogram::counts()` and `Histogram::frequencies()` will always be able to return the correct thing.
   - However, `Histogram::y()` will reference data that has no fixed interpretation that client code can rely on.
   - To make this option work, we would thus need to refactor all client code to either use the `counts()`/`frequencies()` interface, or check the storage mode before using `y()`.
   - Effort: **major**
   - Benefit: **small - medium** (not safe but versatile, we can store any data we may need)
   - Safety: **small - medium** (after a global refactoring this would be safe, but we have no way of forcing client code to check storage mode before using `y()`)

3. **Switchable Y-storage mode without direct Y access**
   - `Histogram` can be in two states `YMode::Counts` and `YMode::Frequencies`.
   - `Histogram::counts()` and `Histogram::frequencies()` will always be able to return the correct thing.
   - However, `Histogram::y()` would reference data that has no fixed interpretation that client code can rely on.
   - We could thus remove this part of the interface and refactor all client code to use the `counts()`/`frequencies()` interface.
   - Effort: **major**
   - Benefit: **medium - high** (safe and versatile, we can store any data we may need)
   - Safety: **high** (cannot misinterpret data, but it would be possible to run any algorithm on any type of data even if that would not make sense)

4. **Fixed Y-storage mode (counts)**
   - `Histogram` has only a single state and always stores counts.
   - It will always be guaranteed that `Histogram::counts()` and `Histogram::frequencies()` return the correct thing, and client code can rely on `Histogram::y()` returning a reference to a vector of counts.
   - What about data that has no underlying counts, for example a function defined at certain points?
     It would basically be converted into fake counts, based on a potentially lossy conversion of `Points` to `BinEdges`.
     Maybe we need a new workspace type for this?
   - Effort: **medium**
   - Benefit: **medium** (safe but not versatile, we can only store counts and need workarounds for non-count data)
   - Safety: **medium - high** (medium if we use `Histogram` to also store distribution data, converted to counts)

All of these options seem a bit awkward.
This is also related to the fact that we can convert between `Points` and `BinEdges`.
Do we need to fix that as well?
Would it make sense to reduce this to a 3-state system, instead of having independent `XMode` and `YMode`, we would have `StorageMode::CountBins`, `StorageMode::FrequencyBins`, and `StorageMode::Points`, the latter implying that the data represents frequencies?



In the case of the `Y` data, removing the ambiguity of storage mode would effectively
- Get rid of the concept *distribution data*.
- All data in `MatrixWorkspace` and `Histogram` is stores as `Counts`.
-


The different interpretations of `Y` data effectively breaks the promises that the `Histogram` interface makes:

- If we allow converting the internal `Y` data between counts and frequencies by clients, `Histogram::counts()` and `Histogram::frequencies()` will not return what their name implies

- `RawCountValidator` can this be removed?

- Saving data, e.g., `SEQUOIAreduction.py`, need to be able to save distribution data.

- `FitMW` has flag to normalize, but does so only if input is histogram data. Ignores `isDistribution()`? But it seems to be inaccessible and is always off?

- `MatrixWorkspace::isDistribution()` example `CreatePSDBleedMask` needs distribution and manually converts

- binary operations, should it implicitly convert? e.g., `Divide` or `Multiply` may not make sense for `Counts`.

- `Integration` always computes the integral of the counts, not the frequencies, even if the workspace stores distribution data.

- Need to be able to load legacy files, in particular `LoadNexusProcessed`.

- `MatrixWorkspace::YUnitLabel()` extra label for distribution?

- `FractionalRebinning` and `RebinnedOutput` workspace?

- How do we deal with point-distribution data? storing counts will be lossy (see maybe `IQTransform`).
  Can store an extra helper value in case the `Histogram` is created from `Points` and `Frequencies`.

  ```cpp
  class Histogram {
  private:
    double m_firstBinEdge = NAN; // not defined in many cases
  };

  Histogram::Histogram(const Points &points, const Frequencies &frequencies) {
    m_x = points.cowData();
    auto edges = BinEdges(points);
    m_y = Counts(edges, frequencies).cowData();
    m_firstBinEdges = edges[0];
  }

  Frequencies Histogram::frequencies() {
    if(xMode == XMode::BinEdges) {
      // ...
    } else {
      auto edges = BinEdges(Points(m_x), m_firstBinEdge);
      return Frequencies(edges, Counts(m_y));
    }
  }

  BinEdges::BinEdges(const Points &points, double firstBinEdge) {
    if (std::isnan(firstBinEdge) {
      // compute edges as midpoints between points
    } else {
      // compute edges such that points are midpoints between edges
    }
  }
  ```

  Note that there is one problem with this mechanism:
If the points are modified after creation of the histogram the value of `m_firstBinEdges` may become outdated.




### Data visualization

#### Plotting

- It must be possible to plot either counts or frequencies

`QwtWorkspaceSpectrumData` checks `MatrixWorkspace::isDistribution()`

#### Table View

If we do no longer store data as frequencies, it should still be possible to display the data in a histogram as frequencies.
This could be done via a simple change in the table view, options are:

1. Provide a way to toggle `Y` between counts and frequencies
2. Replace `Y` by two columns, `Counts` and `Frequencies` (indicating that the latter is simply computed based on `Counts`, maybe via a tool tip).


### Fitting

- Do we ever want to fit counts?
- If yes, we need to be able to select what `Fit` does.

