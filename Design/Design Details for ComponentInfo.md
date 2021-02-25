# Exposing ComponentInfo

## Introduction
This document outlines which methods will be exposed from [`ComponentInfo.h`](https://github.com/mantidproject/mantid/blob/8ec802f56c5db2261a0f9502f30f67fe42530d62/Framework/Geometry/inc/MantidGeometry/Instrument/ComponentInfo.h) to the Python side via the export file `ComponentInfo.cpp` which will be located at: 

`mantid/Framework/PythonInterface/mantid/geometry/src/Exports/ComponentInfo.cpp`. 

This class has not yet been exposed to Python in any way, so a completely new file wiil need to be created and added to the location mentioned above. In addition to this [`ExperimentInfo.cpp`](https://github.com/mantidproject/mantid/blob/dead50f2dbcf307f89ad63b69c2f51caccc9ade5/Framework/PythonInterface/mantid/api/src/Exports/ExperimentInfo.cpp) will also be modified to expose the new method `componentInfo()`. 

There are a number of methods present in [`ComponentInfo.h`](https://github.com/mantidproject/mantid/blob/8ec802f56c5db2261a0f9502f30f67fe42530d62/Framework/Geometry/inc/MantidGeometry/Instrument/ComponentInfo.h) but it may not make sense to expose all of them to be used in Python scripts.
There are plans to expose [`SpectrumInfo`](https://github.com/mantidproject/mantid/blob/43fc616926a32863f37e37f4a107413a0de6dee6/Framework/API/inc/MantidAPI/SpectrumInfo.h) and [`DetectorInfo`](https://github.com/mantidproject/mantid/blob/ffd49f84bdd2e1bb8f0deeb40727fe775a4974ae/Framework/Geometry/inc/MantidGeometry/Instrument/DetectorInfo.h) as well and so it is important that only the required methods from each class are exposed. As such it was decided that this document should be made so that decisions could be taken about which methods are the most relevant for users. Please see below for a list of the methods that are suggested for exposing to Python.

## Suggested Methods

Method Signature in ComponentInfo.h | Method Usage in Python
--------------------------------|--------------------------------------
`size_t size() const` | `int len(ComponentInfo componentInfoObject)`
`size_t size() const` | `int size(int index)`
`bool isDetector(const size_t componentIndex) const` | `bool isDetector(int index)`
`std::vector<size_t> detectorsInSubtree(size_t componentIndex) const` | `list<int> detectorsInSubtree(int index)`
`std::vector<size_t> componentsInSubtree(size_t componentIndex) const` | `list<int> componentsInSubtree(int index)`
`Kernel::V3D position(const size_t componentIndex) const` | `V3D position(int index)`
`Kernel::Quat rotation(const size_t componentIndex) const` | `Quat rotation(int index)`
`Kernel::V3D relativePosition(const size_t componentIndex) const` | `V3D relativePosition(int index)`
`Kernel::Quat relativeRotation(const size_t componentIndex) const`| `Quat relativeRotation(int index)`
`void setPosition(const size_t componentIndex, const Kernel::V3D &newPosition)` | `void setPosition(int index, V3D position)`
`void setRotation(size_t componentIndex, const Kernel::Quat &newRotation)` | `void setRotation(int index, Quat position)`
`bool hasSource() const` | `bool hasSource()`
`bool hasSample() const` | `bool hasSample()`
`size_t source() const` | `int source()`
`size_t sample() const` | `int sample()`
`Kernel::V3D sourcePosition() const` | `V3D sourcePosition()`
`Kernel::V3D samplePosition() const` | `V3D samplePosition()`
`bool hasParent(const size_t componentIndex) const` | `bool hasParent(int index)`
`size_t parent(const size_t componentIndex) const` | `int parent(int index)`
`const std::vector<size_t> &children(size_t componentIndex) const` | `list<int> children(int index)`
`const std::string &name(const size_t componentIndex) const` | `string name(int index)`

### Further Information
As can be seen from the above table, all of the exported methods retain their name and arguments on the Python side.
It was also decided that any methods involving `position` or `rotation` would need to have their documentation updated such that the prefix "absolute" is used when referring to those methods. The purpose of this being so that we can distinguish between `Instrument 1.0` and `Instrument 2.0`.

To gain access to the `ComponentInfo` object and run the above methods the user must do something similar to:

```python

info = workspace.componentInfo()
info.name(0)

```
The user receives a `ComponentInfo` object on which they can call the methods listed above. Testing will need to be carried out to check what happens if the `Workspace` goes out of scope. However, it is likely that a runtime error would occur.  
