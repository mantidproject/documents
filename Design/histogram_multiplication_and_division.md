# Multiplication and Division Rules for Histograms

#### Motivation

- We need to define and provide correct and consistent math operations for Histograms.
- We need to fix existing issues with binary operations for `MatrixWorkspace`, see, e.g., [#15624](https://github.com/mantidproject/mantid/issues/15624).

#### Definitions

- **Distribution data** is smooth and has no jumps.
  This is still valid after rebinning to any bin size.
  Distribution data gives the probability (per unit on the X axis) for measuring a specific value.
- **Histogram data** can be obtained from distribution data by multiplying by the bin width.
  If the bin width is not constant, histogram data will have discontinuities (jumps).
  Histogram data gives the probability integrated over a bin.

#### Derivation of multiplication and division of histogram and distribution data

- Define the function `d()` as dividing data by the bins widths , i.e., applying `d()` to histogram data corresponds to `ConvertToDistribution`.
- Define `h()` as the inverse of `d()`, i.e., applying `h()` to distribution data corresponds to `ConvertFromDistribution`.

Starting with an example:

- Set bin widths `{1,1,2}`.
- Assume the number of measured counts per TOF unit is constant, and we have two measurements, a and b.
  We let the prefix `H` and `D` denote histogram data and distribution data, respectively:

  ```cpp
  Ha = {1,1,2}
  Hb = {2,2,4}
  Da = d(Ha) = {1,1,1}
  Db = d(Hb) = {2,2,2}
  ```
- Dividing the two measurements yields

  ```cpp
  Hb/Ha = {2,2,2} = Db/Ba = Dc
  ```
  The result is distribution data and thus does not have jumps.

By reordering above equation we obtain several rules for multiplication and division (omitting suffixes `a`, `b`, and `c`):

```cpp
H/H = D
D/D = D
D*D = D
H*D = H
H/D = H
D/H = 1/H // neither histogram nor distribution!
```

The final missing combination is

```cpp
Ha*Hb = {2,2,8}
d(Ha*Hb) = {2,2,4}
d(d(Ha*Hb)) = {2,2,2} // two steps from distribution
H*H = H^2 // neither histogram nor distribution!
```

We see that there are two operations that produce results that are neither histogram nor distribution.
A closer look shows that "histogram" and "distribution" are just two steps in an infinite ladder of states:

```cpp
 |
1/H
 |
 D // distribution
 |
 H // histogram
 |
H^2
 |
```

- Applying `d()` takes us one step up, applying `h()` takes us one state down.
- Multiplying or dividing by `D`-data stays on the same step.
- Multiplying by `H`-data takes us one step down.
- Dividing by `H`-data takes us one step up

Mantid supports only `H`-data and `D`-data, and in fact any of the other states does not seem to have a meaningful use.
As a consequence **any operation that takes us above `D` or below `H` must be forbidden**.

#### Conclusion

- `operator*` and `operator/` for `Histogram` should be implemented according to these results.
- The algorithms `Multiply` and `Divide` should be fixed.

Results are summarized in the following table:

| In 1 | In 2 | Op | Allowed | Result |
|:-:|:-:|:-:|:-:|:-:|
| H | H | * | no  | - |
| H | D | * | yes | H |
| D | D | * | yes | D |
| H | H | / | yes | D |
| H | D | / | yes | H |
| D | H | / | no  | - |
| D | D | / | yes | D |
