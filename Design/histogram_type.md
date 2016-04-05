# Histogram Data Type

**Note:** This document is mainly concerned with a data type for a *generic* histogram.
In the context considered here, a histogram is *not* specific to neutron science and probably not even specific to physics.
In particular it should not be confused with the current data types in Mantid that are joint containers for histogram data and spectrum/detector information, such as `ISpectrum` and `Histogram1D`.


## Motivation

One of the most fundamental concepts of ubiquitous use in Mantid is that of histograms of (event) data.
Despite this, there is currently no data type in Mantid that deals with histogram data.
The purpose of this design proposal is to fix this.

There are various motivations for this:

- Reduce code duplication by providing arithmetic operations such as addition of histograms.
- Hide handling of errors (uncertainties).
- Hide discrimination between histogram and distribution data.
- Decrease risk for certain types of bugs by using the C++ type system.

All this would remove duplicated code from the client and put it into a central place where it can be unit-tested.


## Current situation

The current way of dealing with histograms has various shortcomings.
Basically we have a set of four `std::vector<double>`, for `X`, `deltaX`, `Y`, and `E`.
There is a single `typedef` `MantidVec` used for all four of them (and other data), and this is probably adding only more confusion.

The problems include:

- No type safety:
  - The bug in `ConvertUnits` creped in because we are currently using the same instance of a single type for both histogram data and distribution data. The actual meaning of a vector of `Y` values is basically kept as a mental flag in the brain of a Mantid developer.
  - We are using a single type for `X`, `Y`, and `E`. It is thus easy to accidentally mix them up.
  - The array `E` of error values is used for both the variance and the standard deviation. The state is again carried as a flag in the brain of a developer. We even have functions such as `rebin` that return an array of `E` values that may mean either variance or standard deviation depending on a flag to the function!
- Code duplication: Re-implementing the same thing 10 times is wasteful and error prone.
  - Propagation of errors. Currently arithmetics with two histograms requires manually keeping track of the errors.
  - Conversions between variance and standard deviation.
  - Many simple operations on histograms occur frequently.
    - assignment
    - set to zero
    - arithmetics with other vectors, including `+`, `+=`, etc.
    - arithmetics with a scalar, e.g., adding a constant to the bin-edge vector or the bin values
    - comparison (`==`)
    - integration
    - rebinning
    - reverse order (maybe just part of other operations)
    - apply function to values (similar to `std::transform`)
    - truncate head or tail
    - get lambda (i.e., compute bin centers)
- Dealing with different cases of data representation. For example, many algorithms require point data. Currently we have manual checks for `isHistogramData` and subsequent conversions to point data scattered throughout our code.
- Unit testing: Implementation of operations on histogram are currently mixed into algorithm code. Unit tests thus need to test two things at the same time.
  - Many units tests of algorithms do not fully test the range of errors that can happen when, e.g., adding two spectra. Doing so would be very hard in the current de-centralized implementation,
  - Many algorithms need to modify the errors. In some algorithms the unit tests cover the errors, in others they do not.


## Design goals

- Provide simple arithmetic operations for histograms.
  - Arithmetic operations automatically deal with propagation of errors.
- Hide differences between histogram and distribution data, as well as between histogram and point data.
  - Internal storage type could be either, does not need to be known at the interface level?
  - Arithmetic operations should do the right thing for any data type automatically, as far as possible.
- Hide error handling.
  - For simple operations with histograms, algorithm authors should not need to know how to propagate errors.
- Enable unit testing of key concepts in Mantid.
  - Arithmetic operations with histograms.
  - Propagation of errors.
- Enforce type safety.
- Do not compromise on speed.



## Implementation

#### Basics

The basic concept seems simple enough:

- Add one class for a histogram with an interface that provides standard operations for histogram data and point data.
  - Note that we do not introduce a separate type for histogram and distribution data. This distinction would be only internal, and access to either histogram or distribution data is provided via public interface methods. The goal is to eliminate this distinction from as much of the code as possible.
  - For histogram and point data the argument is not so clear. It is not possible to do a unique conversion from point data to histogram data, so the internal storage type is not arbitrary here, and conversion are lossy. Nevertheless, considering how many of our current algorithms deal with both types of data in the same way, it is probably a good idea to also keep both histogram and point data in the same type. The interface will have to reflect the internal differences in this case and cannot be symmetric as in the distribution-data case.
- Add a few classes for `X`, `Y`, and `E` (etc.) that would mainly be used internally in the histogram class and for direct access to the underlying data.

#### Examples

Before going into further details it is best to have a look at the envisioned end result.

We introduce types for all the different interpretations of a `std::vector<double>` in this context.
The new types would be simple wrappers around `std::vector<double>` (or rather `Kernel::cow_ptr<std::vector<double>>`), and add a suitable interface to it.
In particular:

1. X-data: We need to cover two cases and introduce two types: `BinEdges` and `Points`.
2. Y-data: We need to cover two cases and introduce two types: `Counts` and `Frequencies`.
3. Errors: All four types introduced by 1. and 2. can come with uncertainties.
   They can be represented as variances or standard deviations.
   We thus introduce 8 types: `BinEdgeVariances`, `BinEdgeStandardDeviations`, `PointVariances`, `PointStandardDeviations`, `CountVariances`, `CountStandardDeviation`, `FrequencyVariances`, `FrequencyStandardDeviations`.

The amount of new types introduced may seem appalling at first, but we usually do not have to deal with many of them:

1. For 'standard' operations you do not need to work with the low-level types, but can use the interface of `Histogram`, e.g.,

   ```cpp
   Histogram hist1;
   Histogram hist2;
   // Initialize histograms
   // ...
   // Adding histograms can automatically add `Y`, and propagates the errors properly
   auto result = hist1 + hist2;
   ```

   Details of the `Histogram` interface are still open, but it should be simple to extend it once the roll-out is done.

2. `BinEdges` is convertible to `Points`. We can thus avoid the currently prevalent way of dealing with this:

   ```cpp
   // Old:
   const bool isHistogram = ws->isHistogramData();
   for (size_t i = 0; i < Y.size(); ++i) {
     x = isHistogram ? (0.5 * (X[i] + X[i + 1])) : X[i];
     // use x
   }
   
   // New: If you need points, not bin-edges, just read them, Histogram can convert
   const auto &points = histogram.points();
   for (size_t i = 0; i < Y.size(); ++i) {
     // use points[i]
   }
   ```

   The reverse conversion is of course not unique, so we will still have algorithms that refuse to work with histograms that store point data.

3. `Counts` and `Frequencies` can be converted into each other (internally in the `Histogram` type).
   When implementing an algorithm you can thus simply choose which representation you prefer to work with, e.g.,

   ```cpp
   Counts counts { 16, 56758, 34, 0 };
   histogram.setCounts(counts);
   //...
   // We set counts, but can read frequencies somewhere else
   const auto &frequencies = histogram.frequencies();
   // Errors are dealt with implicitly unless specified otherwise
   const auto &errors = histogram.countStandardDeviations();
   // errors[0] should now be 4
   ```

4. As shown in the previous example, in many cases you do not have to deal with errors yourself.
   As long as the standard deviation is simply the square root of the counts it will be computed and propagated under the hood.

5. `Variances` and `StandardDeviations` can be automatically converted, you do not have to deal with it yourself.


#### Details

- The different low-level types have been introduced in the previous section.
  To avoid highly duplicate code and tests, such as for the four `Variance` types, these are implemented using the curiously recurring template pattern (CRTP) which provides something like "mixins".
- Jon pointed out that it may make most sense to default to storing data as `Frequecies`, as OpenGenie did by default.
  Many operations could probably done in this representation, and furthermore the conversion to `Counts` is cheaper, since it includes a multiplication instead of addition.
- The current copy-on-write (COW) mechanism seems useful and should be preserved.
  - The `typedef` `MantidVecPtr` for a `cow_ptr` is useless and confusing and should be removed.
  - We should consider extending the COW mechanism and make sure sharing is preserved more than it is now. For example, what can we do to maintain sharing of `X` for all histograms in a workspace where `X` is modified in an identical way? The COW mechanism as it is now should break down in that case. Probably this needs to be handled at the workspace/algorithm level, and cannot be dealt with this here? Having parametric `X` could circumvent that in certain cases (see outlook).

#### Interface

- The interface of `Histogram` can be (partially) forwarded by `ISpectrum` and `MatrixWorkspace`, similarly to how it is implemented currently for, e.g., `ISpectrum::dataX` and `MatrixWorkspace::dataX`.

- The main challenge in the design of the `Histogram` interface is the way how we deal with references.
  If the internal data storage mode of, say, the Y-data is not known, it is not trivial to provide `Counts &counts()` (as a partial equivalent to the current `std::vector<double> &dataY()`), since there may be nothing to reference to.
  - One way of dealing with this is a conversion of the underlying type on write, e.g.,

    ```cpp
    // Default storage mode is `Frequencies`.
    Histogram hist;
    // Const accessors return by value:
    // const Counts Histogram::constCounts() const;
    const auto &counts = hist.constCounts();
    // Non-const accessors return by reference and converts internal storage mode:
    // Counts &Histogram::counts();
    auto &writableCounts = hist.counts();
    // modify writableCounts
    ```

  - Alternatively, we could eliminate the option of getting non-const references, and instead do everything via setters, e.g.,

    ```cpp
    // Default storage mode is `Frequencies`.
    Histogram hist;
    // Const accessors return by value (there is no non-const overload):
    // Counts Histogram::counts() const;
    auto counts = hist.counts();
    // modify counts
    hist.setCounts(counts);
    ```

  Both options involve some overhead when writing (in the former case we can move the underlying `std::vector<double>` from `Frequencies` to `Counts`, in the latter case we allocate memory for the temporary `Counts` object).

  It is not entirely clear how we would deal with the similar situation in the `BinEdges` vs. `Points` case, where a conversion is not lossless and should thus not be done automatically in the generic case.

  Further thoughts and ideas for this would be really welcome!

- Not all cases for operations with histograms will be covered by the histogram type or free functions for histograms.
  Therefore we need to provide a direct interface to the underlying data as well.

- If we want to hide things like error handling, is there a decent way of making this extensible for new operations? Are operators/functions declared as `friend` in our histogram data type? Are they members? Can we allow the use of `std::transform` on, e.g., the `Y` data? How to transform errors?


## Roll-out

Since histograms are in widespread use in the Mantid code the introduction of the new data type and in particular the new interfaces is not trivial.

The main problem is that there is currently no way of telling how the data in an `ISpectrum` should be interpreted.
There are flags on `MatrixWorkspace` that indicate the state of the `X` and `Y` data, however,

- The flags are not always in the correct state.
- There is no flag that indicates whether errors are stored as variances or standard deviations
- For spectra outside a workspace we have no flag at all.

These problems are indicators for the key issue that this design attempts to fix, so we have no choice and have to deal with this hurdle. To cut the changes into slightly small bits:
Start changing only one of `X`, `Y`, or `E`, I take `X` as an example here:

1. Add a flag `enum class XDataMode { BinEdges, Points }` to `ISpectrum` and make sure it is set properly everywhere.
2. - remove `ISpectrum::refX` (type `cow_ptr<std::vector<double>>`)
   - add `ISpectrum::binEdges` (type `BinEdges`)
   - add `ISpectrum::points` (type `Points`)
   - modify implementation of old interface to forwards to `binEdges::data()` or `points::data()` depending on flag
   - changing flag converts data
3. Add new interface to `ISpectrum`.
   To make use of the new capabilities of the histogram type, the interface of `MatrixWorkspace` and `ISpectrum` could be extended to return a reference to the underlying histogram (once the transition is done for all sub-types).

Step 1 is the hardest part to get right.
We slightly chunk up the work by doing this only for `X`, and not introducing the full `Histogram` type in a single step.

After these initial steps we can then continuously work on reducing the use of the old interface in old and new algorithms.
After a while we should be in a position to decide whether we want to keep the old interface around, or remove it completely.
Furthermore, we will be able to decide whether or not we provide direct access to the underlying `X`, `Y`, and `E` data for non-standard operations.
This direct access would not be identical to the current one, since it would rely on the new types for these data structures.


## Python interface

- There should be no major difficulties providing a Python interface.
- Would it be useful to have the interface for a stand-alone `Histogram` even before the roll out to the C++ parts of Mantid is done?


## Outlook

The proposed encapsulation of histogram data opens the door for improvements that may be worth considering in the future:

- Abstraction of error handling may lead to improvements that are currently hard to implement, such as dealing with non-Gaussian errors or taking into account correlation between data.
- If errors are just the square root of the counts the implementation may choose to not carry them explicitly to save computation time and memory.
- Bin sizes could in some cases be defined in a parametric way, without keeping bin boundaries around explicitly. This could safe memory, memory bandwidth, and cache space.
