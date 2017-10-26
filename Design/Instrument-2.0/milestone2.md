## Brief

Instrument 2.0 has been progressing since January 2016, having been prototyped, the design is now being applied to Mantid. This document reflects the work as of September 2017. 

Very high-level summary of completed work

* Prototype completed and used to steer project
* `DetectorInfo` applied 
* `SpectrumInfo` applied
* `ComponentInfo` applied
* Scanning capabilities applied to `DetectorInfo`
* `InstrumentView` performance investigation completed

## Remaining Work

In conjunction with the [original requirements](https://github.com/mantidproject/documents/blob/master/Design/Instrument-2.0/requirements-v2.md) we identify the following items as remaining within the ESS scope of work.

### Major Items

| Item                | Priority      | Estimated Dev Time  | Notes      |
| ------------------- |:-------------:|:-------------------:|:----------:| 
| Complex Beam Paths  | L | | Fix the Physical/Neutronic instrument problem. Increasingly relevant for ESS instruments. A solution has been prototyped and proved to give good performance. Major time spent will be in fixing Mantid's existing workarounds and removing "neutronic positions". Mantid also lacks a way to specify the beam path at present. |
| Serialization/Deserialization | H | | Cross over with NexusGeometry. Instrument Prototype explored a design which actually allowed different "back-ends" or formats for the serialization, which has a number of benefits from both a flexibility and SE perspective|
| Rollout Instrument 2.0 to `InstrumentView` | M/H | | [Report](https://github.com/DMSC-Instrument-Data/documents/blob/master/investigations/Possible_Instrument_View_Improvements.md) shows that applying Instrument 2.0 may yield good improvements to the `InstrumentView`. However, this is not high-risk. Do we need to do this now given that it doesn't seem particularly complex to do?|
| Scanning any Component | H | | Only Detectors can currently be scanned. This may provide a solution to a Nexus saving issue. Also, do we need to scan every type of component for ESS instruments? Probably not complex to implement and we will get the help of the ILL to do so. This is actually a sub-requirement of the serialization/deserialization issue above. |

### Minor Items

| Item                | Priority      | Estimated Dev Time  | Notes      |
| ------------------- |:-------------:|:-------------------:|:----------:| 
| Write builder for `ComponentInfo`, `DetectorInfo` | L | |  A constructionl object similar to `InstrumentVisitor` required, that bypasses the need to have `Instrument 1.0` aprori useful for testing at present and eventual `Instrument 1.0` replacement |
| Prevent Detector id Duplication | M | | Exception handling present in `InstrumentVisitor::registerDetector` is not good from a funtional or performance point of view. I have cleaned the codebase of any duplicates in IDFs. However we do need to consider the fact that saved processed nexus files will contain legacy IDFs which would not be backwards compatible. |
| Limitations of RotateInstrumentComponent | L | | I'm not 100% on this requirement, but it would be very easy to give this possibility | 

## Discussions

Items discussed with Jon Taylor 21st September 2017. Priorities associated with Major items. Scanning any Component identified as the first next big item to tackle, to coincide with work at ILL.


