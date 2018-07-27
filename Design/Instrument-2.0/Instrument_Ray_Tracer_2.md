# Instrument Ray Tracer 2.0
## Design Document

## Introduction
The current implementation of [`InstrumentRayTracer`](https://github.com/mantidproject/mantid/blob/master/Framework/Geometry/inc/MantidGeometry/Objects/InstrumentRayTracer.h#L56) works off the orginal `Instrument` API and not the `Instrument 2.0` layers, such as `ComponentInfo`, `DetectorInfo` and `SpectrumInfo`. Due to this, there is a dependency on `Instrument` in [`Peak`](https://github.com/mantidproject/mantid/blob/master/Framework/DataObjects/inc/MantidDataObjects/Peak.h#L182) and as such it is currently not possible to move away from using this legacy API. The intention is to stop developers needing access to the `Instrument` API and instead steer them towards using the new `Geometry` and `Beamline` layers as mentioned above.

The goal of this document is to outline a plan for `InstrumentRayTracer 2.0` and to figure out how to move away from making any calls to the legacy API.
 
## `InstrumentRayTracer 2.0` Methods

#### Reuse of Original Code
One idea for the implementation of `InstrumentRayTracer 2.0` is to have many of the old methods from `InstrumentRayTracer` carried over. This is would be a good way to proceed as it would hopefully mean that there will not be as many breaking changes to worry about. The methods to be replaced would be where the legacy API calls are made - i.e. anything that uses `Instrument` could be modified so that the new `Geometry` and `Beamline` layers are used instead. Methods headers that could be kept the same include:

 * `void trace(const Kernel::V3D &dir) const`
 * `void traceFromSample(const Kernel::V3D &dir) const`
 * `Links getResults() const`
 * `IDetector_const_sptr getDetectorResult() const`
 * `void fireRay(Track &testRay) const`

#### Possible New Methods
Although the headers do not explicity have anything to do with `Instrument`, many of the method bodies make use of the member variable `m_instrument` to carry out various tasks. This variable is created and initialised in the constructor. From looking at the implementation in [`InstrumentRayTracer.cpp`](https://github.com/BhuvanBezawada/mantid/blob/master/Framework/Geometry/src/Objects/InstrumentRayTracer.cpp), it seems that the constructor is the one place where there is a dependence on `Instrument` and this is probably the one area that needs to be fully rewritten. 

## The Constructor
To rewrite the constructor it may be enough to pass in a `const` reference to a `ComponentInfo` object. This would ensure that the `InstrumentRayTracer` works as intended but there is a chance that undefined behaviour could arise if scoping is used.

```c++

// This example would work as intended
InstrumentRayTracer2* ptr;
auto ws = CreateWorkspace();
ptr = new InstrumentRayTracer2(ws.componentInfo);
ptr.trace(V3D(0,0,0));

// With the following scoping, there would be undefined behaviour
InstrumentRayTracer2* ptr;
{ 
  auto ws = CreateWorkspace();
  ptr = new InstrumentRayTracer2(ws.componentInfo);
}
ptr.trace(V3D(0,0,0));

```

#### `ComponentInfo` Copy Implementation 
One other possible implementation could be that a copy of a `ComponentInfo` object is passed to the constructor. ComponentInfo is also cheap to copy because in the [copy constructor](https://github.com/mantidproject/mantid/blob/8ec802f56c5db2261a0f9502f30f67fe42530d62/Framework/Geometry/src/Instrument/ComponentInfo.cpp#L88) shared pointers are created to the orginal copy's data. This should also ensure that the undefined behaviour mentioned above should not happen.

#### Classless Implementation
Another idea could be to make the methods of `InstrumentRayTracer 2.0` a set of free functions. Each of the functions would need to take in a `ComponentInfo` and any other variables required to carry out the correct procedure. This approach would definitely eliminate the passing around of the `InstrumentRayTracer` object that currently happens. Also, there are not many variables that would need to be passed to each of the methods meaning calls to the functions would remain largely the same.

## Usage of `ComponentInfo`
If all goes well with the plan to use `ComponentInfo` where possible, it is very likely that the code to use `InstrumentRayTracer 2.0` will be very similar to the current method of using it. Possible methods from `ComponentInfo` that could be used in `InstrumentRayTracer 2.0` might include:

 * `componentInfo.getSource()` in `void InstrumentRayTracer::trace(const V3D &dir) const`
 * `componentInfo.getSample()` in `void InstrumentRayTracer::traceFromSample(const V3D &dir) const`

It should not be too difficult to reuse the code from `ComponentInfo` as it should just be a case of making sure the `ComponentInfo` class is accessible from `InstrumentRayTracer 2.0`.

## Rolling out the Changes
Before rolling out any changes, it is probably a good idea to develop a set of tests exclusively for this new class. Some tests (especially for methods that do not make calls to the legacy API) could probably be based on the existing tests with a few alterations. 

#### Changes to the Code Base
The best way to completely move away from using `InstrumentRayTracer` (and not completely break everything) would be to start with a selection of "testing files" that currently use the `InstrumentRayTracer` e.g `Peak` and begin to change them one by one. Once all of those files are in working order it would provide enough confidence in the new implementation and all the other files can then be updated.

#### Performance Issues
To ensure that the new implementation performs just as well as the existing version, benchmarking tools could be used to record the current performance and this can be used as a target for the new implementation. It does not seem that there would be any major changes to performance since much of the code should remain somewhat similar. If anything, using `ComponentInfo` should reduce the number of function calls being made. 

## Conclusion
Based on the options outlined above, it seems that the best approach may be to make `InstrumentRayTracer 2.0` a class based implementation. The constructor should take in a copy of a `ComponentInfo` object. The reasoning behind this is that the current implementation is class based and keeping the new version familiar in design might be good for end users. Also, there should not be any extra overhead in terms of performance since the implementation strategy is similar to the previous version.
