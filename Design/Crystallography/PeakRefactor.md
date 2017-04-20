# Peak Refactoring

## Motivation
The `Peak` class is widely used throughout Mantid but there are some problems
with the current implementation that should be addressed:

 - Currently there are 6 constructors for a peak object which is a classic 
 symptom of code that is trying to do too much.

```
  Peak(const Geometry::Instrument_const_sptr &m_inst,
       const Mantid::Kernel::V3D &QLabFrame,
       boost::optional<double> detectorDistance = boost::none);

  Peak(const Geometry::Instrument_const_sptr &m_inst,
       const Mantid::Kernel::V3D &QSampleFrame,
       const Mantid::Kernel::Matrix<double> &goniometer,
       boost::optional<double> detectorDistance = boost::none);

  Peak(const Geometry::Instrument_const_sptr &m_inst, int m_detectorID,
       double m_Wavelength);

  Peak(const Geometry::Instrument_const_sptr &m_inst, int m_detectorID,
       double m_Wavelength, const Mantid::Kernel::V3D &HKL);

  Peak(const Geometry::Instrument_const_sptr &m_inst, int m_detectorID,
       double m_Wavelength, const Mantid::Kernel::V3D &HKL,
       const Mantid::Kernel::Matrix<double> &goniometer);

  Peak(const Geometry::Instrument_const_sptr &m_inst, double scattering,
       double m_Wavelength);
```

 - `Peak` recalculates some of its quantities on the fly
