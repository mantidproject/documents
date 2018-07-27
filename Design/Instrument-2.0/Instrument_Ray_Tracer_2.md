# Instrument Ray Tracer 2.0
## Design Document

## Introduction
The current implementation of [`InstrumentRayTracer`](https://github.com/mantidproject/mantid/blob/master/Framework/Geometry/inc/MantidGeometry/Objects/InstrumentRayTracer.h#L56) works off the orginal `Instrument` API and not the `Instrument 2.0` layers, such as `ComponentInfo`, `DetectorInfo` and `SpectrumInfo`. Due to this, there is a dependency on `Instrument` in [`Peak`](https://github.com/mantidproject/mantid/blob/master/Framework/DataObjects/inc/MantidDataObjects/Peak.h#L182) and as such it is currently not possible to move away from using this legacy API. 

The intention is to stop developers needing access to the `Instrument` API and instead steer them towards using the new `Geometry` and `Beamline` layers as mentioned above. The layers provided by `Instrument 2.0` are much more efficient and the read performance is much better. It makes sense to start re-implementing code to make full use of the new layers and this move can help to optimise much of the code base. Also the `ComponentInfo` layer has been designed in such a way that the majority (if not all) of the functionality provided by `Instrument` is readily available via `ComponentInfo`.

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
One other possible implementation could be that a copy of a `ComponentInfo` object is passed to the constructor. `ComponentInfo` is also cheap to copy because in this [copy constructor](https://github.com/mantidproject/mantid/blob/bc136744a7edd8306c86e5176e5625d337852994/Framework/Beamline/src/ComponentInfo.cpp#L28) shared pointers are created to the orginal copy's data. This should also ensure that the undefined behaviour mentioned above should not happen.
#### Classless Implementation

Another idea could be to make the methods of `InstrumentRayTracer 2.0` a set of free functions. Each of the functions would need to take in a `ComponentInfo` and any other variables required to carry out the correct procedure. This approach would definitely eliminate the passing around of the `InstrumentRayTracer` object that currently happens. Also, there are not many variables that would need to be passed to each of the methods meaning calls to the functions would remain largely the same.

## Usage of `ComponentInfo`
If all goes well with the plan to use `ComponentInfo` where possible, it is very likely that the code to use `InstrumentRayTracer 2.0` will be very similar to the current method of using it. Possible methods from `ComponentInfo` that could be used in `InstrumentRayTracer 2.0` might include:

 * `componentInfo.getSource()` in `void InstrumentRayTracer::trace(const V3D &dir) const`
 * `componentInfo.getSample()` in `void InstrumentRayTracer::traceFromSample(const V3D &dir) const`
 * `bool isDetector(const size_t componentIndex) const in IDetector_const_sptr InstrumentRayTracer::getDetectorResult() const`
 

Missing methods:
 * `getComponentByIndex()` for `IDetector_const_sptr InstrumentRayTracer::getDetectorResult() const`
 * `isMonitor()` for `IDetector_const_sptr InstrumentRayTracer::getDetectorResult() const`

It should not be too difficult to reuse the code from `ComponentInfo` as it should just be a case of making sure the `ComponentInfo` class is accessible from `InstrumentRayTracer 2.0`.

## Rolling out the Changes
Before rolling out any changes, it is probably a good idea to develop a set of tests exclusively for this new class. Some tests (especially for methods that do not make calls to the legacy API) could probably be based on the existing tests with a few alterations. 

#### Changes to the Code Base
The best way to completely move away from using `InstrumentRayTracer` (and not completely break everything) would be to start with a selection of "testing files" that currently use the `InstrumentRayTracer` e.g `Peak` and begin to change them one by one. Once all of those files are in working order it would provide enough confidence in the new implementation and all the other files can then be updated.

#### Performance Issues
To ensure that the new implementation performs just as well as the existing version, benchmarking tools could be used to record the current performance and this can be used as a target for the new implementation. It does not seem that there would be any major changes to performance since much of the code should remain somewhat similar. If anything, using `ComponentInfo` should reduce the number of function calls being made. 

## Conclusion
Based on the options outlined above, it seems that the best approach may be to make `InstrumentRayTracer 2.0` a classless implementation. There are a number of reasons for this choice: 
 
 * The same operations can be achieved in far fewer lines of code.
 * There is no need to worry about copying `ComponentInfo`
 * The internal code will be just as efficient
 * No need to pass around `InstrumentRayTracer` objects
 
Much of the core code should remain the same, so efficiency and performance should not be negatively affected in any way.

## Relevant Files
[InstrumentRayTracer.h](https://github.com/mantidproject/mantid/blob/f60045bd5ed646dbb4f203d21f2cd17420e0d705/Framework/Geometry/inc/MantidGeometry/Objects/InstrumentRayTracer.h)

[InstrumentRayTracer.cpp](https://github.com/mantidproject/mantid/blob/98a6c146c2e58d943d48deb1c2b996a023808f49/Framework/Geometry/src/Objects/InstrumentRayTracer.cpp)

[InstrumentRayTracerTest.h (DataHandling)](https://github.com/mantidproject/mantid/blob/852c39f53dc5abc2c83e88618040b4118f13b8f1/Framework/DataHandling/test/InstrumentRayTracerTest.h)

[InstrumentRayTracerTest.h (Geometry)](https://github.com/mantidproject/mantid/blob/bf795302a51bdd24cd2d86b8fb02930e35dee9e8/Framework/Geometry/test/InstrumentRayTracerTest.h)

[RayTracerTester.cpp](https://github.com/mantidproject/mantid/blob/98a6c146c2e58d943d48deb1c2b996a023808f49/Framework/Algorithms/src/RayTracerTester.cpp)

[MockObjects.h](https://github.com/mantidproject/mantid/blob/ab3e090c829c8696810d2986699f30cf9c9a7fb1/Framework/Geometry/test/MockObjects.h)

[DetectorSearcher.h](https://github.com/mantidproject/mantid/blob/f60045bd5ed646dbb4f203d21f2cd17420e0d705/Framework/API/inc/MantidAPI/DetectorSearcher.h)

[DetectorSearcher.cpp](https://github.com/mantidproject/mantid/blob/11066e45b6734332e954d3c1c4e099b61c9b5d5f/Framework/API/src/DetectorSearcher.cpp)

[IPeak.h](https://github.com/mantidproject/mantid/blob/ab3e090c829c8696810d2986699f30cf9c9a7fb1/Framework/Geometry/inc/MantidGeometry/Crystal/IPeak.h)

[Peak.h](https://github.com/mantidproject/mantid/blob/ab3e090c829c8696810d2986699f30cf9c9a7fb1/Framework/DataObjects/inc/MantidDataObjects/Peak.h)

[Peak.cpp](https://github.com/mantidproject/mantid/blob/ab3e090c829c8696810d2986699f30cf9c9a7fb1/Framework/DataObjects/src/Peak.cpp)

[FindPeaksMD.h](https://github.com/mantidproject/mantid/blob/f55473e499f8c28ffd65bc66d6169e9540aeb16d/Framework/MDAlgorithms/inc/MantidMDAlgorithms/FindPeaksMD.h)

[FindPeaksMD.cpp](https://github.com/mantidproject/mantid/blob/9d79448d8e45fd9c3b60e71a75aa26d26a7c6939/Framework/MDAlgorithms/src/FindPeaksMD.cpp)

[PredictPeaks.cpp](https://github.com/mantidproject/mantid/blob/5d4192c739fe8bd5bcd92f984c7a983947fbd9ae/Framework/Crystal/src/PredictPeaks.cpp)

[PredictFractionalPeaks.cpp](https://github.com/mantidproject/mantid/blob/e4a20712985c48c2c42bd6b4ed6733491fddb1fa/Framework/Crystal/src/PredictFractionalPeaks.cpp)

[CompAssembly.h](https://github.com/mantidproject/mantid/blob/f60045bd5ed646dbb4f203d21f2cd17420e0d705/Framework/Geometry/inc/MantidGeometry/Instrument/CompAssembly.h)

[CompAssembly.cpp](https://github.com/mantidproject/mantid/blob/63d508e82d15ec501d4c3be092d5e958ae994e73/Framework/Geometry/src/Instrument/CompAssembly.cpp)

[ObjCompAssembly.cpp](https://github.com/mantidproject/mantid/blob/c05188d521e922360b39b46443812d5856283fed/Framework/Geometry/src/Instrument/ObjCompAssembly.cpp)

[RectangularDetector.cpp](https://github.com/mantidproject/mantid/blob/bc136744a7edd8306c86e5176e5625d337852994/Framework/Geometry/src/Instrument/RectangularDetector.cpp)

[CMakeLists.txt](https://github.com/mantidproject/mantid/blob/8a5ddb4937b7486ce01480149dbffe1c3925647f/Framework/Geometry/CMakeLists.txt)
