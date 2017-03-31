## Python `getDetector` method

The methods `MatrixWorkspace::getDetector` and `Instrument::getDetector` are being phased out, with their use being replaced by `SpectrumInfo` and `DetectorInfo` respectively.

There is a question about what to do about the exported Python method `getDetector`. Below are some of the options available.

Wrapping it would require re-implementing a large number of methods as `Detector` and `DetectorGroup` have a long inheritance tree. Inheritance 

### 1. Remove `getDetector`

Remove this method and break backwards compatibility for any Python scripts using the `getDetector` method. A detailed warning can be printed when someone attempts to use this method, explaining how to use the new `SpectrumInfo` and `DetectorInfo` methods.

### 2. Add pointers to `DetectorInfo` & `SpectrumInfo` to `IDetector`

We would need to add to `IDetector` pointers to the `DetectorInfo` and `SpectrumInfo` objects, as well as values for the spectrum index and detector index.

When calling `MatrixWorkspace::getDetector` for the Python export `SpectrumInfo *` should be initialised. The exported version of `IDetector::isMasked` and similar methods should use `m_detectorInfo`.

### 3. Use a `DetectorInfoItem` class

For a discussion in a similar context it was proposed to add a `DetectorInfoItem` class. This would hold all the information required for the detector component.

This would require re-implementing all the methods in the inheritance tree for `IDetector` ~29 methods for `Detector` and further ones used only be `DetectorGroup`. This will cause extra maintenance work.

```cpp
#include <vector>
#include <stdio.h>

namespace Geometry {
  struct IComponent {
    virtual double getPos() const = 0;
  };

  struct Sample : public IComponent {
    double getPos() const override { return 1.0; }
  };

  void legacyCode(const IComponent &comp) { printf("Comp at pos %e\n", comp.getPos()); }
}

namespace Beamline {
class Detector;

class DetectorInfo {
public:
  DetectorInfo(const size_t size) : m_masked(size), m_pos(size) {}
  const DetectorInfoItem operator[](const size_t index) const;
  bool isMasked(const size_t index) const { return m_masked[index]; }
  double pos(const size_t index) const { return m_pos[index]; }

private:
  std::vector<bool> m_masked;
  std::vector<double> m_pos;
};

class DetectorInfoItem : public Geometry::IComponent {
public:
  DetectorInfoItem(const DetectorInfo *parent, const size_t index)  : m_parent(parent), m_index(index){};

  bool isMasked() const { return m_parent->isMasked(m_index); }
  double pos() const { return m_parent->pos(m_index); }

  // Overloads for IComponent methods
  double getPos() const override { return pos(); }

private:
  const DetectorInfo *m_parent;
  const size_t m_index;
};

const DetectorInfoItem DetectorInfo::operator[](const size_t index) const { return DetectorInfoItem(this, index); }
}

int main() {
  Geometry::Sample sample;
  Beamline::DetectorInfo info(2);

  Geometry::legacyCode(sample);
  Geometry::legacyCode(info[0]);
  Geometry::legacyCode(info[1]);
}
```

