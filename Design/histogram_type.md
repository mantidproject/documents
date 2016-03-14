# Histogram Data Type

**Note:** This document is mainly concerned with a data type for a *generic* histogram.
In the context considered here, a histogram is *not* specific to neutron science and probably not even specific to physics.
In particular it should not be confused with the current data types in Mantid that are containers for histogram data and spectrum/detector information, such as `ISpectrum` and `Histogram1D`.


## Motivation

One of the most fundamental concepts of ubiquitous use in Mantid is that of histograms of (event) data.
Despite this, there is currently no data type in Mantid that deals with histogram data.
The purpose of this design proposal is to fix this.

There are various motivations for this:
- Reduce code duplication by providing arithmetic operations such as addition of histograms.
- Hide error handling.
- Hide discrimination between histogram and distribution data.

This removes duplicated code from the client and moves it into a central place where it can be unit-tested.



Type safety
simle arithmettic ops
error handling
dis/count mess (ref ConvertUnits bug)


## Current situation

The current way of dealing with histograms has various shortcomings.
Basically we have a set of three `std::vector<double>`, for `X`, `Y`, and `E`.
There is a single `typedef MantidVec` used for all three of them (and other data), and this is probably adding only more confusion.

The problems include:

- No type safety:
  - The bug in `ConvertUnits` creped in because we are currently using the same data type for both histogram data and distribution data. The actual meaning of a vector of `Y` values is basically kept as a mental flag in the brain of a Mantid developer.
  - We are using the same data type for `X`, `Y`, and `E`. It is thus easy to accidentally mix them up.
  - The array `E` of error values is used for both the variance and the standard deviation. The state is again carried as a flag in the brain of a developer. We even have functions such as `rebin` that return an array of `E` values that may mean either variance or standard deviation depending on a flag to the function!
- Code duplication:
  - Operations like adding histograms are frequent. Re-implementing the same thing 10 times is error prone.
  - Propagation of errors.
  - Conversions between variance and standard deviation.
- Unit testing:
  - Many units tests of algorithms do not fully test the range of errors that can happen when, e.g., adding two spectra. Doing so would be very hard in the current de-centralized implementation,
  - Many algorithms need to modify the errors. In some algorithms the unit tests cover the errors, in others they do not.


## Design goals

- Provide simple arithmetic operations for histograms.
  - Arithmetic operations automatically deal with propagation of errors.
- Hide differences between histogram and distribution data.
  - Internal storage type of data could be either, does not need to be known at the interface level?
  - Arithmetic operations should do the right thing for any data type automatically.
- Hide error handling.
  - For simple operations with histograms algorithm authors should not need to know how to propagate errors.
  - Abstraction may lead to improvements that are currently hard to implement, such as dealing with non-Gaussian errors or taking into account correlation between data.
- Enable unit testing of key concepts in Mantid:
  - Arithmetic operations with histograms.
  - Propagation of errors.


If errors are just the square root of the counts the implementation may choose to not carry them explicitly to save computation time and memory.

Jon pointed out that it may make most sense to default to distribution data.

Bin sizes could in some cases be defined in a parametric way, without keeping bin boundaries around explicitly.

Do we need sub-types for `X`, `Y`, `E`, and `E-squared`? (and dist- data)?

What can we do to maintain sharing of `X` for all histograms in a workspace where `X` is modified in an identical way? The COW mechanism as it is now should break down in that case. Does it need to be handled at the workspace level, or can we deal with this here? Having parametric `X` would circumvent that case in certain cases.


## Implementation

The details of the implementation have not been worked out in detail.
The basic concept seems simple enough:

- One class for a histogram with an interface that provides standard operations for histogram data.
- Potentially a few classes for `X`, `Y`, and `E` (etc.) that would mainly be used internally in the histogram class. If these inherit from `std::vetor<double>`, they could also be used to keep the legacy interface for `ISpectrum` alive until the roll-out is complete.


## Interface

At least initially not all cases for operations with histograms will be covered by the histogram type or free functions for histograms.
Therefore we probably need to provide a direct interface to the underlying data as well.
One option would be to have sub-types for `X`, `Y`, and `E`, let them inherit from `std::vector<double>` and just add new interface functions.

If we want to hide things like error handling, is there a decent way of making this extensible for new operations? Are operators/functions declared as `friend` in our histogram data type? Are they members? Can we allow the use of `std::transform` on, e.g., the `Y` data? How to transform errors?

## Roll-out
