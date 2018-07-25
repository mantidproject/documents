# Instrument Ray Tracer 2.0
## Design Document

## Introduction
The current implementation of `InstrumentRayTracer` works off the orginal `Instrument` API and not the `Instrument 2.0` layers, such as `ComponentInfo`. Due to this, there is a dependency on `Instrument` in `Peak` and as such it is currently not possible to move away from using this legacy API. 

The intention is to stop developers needing access to the `Instrument` API and instead steer them towards using the new `Geometry` and `Beamline` layers as mentioned above.

The goal of this document is to outline a plan for the new `InstrumentRayTracer` and to remove any calls to the legacy API. The areas of discussion in this document include:

 * What to have in the new implementation of `InstrumentRayTracer`
 * How to incorporate some of the functionality of `ComponentInfo` into the new implementation 
 * How to roll out these new breaking changes
 * What a possible API would look like
 * What changes would have to be made to the code base
 * How to ensure that performance is good enough
 
