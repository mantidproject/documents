## Scanning Instrument Support for the ILL

### Background

#### Instrument 2.0

The full discussion on Instrument 2.0 is beyond the scope of this document, more details are contained in this [requirements document](requirements-v2.md). A short summary on [scanning instrument requirements is given](requirements-v2.md#moving-instruments-requirements) within this document.

For the purposes of the discussion here scanning instruments (or moving instruments) describe instruments that have detectors that can be in different positions during a single run. This forms a step scan. This is used to cover data collection where there are gaps between detectors. The aim of the work is to be able to deal with such detectors that move during a run, and be able to accumulate the data into a single workspace with the detectors at different positions throughout the run. This does not include two other use cases from the Instrument 2.0 requirements document; continuous scans and triple axis spectrometers.

#### ILL Requirements

The ILL have a requirement to implement support for moving instruments by the end of April 2017, in order to work with some of the diffractometers in use there. It is planned to implement the Instrument 2.0 support for moving instruments early in Mantid, to support the work at the ILL in a way that will not need to change with the full implementation of instrument 2.0. This document aims to describe the necessary steps to implement the Instrument 2.0 parts required.

#### Overview of Proposed Implementation

Two classes related to this have already been partially implemented in Mantid, [`SpectrumInfo`](https://github.com/mantidproject/mantid/pull/17394) and [`DetectorInfo`](https://github.com/mantidproject/mantid/pull/17875). These define the new way of working with commonly used information about a spectrum, namely isMasked, isMonitor, l2, twoTheta, signedTwoTheta, position, rotation and eFixed (coming soon). Eventually `DetectorInfo` will be responsible for the ownership of the parameters for the position and rotation, so for example moving a detector would have the new position stored in the `DetectorInfo` class, instead of the parameter map as is done currently. Values such as `l2` and `twoTheta` would use the new position when called and cache the return value, until another position change invalidates it.

Support for the moving instruments will be implemented via the `DetectorInfo` class. The usage `SpectrumInfo` class needs no direct knowledge of the time indexing. The methods on the `DetectorInfo` class for accessing detector information will be accessed by giving a detector index and an optional time index. It will also hold information on the start and end times for each time index. Any further information, for example to normalise to monitor counts, can be held in a time series sample log.

### Design

#### `DetectorInfo`

The core of the changes to support scanning instruments will be in the [`DetectorInfo`](https://github.com/mantidproject/mantid/blob/master/Framework/API/inc/MantidAPI/DetectorInfo.h) class. There are two choices for implementing the required changes in `DetectorInfo`. Currently the methods `isMonitor`, `isMasked`, `l2`, `twoTheta`, `signedTwoTheta`, `position`, `rotation`, `setPosition` and `setRotationEach` are accessed by a detector index. This could be kept and the detector index would be associated with a detector ID and a time index. Alternatively the methods can be accessed by supplying the detector index, which has a one-to-one correspondence with a detector ID, and a time index. There would be a time index corresponding to each position in the step scan.

The current plan is to access to add methods that take a detector index and a time index, in addition to the methods that take just a detector index. Accessing a scanning instrument with just a detector index would throw. This will save memory on detector metadata which would not change for different time indices, such as the monitor flag. See the end of this document for the changes to the signature of some of the public `DetectorInfo` methods.

The `timeIndex` argument is optional, so algorithms that do not care about time indexing will simply return the first/only time index. `DetectorInfo` should also contain a vector of start and end times for each time index. This will mean any information stored as a time series sample log can also be obtained for the correct step, for example the monitor counts for normalisation.

`DetectorInfo` will ultimately store the information for positions and rotation, so will need to do this in a way that can be accessed by both the detector index and time index. Masking could also be stored in a time indexed fashion.

#### `SpectrumInfo`

Currently [`SpectrumInfo`](https://github.com/mantidproject/mantid/blob/master/Framework/API/inc/MantidAPI/SpectrumInfo.h) has a private `getDetector` method for finding the detector for the workspace. This uses the `getSpectrum(index)` method on `MatrixWorkspace` to return the detector IDs for the spectrum.

A new method should be added, for example `getTimeIndexedDetectorIDs(index)` to return a set of `std::pair<detid_t, size_t>`.

This can be used to access methods on `DetectorInfo`, for example `m_detectorInfo.twoTheta(detIndex, timeIndex)`.

#### `MatrixWorkspace` & `ISpectrum`/`Spectrum`

As metioned under **`SpectrumInfo`** `MatrixWorkspace` will require a `getTimeIndexedDetectorIDs(index)` method.

This implies the member variable `std::set<detid_t> detectorIDs` in `ISpectrum` will need to become `std::set<std::pair<detid_t, size_t>> timeIndexedDetectorIDs`.

The corresponding methods in `ISpectrum` would also need to be replicated for the time indexed case. For example `addDetectorID(const std::pair<detid_t, size_t> timeIndexedDetID)`.

The original methods such as `this->detectorIDs.insert(detID)` should remain and add detectors at time index 0. This allows existing algorithms, e.g. loaders, that do not need time indexing to work as before. Similarly the `getDetectorIDs(index)` method would still return detector IDs without the time indexing information.

**Note:** working directly with the detector IDs is something that should be eliminated with the use of `SpectrumInfo` and `DetectorInfo`. The use of a `getTimeIndexedDetectorIDs` or `getDetectorIDs` should not be needed in the final Instrument 2.0. Similarly the method `getSpectrum(index)` on `MatrixWorkspace` should eventually be eliminated.

### Implementation

For more details on the rollout plan see the document [Scanning Instruments Plan](ScanningInstruments_Plan.md).

For this design to be implemented the use of `SpectrumInfo` and `DetectorInfo` will need to be rolled out in Mantid. The rollout for [`SpectrumInfo`](https://github.com/mantidproject/mantid/issues/17743) has been started.

### New DetectorInfo Signatures

Currently detector info public methods look like the following.

```cpp
DetectorInfo(boost::shared_ptr<const Geometry::Instrument> instrument,
           Geometry::ParameterMap *pmap = nullptr);

bool isMonitor(const size_t index) const;
bool isMasked(const size_t index) const;
double l2(const size_t index) const;
double twoTheta(const size_t index) const;
double signedTwoTheta(const size_t index) const;
Kernel::V3D position(const size_t index) const;
Kernel::Quat rotation(const size_t index) const;

void setPosition(const size_t index, const Kernel::V3D &position);
void setRotation(const size_t index, const Kernel::Quat &rotation);

void setPosition(const Geometry::IComponent &comp, const Kernel::V3D &pos);
void setRotation(const Geometry::IComponent &comp, const Kernel::Quat &rot);
```

The following methods will be given require a time index access, in addition to the detector index.

```cpp
DetectorInfo(boost::shared_ptr<const Geometry::Instrument> instrument,
           Geometry::ParameterMap *pmap = nullptr);

bool isMonitor(const size_t index) const;
bool isMasked(const size_t index) const;
double l2(const size_t index) const;
double l2(const size_t index, const size_t timeIndex) const;
double twoTheta(const size_t index) const;
double twoTheta(const size_t index, const size_t timeIndex) const;
double signedTwoTheta(const size_t index) const;
double signedTwoTheta(const size_t index, const size_t timeIndex) const;
Kernel::V3D position(const size_t index) const;
Kernel::V3D position(const size_t index, const size_t timeIndex) const;
Kernel::Quat rotation(const size_t index) const;
Kernel::Quat rotation(const size_t index, const size_t timeIndex) const;

void setPosition(const size_t index, const Kernel::V3D &position);
void setPosition(const size_t index, const Kernel::V3D &position, const size_t timeIndex);
void setRotation(const size_t index, const Kernel::Quat &rotation);
void setRotation(const size_t index, const Kernel::Quat &rotation, const size_t timeIndex);

void setPosition(const Geometry::IComponent &comp, const Kernel::V3D &pos);
void setPosition(const Geometry::IComponent &comp, const Kernel::V3D &pos, const size_t timeIndex);
void setRotation(const Geometry::IComponent &comp, const Kernel::Quat &rot);
void setRotation(const Geometry::IComponent &comp, const Kernel::Quat &rot, const size_t timeIndex);
```

`isMonitor` and `isMasked` do not need to have moving instrument access. Monitors should not ever need to change. If a specific detector position needs to be masked that should be done by masking the spectrum.

The routines without time indexing should always throw if they are attempted to be used on a non-moving instrument.

