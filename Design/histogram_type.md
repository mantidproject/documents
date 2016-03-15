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
Basically we have a set of three `std::vector<double>`, for `X`, `Y`, and `E`.
There is a single `typedef` `MantidVec` used for all three of them (and other data), and this is probably adding only more confusion.

The problems include:

- No type safety:
  - The bug in `ConvertUnits` creped in because we are currently using the same instance of a single type for both histogram data and distribution data. The actual meaning of a vector of `Y` values is basically kept as a mental flag in the brain of a Mantid developer.
  - We are using a single type for `X`, `Y`, and `E`. It is thus easy to accidentally mix them up.
  - The array `E` of error values is used for both the variance and the standard deviation. The state is again carried as a flag in the brain of a developer. We even have functions such as `rebin` that return an array of `E` values that may mean either variance or standard deviation depending on a flag to the function!
- Code duplication: Re-implementing the same thing 10 times is wasteful and error prone.
  - Operations like adding histograms are frequent.
  - Propagation of errors.
  - Conversions between variance and standard deviation.
- Unit testing: Implementation of operations on histogram are currently mixed into algorithm code. Unit tests thus need to test two things at the same time.
  - Many units tests of algorithms do not fully test the range of errors that can happen when, e.g., adding two spectra. Doing so would be very hard in the current de-centralized implementation,
  - Many algorithms need to modify the errors. In some algorithms the unit tests cover the errors, in others they do not.


## Design goals

- Provide simple arithmetic operations for histograms.
  - Arithmetic operations automatically deal with propagation of errors.
- Hide differences between histogram and distribution data.
  - Internal storage type could be either, does not need to be known at the interface level?
  - Arithmetic operations should do the right thing for any data type automatically.
- Hide error handling.
  - For simple operations with histograms algorithm authors should not need to know how to propagate errors.
- Enable unit testing of key concepts in Mantid.
  - Arithmetic operations with histograms.
  - Propagation of errors.



## Implementation

#### Basics

The details of the implementation have not been worked out yet.
The basic concept seems simple enough:

- Add one class for a histogram with an interface that provides standard operations for histogram data.
  - Note that we do not introduce a separate type for histogram and distribution data. This distinction would be only internal, and access to either histogram or distribution data is provided via public interface methods. The goal is to eliminate this distinction from as much of the code as possible.
- Add a few classes for `X`, `Y`, and `E` (etc.) that would mainly be used internally in the histogram class and for direct access to the underlying data. If these inherit from `std::vetor<double>`, they could also be used to keep the legacy interface for `ISpectrum` alive until the roll-out is complete.

#### Details

- It is probably useful to introduce two types for vectors of standard deviation and variance, instead of the current double use of `E`.
- Similarly we should have distinct internal types for histogram and distribution data, in case our implementation relies on this distinction. Jon pointed out that it may make most sense to default to distribution data, as OpenGenie did by default.
- The current copy-on-write (COW) mechanism seems useful and should be preserved.
  - The `typedef` `MantidVecPtr` for a `cow_ptr` is useless and confusing and should be removed.
  - We should consider extending the COW mechanism and make sure sharing is preserved more than it is now. For example, what can we do to maintain sharing of `X` for all histograms in a workspace where `X` is modified in an identical way? The COW mechanism as it is now should break down in that case. Does it need to be handled at the workspace level, or can we deal with this here? Having parametric `X` could circumvent that in certain cases (see outlook).

#### Interface

- At least initially not all cases for operations with histograms will be covered by the histogram type or free functions for histograms. Therefore we probably need to provide a direct interface to the underlying data as well.
- If we want to hide things like error handling, is there a decent way of making this extensible for new operations? Are operators/functions declared as `friend` in our histogram data type? Are they members? Can we allow the use of `std::transform` on, e.g., the `Y` data? How to transform errors?


## Roll-out

Since histograms are in widespread use in the Mantid code the introduction of the new data type is not trivial.
However, we can probably adopt a step-by-step approach that makes the roll-out quite feasible:

- The new histogram data type is typically encapsulated in an `ISpectrum` object.
  - Currently the `X` data is part of `ISpectrum`, whereas `Y` and `E` are part of `Histogram1D`. We somehow have to change this, or provide the option to have a histogram without `Y` and `E` data. This may be the main difficulty of these first steps.
  - The interface of `ISpectrum` could be kept unchanged at first. The data access functions would then forward to the internal `X`, `Y`, and `E` data inside the new histogram type.
- The interface of `MatrixWorkspace` would continue to forward to the interface of `ISpectrum`.
- To make use of the new capabilities of the histogram type, the interface of `MatrixWorkspace` and `ISpectrum` could be extended to return a reference to the underlying histogram.

After these initial steps we can then continuously work on reducing the use of the old interface in old and new algorithms.
After a while we should be in a position to decide whether we want to keep the old interface around, or remove it completely.
Furthermore, we will be able to decide whether or not we provide direct access to the underlying `X`, `Y`, and `E` data for non-standard operations.
This direct access would not be identical to the current one, since it would rely on the new types for these data structures.


## Outlook

The proposed encapsulation of histogram data opens the door for improvements that may be worth considering in the future:

- Abstraction of error handling may lead to improvements that are currently hard to implement, such as dealing with non-Gaussian errors or taking into account correlation between data.
- If errors are just the square root of the counts the implementation may choose to not carry them explicitly to save computation time and memory.
- Bin sizes could in some cases be defined in a parametric way, without keeping bin boundaries around explicitly. This could safe memory, memory bandwidth, and cache space.
