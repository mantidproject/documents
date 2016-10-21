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
 * SpectrumInfo needs to update positions on the fly, else we need to update values in SpectrumInfo too (if this is too slow can cache the values in SpectrumInfo)
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
* Merging algorithm - for several workspaces with different detector positions need to merge these correctly
 * Add the position to the vector of time indexded positions
 * Should not automatically sum any spectra - else problems with normalisation
 * Consistency checks - need to check the instrument sample positions, masking etc. - can wait for Instrument 2.0?
* D2B loader to test with

### Random notes

#### Moving detectors access

If we try to get a position of by detector index for a moving instrument, we should throw if the instrument has more than on time index - `DetectorInfo::position(detIndex)`.

#### Python legacy access

Problem - how to get parameterised detector in Python with new DetectorInfo class e.g. `ws.getDetector()`.

```
getPos {
if (pmap)
 if det in pmap
  return pmap.pos(det) // but what happens when the pmap has been emptied of position/rotation information?
ret base_component.pos()
```

Solution - wrap e.g. with an WrappingComponent class.

```
WrappingComponent {
 IComponent... <- for things like getShape()
 SpectrumInfo <- for things like getPos()
}
```

Might need two wrapper classes, or same class with two different pointers, for two different cases:
`MatrixWorkspace::getDetector()` - wrap with SpectrumInfo
`Instrument::getDetector()` - wrap with DetectorInfo

Dynamic cast will be required to work out what the component type is, three cases:
* DetectorGroup -> go via SpectrumInfo
* Detector -> go via DetectorInfo
* Other -> go via IComponent

### Monitors

If we have one long monitor count NormaliseToMonitor will need to normalise based on time at each position compared to total time.

If there is a spectrum for each time index then NormaliseToMonitor should take the correct spectrum for each normalisation, by matching the time indicies of monitors to the time indicies of the spectra.




