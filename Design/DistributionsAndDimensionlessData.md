# An issue with distributions and dimensionless units

## Problem Description
Issue [#21106](https://github.com/mantidproject/mantid/issues/21106) in the Mantid project has exposed a deeper problem with our current definition of distributions and the `Divide` algorithm. The problem in that particular issue is that the algorithm requires counts (i.e. the raw data points unweighted by the bin width). In the code before the issue this was being accessed via `workspace->counts(i)`. This function will either directly return the counts or, if the workspace is a distribution, remove the bin width scale factor from the frequencies. This works entirely as expected in many cases.

The problem comes when the workspace passed to the algorithm is a distribution that has been created through a special case of the `Divide` algorithm. The `Divide` algorithm will force a workspace to be set to a distribution if the following condition is met:

```c++
// If the Y units match, then the output will be a distribution and will be
// dimensionless
else if (lhs->YUnit() == rhs->YUnit() && rhs->blocksize() > 1) {
    out->setYUnit("");
    out->setDistribution(true);
}
```

This means that if the Y units of the two operands are equal, i.e. dividing by these workspaces will produce a dimensionless *ratio*, the workspace will be marked as being a distribution. This is a problem because if at any point in the future the code tries to specifically access the counts contained in the workspace it will attempt to remove a bin width scale factor which was not present in the data!

In the specfic case of the bug report this causes an issue because the reduction workflow was loading two runs, one of a sample of interest and one of Vanadium and dividing the sample by Vanadium. This leads to the workspace having a dimensionless Y axis and being marked as a distribution. Subsequent calls to `->counts(i)` will yield an incorrect value. 

## Key issues

There are a several questions that need to be addressed here:

- Should we stop marking dimensionless workspaces created though `Divide` as distributions?
- Is the use of the empty Y unit name enough to indicate the a workspace is dimensionless?
    - What about the case when a user creates a workspace and does not specify a Y unit?
- The above code with yield a workspace that is a distribution but as has bin edges. Is this correct?
- Should data that is of raw counts be marked as dimensionless on load?
