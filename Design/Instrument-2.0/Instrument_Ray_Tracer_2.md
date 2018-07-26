# Instrument Ray Tracer 2.0
## Design Document

## Introduction
The current implementation of `InstrumentRayTracer` works off the orginal `Instrument` API and not the `Instrument 2.0` layers, such as `ComponentInfo`, `DetectorInfo` and `SpectrumInfo`. Due to this, there is a dependency on `Instrument` in `Peak` and as such it is currently not possible to move away from using this legacy API. The intention is to stop developers needing access to the `Instrument` API and instead steer them towards using the new `Geometry` and `Beamline` layers as mentioned above.

## Overview
The goal of this document is to outline a plan for the new `InstrumentRayTracer` and to figure out how to move away from making any calls to the legacy API. The areas of discussion in this document include:

 * Implementation details of `InstrumentRayTracer 2.0`
   * Possible new methods
   * Reuse of original code
   * Usage of new implementation
     
 * Using the functionality of `ComponentInfo`
   * Determining what code would actually be useful
   * Incorporating it into the new implementation
   
 * Rolling out the changes
   * Figuring out what a possible API would look like 
   * Outlining what changes would have to be made to the code base
   * How to ensure that performance is good enough
 
## Implementation Details of `InstrumentRayTracer 2.0`
One idea for the implementation of `InstrumentRayTracer 2.0` is to have as many of the old methods from `InstrumentRayTracer` as possible carried over. This is would be a good way to proceed as it would hopefully mean that there will not be as many breaking changes to worry about. The methods to be replaced would be where the legacy API calls are made - i.e. anything that uses `Instrument` could be modified so that the new `Geometry` and `Beamline` layers are used instead. It seems that using the functionality of `ComponentInfo` where possible might be the best way to proceed - please see the section below for more details.

## Using the Functionality of `ComponentInfo`
The newly exposed `ComponentInfo` layer is accessible from a workspace - examples of usage can be found [here](). Possible methods that could be used in `InstrumentRayTracer 2.0` might include:

## Rolling out the Changes

