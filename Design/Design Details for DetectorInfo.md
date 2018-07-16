
# Exposing DetectorInfo

## Introduction
This document outlines which methods will be exposed from [`DetectorInfo.cpp`](https://github.com/mantidproject/mantid/blob/ffd49f84bdd2e1bb8f0deeb40727fe775a4974ae/Framework/Geometry/src/Instrument/DetectorInfo.cpp)to the Python side via the export file `DetectorInfo.cpp` which will be located at: 

`mantid/Framework/PythonInterface/mantid/geometry/src/Exports/DetectorInfo.cpp`. 

The currently existing [`DetectorInfo.cpp`](https://github.com/mantidproject/mantid/blob/dead50f2dbcf307f89ad63b69c2f51caccc9ade5/Framework/PythonInterface/mantid/api/src/Exports/SpectrumInfo.cpp) will need to be moved to this new location or deleted.
There are a number of methods present in [`DetectorInfo.cpp`](https://github.com/mantidproject/mantid/blob/ffd49f84bdd2e1bb8f0deeb40727fe775a4974ae/Framework/Geometry/src/Instrument/DetectorInfo.cpp) but it may not make sense to expose all of them to be used in Python scripts.
There are plans to expose [`SpectrumInfo`](https://github.com/mantidproject/mantid/blob/43fc616926a32863f37e37f4a107413a0de6dee6/Framework/API/src/SpectrumInfo.cpp) and [`ComponentInfo`](https://github.com/mantidproject/mantid/blob/8ec802f56c5db2261a0f9502f30f67fe42530d62/Framework/Geometry/src/Instrument/ComponentInfo.cpp) as well and so it is important that only the required methods from each class are exposed. As such it was decided that this document should be made so that decisions could be taken about which methods are the most relevant for users. Please see below for a list of the methods that are suggested for exposing to Python.

## Suggested Methods

Method Signature in DetectorInfo.h | Method Usage in Python
--------------------------------|--------------------------------------
`size_t size() const` | `len(DetectorInfo detectorInfoObject)`
`size_t size() const` | `size()`
`bool isMonitor(const size_t index) const` | `isMonitor(int index)`
`bool isMasked(const size_t index) const` | `isMasked(int index)`
`bool isEquivalent(const DetectorInfo &other) const` | `isEquivalent(DetectorInfo other)`
`double twoTheta(const size_t index) const` | `twoTheta(int index)`
`Kernel::V3D position(const size_t index) const` | `position(int index)`
`Kernel::Quat rotation(const size_t index) const` | `rotation(int index)`
`void setMasked(const size_t index, bool masked)` | `setMasked(int index, bool masked)`
`void clearMaskFlags()` | `clearMaskFlags()`

### Further Information
As can be seen from the above table, the majority of the exported methods retain their name and arguments on the Python side.
It was also decided that any methods involving `position` or `rotation` would need to have their documentation updated such that the prefix "absolute" is used when referring to those methods. The purpose of this being so that we can distinguish between `Instrument 1.0` and `Instrument 2.0`.

To gain access to the `DetectorInfo` object and run the above methods the user must do something similar to:

```python

info = workspace.detectorInfo()
info.clearMaskFlags()

```
The user receives a `DetectorInfo` object on which they can call the methods listed above. Testing will need to be carried out to check what happens if the `Workspace` goes out of scope. However, it is likely that a runtime error would occur.  
