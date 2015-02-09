##Peak Shape Problem

We cannot track how peaks have been integrated, or what the shape parameters used for the integration where. This makes it currently impossible
to represent SC peaks in a useful manner, or track histories of peak integration upon combination of sub-lists of PeaksWorkspaces.

##Solution Implemented

* Each Peak in Mantid has an shape
* Shape gets written upon Integration
* Shape records Algorithm and version of Algorithm used to perform the integration
* All shapes are written to and read from the processed NeXus format
* IntegratePeaksMD v1, IntegratePeaksMD v2, IntegrateEllipsoids are writing this information out now.

## Examples 

```python
PeaksLatticeFFT = IntegratePeaksMD(InputWorkspace=LabQ, PeakRadius=0.12,
    BackgroundOuterRadius=0.18,BackgroundInnerRadius=0.15,
    PeaksWorkspace=PeaksLatticeFFT)


shape = PeaksLatticeFFT.getPeak(0).getPeakShape()
print shape.toJSON()
```

```
{
   "algorithm_name" : "IntegratePeaksMD",
   "algorithm_version" : 2,
   "background_inner_radius" : 0.150,
   "background_outer_radius" : 0.180,
   "frame" : 1,
   "radius" : 0.120,
   "shape" : "spherical"
}
```

```python   
PeaksLatticeFFT = IntegrateEllipsoids(InputWorkspace=ws, PeaksWorkspace=PeaksLatticeFFT) 
    


shape = PeaksLatticeFFT.getPeak(0).getPeakShape()
print shape.toJSON()
```

```
{
   "algorithm_name" : "IntegrateEllipsoids",
   "algorithm_version" : -1,
   "background_inner_radius0" : 0.1569320366997004,
   "background_inner_radius1" : 0.1904709902029069,
   "background_inner_radius2" : 0.2009385702055810,
   "background_outer_radius0" : 0.1977219764573250,
   "background_outer_radius1" : 0.2399784099709861,
   "background_outer_radius2" : 0.2531667343589144,
   "direction0" : "-0.397112 0.592816 0.700622",
   "direction1" : "-0.674626 -0.706126 0.215095",
   "direction2" : "-0.622239 0.387241 -0.68034",
   "frame" : 1,
   "radius0" : 0.1569320366997004,
   "radius1" : 0.1904709902029069,
   "radius2" : 0.2009385702055810,
   "shape" : "ellipsoid"
}
```