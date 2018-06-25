# FitPeaks

## The algorithms to do peak fitting in Mantid

* [Fit](http://docs.mantidproject.org/nightly/algorithms/Fit-v1.html)
* [FitPeak](http://docs.mantidproject.org/nightly/algorithms/FitPeak-v1.html)
* [FindPeaks](http://docs.mantidproject.org/nightly/algorithms/FindPeaks-v1.html)
* MantidPlot fitting UI

### A brief history

* Long long time ago...
 * Fit
 * FindPeaks -- call Fit as a child algorithm
   * Finding peaks by fitting peaks in the given location;
   * Using Mariscotti algorithm to *observe* peaks; Fitting peaks that are *observed*
* Required to improve for
 * fitting some vanadium peaks
 * fitting for tens of thousands Gaussian peaks
* FindPeaks got more and more complicated and hard to read and improve
 * FitPeak was split from FindPeaks for better maintanence
* Eventually in 2017, it failed on several applications
 * Vulcan's diamond data
 * Powgen's low angle data
 
### What we want in FitPeaks

* Be able to fit all the peaks present FindPeaks can fit,
 * i.e., replace peak fitting in FindPeaks
* Easy to set up
* Be able to tackle the complicated use cases
* More on non-functional requirements
 * Output fitted data
 * Detailed list of fitted parameters' value
 * and etc.

## First place to look: [Concept Pages](http://docs.mantidproject.org/nightly/concepts/WorkspaceGroup.html).

Documentation says:
> A WorkspaceGroup is a group of workspaces.

Gives information on:
* grouping
* un-grouping
* expected behaviour in algorihtms



## Using WorkspaceGroups in Algorithms
* Algorithms which accept Workspaces properties which are not groups may in some cases still run with WorkspaceGroups. The result will be the algorithm being executed on each workspace in the group in turn.
```python
dataX = [0, 2, 4, 6, 8, 10, 12, 14]
dataY = [98, 30, 10, 2, 1, 1, 1]

ws1 = CreateWorkspace(dataX, dataY)
ws2 = CloneWorkspace(ws1)

group = GroupWorkspaces([ws1, ws2])


ouput = Rebin(group, 1)


print type(ouput)
```
* Algorithms which accept WorkspaceGroup specifically will not work if the wrong workspace type is passed e.g PolarizationCorrection.
```python
dataX = [0, 2, 4, 6, 8, 10, 12, 14]
dataY = [98, 30, 10, 2, 1, 1, 1]

ws = CreateWorkspace(dataX, dataY)

output = PolarizationCorrection(ws) #ValueError
```



