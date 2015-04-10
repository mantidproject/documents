#IMDDimension Update#

##Motivation##

The IMDWorkspace format in Mantid provides a flexible way to store n-dimensional data of any type. The format is not limited to work either with a fixed number, or dimensions, or a particular set of units for any of the dimensions.

Increasingly we need to know more information about the dimensions when algorithm, visualisation and other processing code needs to look for, and act on specific dimensions. The primary use case for this is to find the Q dimensions.

Up until now, we have had no way to do this, and have had to resort to regex matching the dimension names and ids in order to find our Q dimensions in the workspace. For example [here](https://github.com/mantidproject/mantid/blob/master/Code/Mantid/Framework/API/src/PeakTransformHKL.cpp#L9:L18). This is fragile, but the information to otherwise identify these dimensions is missing.

We currently have a visualisation request to lock the aspect ratios in the SliceViewer only for the Q dimensions, and this would be a good opportunity to tackle the issue properly as part of this work, and retrospectively fix the areas of the code base that string based matching to determine these fields.

##Definitions##

| Term        | Meaning          |
| ------------- |:-------------:|
| IMDWorkspace      | Interface for the multidimensional Mantid Workspace |
| IMDDimension      | Interface for a dimension of an IMDWorkspace |
| SliceViewer      | Multidimensional 2D slicing tool in Mantid |
| r.l.u       | Reciprocal lattice units |

##Solution and Questions##

*Rough ideas at this point:*

* The fix will be made to IMDDimension and all subtypes
* Information is missing from the IMDDimension relating to Units (first-class citizens, not UnitLabels) 
* QLab, QSample and HKL need to be recognised. We could use the existing Mantid::Kernel::SpecialCoordinates enum for this?
* Units of HKL (but not QLab and QSample which are normally in A^-1) need to be marked as either being in r.l.u or A^-1
* Is there any other information we are missing from IMDDimension we can add as we do this?



