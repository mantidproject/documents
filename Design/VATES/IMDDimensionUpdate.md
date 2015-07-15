#IMDDimension Update#

##Motivation##

The IMDWorkspace format in Mantid provides a flexible way to store n-dimensional data of any type. The format is not limited to work either with a fixed number, or dimensions, or a particular set of units for any of the dimensions.

Increasingly we need to know more information about the dimensions when algorithm, visualisation and other processing code needs to look for, and act on specific dimensions. The primary use case for this is to find the Q dimensions.

Up until now, we have had no way to do this, and have had to resort to regex matching the dimension names and ids in order to find our Q dimensions in the workspace. For example [here](https://github.com/mantidproject/mantid/blob/master/Code/Mantid/Framework/Geometry/src/Crystal/PeakTransformHKL.cpp#L9:L18). This is fragile, but the information to otherwise identify these dimensions is missing. Likewise, we have no good way of extracting the scaling off these dimensions. Once it gets written as a string. We would again need some kind of regex to rextract it. For example scaling information is applied [here](https://github.com/mantidproject/mantid/blob/master/Code/Mantid/Framework/MDAlgorithms/src/MDWSTransform.cpp#L357:L390), and used to create dimensions [by calling this](https://github.com/mantidproject/mantid/blob/master/Code/Mantid/Framework/MDAlgorithms/src/MDEventWSWrapper.cpp#L25:L46). you will notice the lack of other information fed into the MDHistoDimension because the MDHistoDimension currently has no proper placeholder for the unit type.

We currently have a visualisation request to lock the aspect ratios in the SliceViewer only for the Q dimensions, and this would be a good opportunity to tackle the issue properly as part of this work, and retrospectively fix the areas of the code base that string based matching to determine these fields.

In addition to this Andrei has pointed out that we ought to use the coordinate frame information to warn users when they apply cuts with non-orthonongal axis that span a mix of dimension types. For example a cut that included components along an output axis of both Qx and E.

### Why not use Kernel::Unit

1. Kernel::Unit mixes the concepts of Unit and Quantity. Time of Flight is not a [Unit](https://en.wikipedia.org/wiki/Units_of_measurement), it is a Quantity. Physical Quantities have measurement units to describe their magnitude. To describe Time of Flight, you could use either seconds, miliseconds, microseconds etc. Kernel::Unit does not support this option. For additional information on the basic software engineering aspects of this [see](http://martinfowler.com/eaaDev/quantity.html). For MDUnits, converting a measurement to a different set of units is an important operaton. R.L.U and A^-1 are convertable units in the HKL frame.
2. Kernel::Unit has been written to support conversions between Quantities via a TOF conversion. This does not fit well with the MDUnit.

**In summary the benefits of doing this work would be:**

1. The ability to fix aspect ratios for Q dimensions
1. The ability to detect how slicing has been applied (Andrei's suggestion)
1. For a subset of cases, The ability to switch units. For example from HKL to r.l.u.
1. Proper definitions for core-concepts, which will greatly aid maintenace and make things a lot easier to extend and test

##Definitions##

| Term        | Meaning          |
| ------------- |:-------------:|
| IMDWorkspace      | Interface for the multidimensional Mantid Workspace |
| IMDDimension      | Interface for a dimension of an IMDWorkspace |
| SliceViewer      | Multidimensional 2D slicing tool in Mantid |
| r.l.u       | Reciprocal lattice units |

##Solution 1##

This solution is based around introducing a complete set of missing types, which are fundamental to recording and interchanging between different representation.


####IMDDimension####

```cpp
class IMDDimension {

  ...
  public:
    MDFrame getMDFrame() const; // Add new accessor

};

```

####MDFrame####

New abstract type. This is designed to be light-weight enough save and load from files without affecting speed. This will replace Mantid::Kernel::SpecialCoordinateSystem

```cpp
class MDFrame {
  public:
    UnitLabel getUnitLabel() const = 0; // Concrete implementations will forward
    MDUnit getMDUnit() const = 0;
    bool canConvertTo(&MDUnit other) const = 0;
};

class QLab : public MDFrame{
  ...
};

class QSample : public MDFrame{
  ...
};

class HKL : public MDFrame{
  ...
};

class General : public MDFrame{
  ...
};


```

####MDUnit####

The reason to separate MDUnit from MDFrame is to support the concept of conversion better. While QLab can be converted to a different MDFrame, such as QSample or HKL, according to the Busing-Levy model, it is not possible to represent QLab or QSample in anything other than inverse Angstroms properly. HKL quantities can be represented in either inverse Angstroms or reciprocal lattice units. We would then later be able to add algorithms that support these conversions. We currently have to perform these conversions in a bespoke fashion in numerous places particularly in the Crystal module of Mantid.

HKL (r.l.u) and HKL (A^-1) would be modelled with the same MDFrame, but with different MDUnits. We would of course overload operator== to ensure that instances of these were treated as non-equal. Algorithms to perform these conversions both intra MDFrame and inter MDFrame to all data points would be simple enough, but not in the immediate scope of these changes.

```cpp
class MDUnit {
  public:
    virtual UnitLabel getUnitLabel() const = 0;
    bool operator==(const MDUnit&) const;
};

class QUnit : public MDUnit { // Useful for equality purposes
  ...
}

class RLU : public QUnit {
  ...
};

class InverseAngstroms : public QUnit {
  ...
};

class LabelMDUnit : public MDUnit {
  ...
};
```

###Development Steps###
1. Introduce the new type MDUnit and subtypes. Ensure equality is implemented properly.
1. Introduce the new type MDFrame and subtypes.
1. Create Factory for MDUnits. Fall through to GeneralUnits. Use Chain of Responsibility (see PeakShapeFactory)
1. Make additional constructor MDHistoDimension for the MDUnit type. Try to get rid of old string based constructor on MDHistoDimension
1. In LoadMD, have createDimension call MDUnitFactory
1. On MDDimension::createXML, update xml schema to include frame_name
1. In LoadMD try to read the frame_name. Fall back to GeneralFrame if you can't
1. Update constructor on MDHistoDimension to take the full MDFrame now, instead of the MDUnit
1. Look at any algorithm creating MDWorkspaces, where MDDimensions are being created, update them to pass the correct MDFrame and MDUnit information across. 

#### Second Phase
1. Kill SpecialCoordinateSystem on IMDWorkspaces. Fetch the information off the dimension instead by adding std::set<MDFrame> MDGeometry::qFrame() const. This should reliably return a set with a single entry, as we currently have no algorithms that can convert to a workspace that has a mix of coordinates in the qLab and qSample frame.
1. Keep the special coordinate member on PeaksWorkspace, but make it a MDFrame instead.
1. Update SetSpecialCoordinate algorithm so that it can only modify PeaksWorkspaces.

### Third Phase
Refactor existing code that parses dimension names

Refactoring all existing code to better use these types would be a further step.

##Further Requirements##
We are not handling the following yet:

* If we have a workspace in the HKL frame and we do a cut that gives an output dimension that is HH, we should still be able to convert between r.l.u and inverse Angstroms. This implies that the MDFrame should carry a list of functions required to perform the conversion.
* What about transformations that involve a shift as well as a scale. For example Energy to Temperature in F.
* Shared implementation between Kernel::Units and MDUnits. It may be possible to bring the two concepts together, but we need to have both concepts working first before we do this.


##Reviews##
* This document was presented to and discussed as part of [this](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/meetings/2015/TSC-meeting-2015-04-21.md) SSC meeting. The document has been updated accordingly.
* This document was reviewed by Anders Markvardsen on 23rd June 2015


