# Y and E data storage modes

## Uncertainties

### Status

- Typically, `E` stores the standard deviation.
- For computations such as adding data, the variance is required, thus `E` is squared and converted back to standard deviation by taking the `sqrt` at a later points.
  Often this is done in-place, i.e., `E` temporarily stores the variance.
- In a few cases `E` is kept as a variance until just before the end of an algorithm for performance reasons.
  For example, `DiffractionFocussing2` needs to summing many spectra.
  To avoid repeated evaluation of the expensive `sqrt` function for the target spectrum, all spectra are added without converting back to standard deviation after every addition.

Notable examples include `Kernel::VectorHelper::rebin()` and `Kernel::VectorHelper::rebinHistogram()`.

### Discussion

For `E` data, the modification of the storage mode is typically very local and a fix should be rather easy.

- `Histogram` provides functions for obtaining variances as well as standard deviations, e.g., `countVariances()` and `countStandardDeviations()`.
  If the internal `E` vector were converted to variances by external means (as it is done currently), these access methods would do the wrong thing.

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
    Unfortunately, there will be an implicit performance and ressource issue if the input is an `EventWorkspace`!
    Obtaining a `Histogram` from the input workspace will create the `Y` and `E` data on the fly (this needs to be done in any solution).
    However, to create the vector of histograms as input for `sumHistograms()` we need to **store all histograms at the same time**.
    This will increase memory consumption and reduce cache locality of the computation.


## Count and frequency data

### Status

- Data in `Workspace2D` be represent counts or frequencies.
- Conversions between the two are done with the algorithms `ConvertToDistribution` and `ConvertFromDistribution`, or the helper function `WorkspaceHelpers::makeDistribution()`.
- `MatrixWorkspace::isDistribution()` can be used for checking the state, and `MatrixWorkspace::setDistribution()` for setting the corresponding flag (note that this does not actually transform the data!).
- There is a validator that verifies the state of a workspace, `RawCountValidator`, however is is used by relatively few algorithms.
- A considerable number of algorithms use `MatrixWorkspace::isDistribution()` to adapt their behavior, in most cases this adaption is a simple conversion to the desired data storage type.
- For a large number of algorithms there are no checks, and it is not documented whether or not the work only with counts, only with frequencies, or both.

### Discussion

If we permit storing either counts or frequencies

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
   - Safety: **small - medium** (we have no way of forcing client code to check storage mode before using `y()`)

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

The different interpretations of `Y` data effectively breaks the promises that the `Histogram` interface makes:

- If we allow converting the internal `Y` data between counts and frequencies by clients, `Histogram::counts()` and `Histogram::frequencies()` will not return what their name implies

- `RawCountValidator` can this be removed?

- Saving data, e.g., `SEQUOIAreduction.py`

- `FitMW` has flag to normalize, but does so only if input is histogram data. Ignores `isDistribution()`? But it seems to be inaccessible and is always off?

- `MatrixWorkspace::isDistribution()` example `CreatePSDBleedMask` needs distribution and manually converts

- binary operations


- `Integration` always computes the integral of the counts, not the frequencies, even if the workspace stores distribution data.

- Need to be able to load legacy files, in particular `LoadNexusProcessed`.

- `MatrixWorkspace::YUnitLabel()` extra label for distribution?

- `FractionalRebinning` and `RebinnedOutput` workspace?

- how do we deal with point-distribution data? storing counts will be lossy (see maybe `IQTransform`).

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


