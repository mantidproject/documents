# Peak Refactoring

## Motivation
The `Peak` class is widely used throughout Mantid but there are some problems
with the current implementation that should be addressed:

 - Currently there are 6 constructors for a peak object which is looks very much
 like the telescoping constructor anti-pattern. This anti-pattern poses several
 problems:
     - They each have many parameters making it difficult to read.
     - It is difficult to even tell which constructor is being used.
     - Adding a new parameter requires adding a new constructor.

 - `Peak` recalculates some of its quantities on the fly. For example, after a
 `Peak` class is constructed if you call to `getQLabFrame` the value for `Qlab`
 is actually recalculated from other parameters. If you do this repeatedly you
 can run into a situation where your peak "moves".

 - The `Peak` class performs ray tracing depending on the constructor used or
 the order of parameters set on the `Peak` class. The key decision is whether or
 not the detector ID for a peak is set before the Q vector. Getting this wrong
 is easy to do and has been the source of bad performance in Mantid a couple of
 times already (specifically where many peaks are created at once such as in
 [PredictPeaks](https://github.com/mantidproject/mantid/issues/19131) and in
 [LoadNexusProcessed](https://github.com/mantidproject/mantid/issues/19522)).

 - Another problem is that `Peak` does not distinguish between the type of peak
 we're creating. For example a peak which was generated from a theortical
 information (for example from `PredictPeaks`) is not differentiated from a peak
 that was created from experimental data.

## Requirements

## Design

