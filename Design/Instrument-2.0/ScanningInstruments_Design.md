### Requirements

See [Scanning Instruments ILL](ScanningInstruments_ILL.md) for ILL requirements.

### Design

#### DetectorInfo

The core of the change will be in the [`DetectorInfo`](https://github.com/mantidproject/mantid/blob/master/Framework/API/inc/MantidAPI/DetectorInfo.h) class.

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

bool isMonitor(const size_t index, const size_t timeIndex=0) const;
bool isMasked(const size_t index, const size_t timeIndex=0) const;
double l2(const size_t index, const size_t timeIndex=0) const;
double twoTheta(const size_t index, const size_t timeIndex=0) const;
double signedTwoTheta(const size_t index, const size_t timeIndex=0) const;
Kernel::V3D position(const size_t index, const size_t timeIndex=0) const;
Kernel::Quat rotation(const size_t index, const size_t timeIndex=0) const;

void setPosition(const size_t index, const Kernel::V3D &position, const size_t timeIndex=0);
void setRotation(const size_t index, const Kernel::Quat &rotation, const size_t timeIndex=0);

void setPosition(const Geometry::IComponent &comp, const Kernel::V3D &pos, const size_t timeIndex=0);
void setRotation(const Geometry::IComponent &comp, const Kernel::Quat &rot, const size_t timeIndex=0);
```

The `timeIndex` argument is optional, so algorithms that do not care about time indexing will simply return the first/only time index.

#### SpectrumInfo

Currently [`SpectrumInfo`](https://github.com/mantidproject/mantid/blob/master/Framework/API/inc/MantidAPI/DetectorInfo.h) has a `getDetector` method for finding the detector for the workspace. This uses the `getSpectrum(index)` method on `MatrixWorkspace` to return the detector IDs for the spectrum.

This should be changed, or a new method added, for example `getTimeIndexedDetectorIDs(index)` to return a set of `std::pair<detid_t, size_t>`.

This can be used to access methods on `DetectorInfo` of the form `m_detectorInfo.twoTheta(detIndex, timeIndex)`.


