# Replacing legacy access to Histograms

Apart from 1:1 replacements (such as `readX -> x` or `dataX -> mutableX`), pay special attention to the following:

- There are `consts` variants of `dataX`, `dataY`, and `dataE`, so there are cases where they should be replaced by `x`, `y`, and `e` instead of the "mutable" variants.
- Sometimes the non-`const` variants of `dataX`, `dataY`, and `dataE` are misused, i.e., used in cases where data is not actually modified.
  It is important to find these cases and replace them by `x`, `y`, and `e`, since otherwise a copy of the data is forced (internal sharing is broken).
- It is now easy to "share" also Y and E data.
  In the old interface you will have been familiar with this for X (using `refX`, `ptrX`, and `setX`).
  Whenever you encounter a plain copy of Y and E data, such as

  ```cpp
   outWS->dataY(i) = inWS->readY(i);
  ```

  replace it with

  ```cpp
   outWS->setSharedY(i, inWS->sharedY(i));
   // Share the whole Histogram
   outWS->setHistogram(i, inWS->histogram(i));
  ```

- Improving sharing is the (only) main reason for improved performance by using functionality from the new `HistogramData` module.
  We want to track these improvements, please keep track of the algorithms where you did such improvements, implement a performance tests (or manually test it, e.g., my adapting a doctest) and give the results in the pull request.
- If in doubt, create a pull request for an early/intermediate code review by one of the team members that has already done more work with these refactorign steps.
  In particular, do this before putting effort into writing performance tests.
- Replace uses of `std::vector<double>` (`MantidVec`) in function arguments by the new types for improved type-safety.
- **Keep pull request small, in particular is this is your first contact with `HistogramData`.**

There are a few new features of `HistogramData` that are not yet described in the [transistion document](http://docs.mantidproject.org/nightly/concepts/HistogramData.html):

#### Arithmetic operators:

- `+`, `-`, `*`, and `/` with `double` argument for Y and E types.
- `=` with `double` argument for Y and E types.
- `*` and `/` with `double` argument for `Histogram`
- `+`, `-`, `*`, and `/` with `double` argument for two `Histograms`.
- Where applicable, also the corresponding `+=` operators (etc.) have been added.

The operators for the individual (Y and E) types are included by default.
Operators for `Histogram` are available in `MantidHistogramData/HistogramMath.h`.

#### Generators (useful in particular for many unit tests):

```cpp
#include "MantidHistogramData/LinearGenerator.h"
#include "MantidHistogramData/LogarithmicGenerator.h"
using namespace HistogramData;

size_t count = 5;
double start = 1.0;
double increment = 0.1;
BinEdges edges(count, LinearGenerator(start, increment));
// edges = { 1.0, 1.1, 1.2, 1.3, 1.4 }

// Similar for LogarithmicGenerator
```
