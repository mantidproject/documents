This is a document to capture the plans to support Scanning Instruments. The parts of Instrument 2.0 required to supporort this are listed below. 

### Current work

* DetectorInfo wrapper class - SH - 2 weeks
 * Maps from detector IDs to dector indicies
* Refactoring to use SpectrumInfo - IB - 
* Read Selected Information from Saved ParameterMap -IB
 * Could be just for scanning instruments as a stop gap
 * Should remove things from parameter map so acces is only via DetectorInfo
 * Should not called automatically/merged until the Python legacy access is done
 
### Future work

* DetectorInfo move mechanism
```
DecectorInfo::move(Component *c) {
 if (isDetector(c))
  m_position = moved...
 else
  ComponentHelper::move(c, ...)
  updateDetectorPositions()
```
* DetectorInfo add time indexded vector of positions and rotations
* Refactor existing classes to use DetectorInfo
* Saving NeXus processed files
* Python interface legacy access
