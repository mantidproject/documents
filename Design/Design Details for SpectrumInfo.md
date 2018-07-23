# Exposing SpectrumInfo

## Introduction
This document outlines which methods will be exposed from [`SpectrumInfo.h`](https://github.com/mantidproject/mantid/blob/43fc616926a32863f37e37f4a107413a0de6dee6/Framework/API/inc/MantidAPI/SpectrumInfo.h) to the Python side via the export file [`SpectrumInfo.cpp`](https://github.com/mantidproject/mantid/blob/dead50f2dbcf307f89ad63b69c2f51caccc9ade5/Framework/PythonInterface/mantid/api/src/Exports/SpectrumInfo.cpp).
There are a number of methods present in [`SpectrumInfo.h`](https://github.com/mantidproject/mantid/blob/43fc616926a32863f37e37f4a107413a0de6dee6/Framework/API/inc/MantidAPI/SpectrumInfo.h) but it may not make sense to expose all of them to be used in Python scripts.
There are plans to expose [`DetectorInfo`](https://github.com/mantidproject/mantid/blob/ffd49f84bdd2e1bb8f0deeb40727fe775a4974ae/Framework/Geometry/inc/MantidGeometry/Instrument/DetectorInfo.h) and [`ComponentInfo`](https://github.com/mantidproject/mantid/blob/8ec802f56c5db2261a0f9502f30f67fe42530d62/Framework/Geometry/inc/MantidGeometry/Instrument/ComponentInfo.h) as well and so it is important that only the required methods from each class are exposed. As such it was decided that this document should be made so that decisions could be taken about which methods are the most relevant for users. Please see below for a list of the methods that are suggested for exposing to Python.

## Suggested Methods

Method Signature in SpectrumInfo.cpp | Method Usage in Python
--------------------------------|--------------------------------------
`size_t size() const` | `int len(SpectrumInfo obj)`
c`size_t size() const` | `int size()`
p`bool isMonitor(const size_t index) const` | `bool isMonitor(int index)`
`bool isMasked(const size_t index) const` | `bool isMasked(int index)`
`void setMasked(const size_t index, bool masked)` | `void setMasked(int index, bool masked)`
`double twoTheta(const size_t index) const` | `double twoTheta(int index)`
`double signedTwoTheta(const size_t index) const` | `double signedTwoTheta(int index)`
`double l1() const` | `double l1()`
`double l2(const size_t index) const` | `double l2(int index)`
`bool hasDetectors(const size_t index) const` | `bool hasDetectors()`
`bool hasUniqueDetector(const size_t index) const` | `bool hasUniqueDetector(int index)`
p`Kernel::V3D position(const size_t index) const` | `V3D position(int index)`
`Kernel::V3D sourcePosition() const` | `V3D sourcePosition()``Kernel::V3D samplePosition() const` | `V3D samplePosition()`
-- | `list<SpectrumDefinition> getAllSpectrumDefinitions()`

### Further Information
As can be seen from the above table, the majority of the exported methods retain their name and arguments on the Python side.
`const std::pair<size_t, size_t> &operator[](const size_t index)` | `__getitem__(int index)`
It was also decided that any methods involving `position` or `rotation` would need to have their documentation updated such that the prefix "absolute" is used when referring to those methods. The purpose of this being so that we can distinguish between `Instrument 1.0` and `Instrument 2.0`.

The last change is with regards to the method `getAllSpectrumDefinitions()`. This method is not actually implemented in the C++ `SpectrumInfo` class but it is exported as it was thought that a list of all the `SpectrumDefinition`s would be more natural to users.

To gain access to the `SpectrumInfo` object and run the above methods the user must do something similar to:

```python
info = workspace.spectrumInfo()
info.l1()

```
The user receives a `SpectrumInfo` object on which they can call the methods listed above. Testing will need to be carried out to check what happens if the `WorkSpace` goes out of scope. However, it is likely that a runtime error would occur.  

## Exposing SpectrumDefinition 
The methods to be exposed in `SpectrumDefinition` can be found at [`SpectrumDefinition.h`](https://github.com/mantidproject/mantid/blob/7c099518cd4351da37474e96cdc005678bebf753/Framework/Types/inc/MantidTypes/SpectrumDefinition.h)
Since the method `getAllSpectrumDefinitions()` returns a list of type `SpectrumDefinition`, a new class called `SpectrumDefinition` was exposed as well. This object allows the user access to the following methods:

Method Signature in SpectrumDefinition.h | Method Usage in Python
--------------------------------|--------------------------------------
`const std::pair<size_t, size_t> &operator[](const size_t index)` | `__getitem__(int index)`
`size_t size() const` | `int size()`
`void add(const size_t detectorIndex, const size_t timeIndex = 0)` | `void add(int detectorIndex, int timeIndex)`
`bool operator==(const SpectrumDefinition &other) const` | `bool equals(SpectrumDefinition other)`

### Further Information
The `__getitem__` method would actually need to call an another intermediate method called `toTuple()`. This intermediate method is required as the return type of `operator[]` is a `std::pair<size_t, size_t>` and it does not really make sense to expose this type to Python when the `tuple` type already exists! The `toTuple()` method extracts out the pair details and creates and returns a `boost::python::tuple`.

To gain access to the `SpectrumDefinition` objects the user must do something similar to:

```python

info = workspace.spectrumInfo()
spectrumDefinitionList = info.getAllSpectrumDefinitions()
```

They can then call the above methods by indexing into `spectrumDefinitionList` - e.g.

```python

spectrumDefinitionList[0].size()

```
