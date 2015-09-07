Instrument Geometry v1 Features
===============================

After a performance analysis (insert link to document), it was found that as much as 30% of the time of some reduction
pipelines is concerned with querying something about the instrument geometry. An agreement was made that we should
look into the design of the instrument geometry as a whole with the view of implementing an improved design that can
address performance concerns along with allowing us to better deal with geometries we are not bale to handle so well,
e.g. indirect.

### Current Features

This document aims to capture the features of the current instrument framework that a new system would need to
be able to handle. Currently we can

* load from XML
* create a 3D representation with OpenGL
* share a "base" instrument + changes (pos, rot, parameters) on a per-workspace level
* attach arbitrary parameters (bool, int double, string, fitting) to components (specifiable in source description) on a per-workspace level
* load/save to processed format
* handle components with an arbitrary shape defined by CSG (constructive solid geometry)
* define a reference frame
* define a instrument as a tree of components, possibly containing sub-assemblies
* define higher-level detector types, e.g. `RectangularDetector`
* lookup `Detector` objects via IDs
* retrieve source, sample components
