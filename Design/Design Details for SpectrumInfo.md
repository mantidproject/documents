# Exposing SpectrumInfo

## Introduction
This document outlines which methods will be exposed from `SpectrumInfo` to the Python side.
There are a number of methods present in `SpectrumInfo.cpp` but it may not make sense to expose all of them to be used in Python scripts.
There are plans to expose `DetectorInfo` and `ComponentInfo` as well and so it is important that only the required methods from each class are exposed. As such it was decided that this document should be made so that decisions could be taken about which methods are the most relevant for users. Please see below for a list of the methods that are suggested for exposing to Python.

## Suggested Methods

Method Signature in SpectrumInfo.cpp | Method Usage in Python
--------------------------------|--------------------------------------
`bool SpectrumInfo::isMonitor(const size_t index) const` | `isMonitor(int index)`
`bool SpectrumInfo::isMasked(const size_t index) const` | `isMasked(int index)`
`void SpectrumInfo::setMasked(const size_t index, bool masked)` | `setMasked(int index, bool masked)`
`bool SpectrumInfo::hasDetectors(const size_t index) const` | `hasDetectors()`
`double SpectrumInfo::twoTheta(const size_t index) const` | `twoTheta(int index)`
`double SpectrumInfo::signedTwoTheta(const size_t index) const` | `signedTwoTheta(int index)`
`size_t SpectrumInfo::size() const` | `size()`
`bool SpectrumInfo::hasUniqueDetector(const size_t index) const` | `hasUniqueDetector(int index)`
`double SpectrumInfo::l1() const` | `l1()`
`double SpectrumInfo::l2(const size_t index) const` | `l2(int index)`
`Kernel::V3D SpectrumInfo::position(const size_t index) const` | `absolutePosition(int index)`
`Kernel::V3D SpectrumInfo::sourcePosition() const` | `absoluteSourcePosition()`
`Kernel::V3D SpectrumInfo::samplePosition() const` | `absoluteSamplePosition()`
-- | `getAllSpectrumDefinitions()`

### Further Information
As can be seen from the above table, the majority of the exported methods retain their name and arguments on the Python side. Some of the exceptions are the following:

* `position()` -> `absolutePosition()`
* `sourcePosition()` -> `absoluteSourcePosition()`
* `samplePosition()` -> `absoluteSamplePosition()`

For these three methods, the prefix "absolute" is prepended to the method names so that we can distinguish between `Instrument 1.0` and `Instrument 2.0`.

The last change is with regards to the method `getAllSpectrumDefinitions()`. This method is not actually implemented in the C++ `SpectrumInfo` class but it is exported as it was thought that a list of all the `SpectrumDefinition`s would be more natural to users.

To gain access to the `SpectrumInfo` object and run the above methods the user must do something similar to:

```python

info = workspace.spectrumInfo()
info.l1()

```

## Exposing SpectrumDefinition 
Since the method `getAllSpectrumDefinitions()` returns a list of type `SpectrumDefinition`, a new class called `SpectrumDefinition` was exposed as well. This object allows the user access to the following methods:

Method Signature in SpectrumDefinition.h | Method Usage in Python
--------------------------------|--------------------------------------
`size_t size() const` | `size()`
`void add(const size_t detectorIndex, const size_t timeIndex = 0)` | `add(int detectorIndex, int timeIndex)`
`bool operator==(const SpectrumDefinition &other) const` | `equals(SpectrumDefinition other)`
`const std::pair<size_t, size_t> &operator[](const size_t index)` | `get(int index)`

### Further Information
The `get()` method actually calls an another intermediate method called `toTuple()`. This intermediate method is required as the return type of `operator[]` is a `std::pair<size_t, size_t>` and it does not really make sense to expose this type to Python when the `tuple` type already exists! The `toTuple()` method extracts out the pair details and creates and returns a `boost::python::tuple`.

To gain access to the `SpectrumDefinition` objects the user must do something similar to:

```python

info = workspace.spectrumInfo()
spectrumDefinitionList = info.getAllSpectrumDefinitions()
```

They can then call the above methods by indexing into `spectrumDefinitionList` - e.g.

```python

spectrumDefinitionList[0].size()

```
