# ORNL_SANS_Reducer

## TL;TR;

Documentation: http://docs.mantidproject.org/nightly/concepts/ORNL_SANS_Reduction.html

## 

Code is in the folder:
`mantid/scripts/reduction_workflow`

## Reduction script

imports:
```python
from reduction_workflow.instruments.sans.hfir_command_interface import *
```

Code example:
```python
GPSANS()
SetSampleDetectorDistance(1802.5)
# (....)
Reduce()
```

## Code

https://github.com/mantidproject/mantid/blob/master/scripts/reduction_workflow/instruments/sans/hfir_command_interface.py

Sets poperties on `ReductionSingleton()`, e.g.:
```python
ReductionSingleton().reduction_properties["BeamCenterFile"] = datafile
```



`ReductionSingleton()` is here:
https://github.com/mantidproject/mantid/blob/master/scripts/reduction_workflow/command_interface.py

The `ReductionSingleton()` contains an instance of `Reducer`

`Reducer` is here: https://github.com/mantidproject/mantid/blob/master/scripts/reduction_workflow/reducer.py


In the end `Reduce()` calls `ReductionSingleton().reduce()` which in turn calls `Reducer.reduce()`.


### Example:

**Script 1:**
```
BIOSANS()
```
Code in `hfir_command_interface`:
```python
def BIOSANS():
    Clear()
    ReductionSingleton().set_instrument("BIOSANS",
                                        setup_algorithm="SetupHFIRReduction",
                                        reduction_algorithm="HFIRSANSReduction")
    TimeNormalization()
    SolidAngle()
    AzimuthalAverage()

def TimeNormalization():
    ReductionSingleton().reduction_properties["Normalisation"] = "Timer"

def SolidAngle(detector_tubes=False, detector_wing=False):
    ReductionSingleton().reduction_properties["SolidAngleCorrection"] = True
    ReductionSingleton().reduction_properties["DetectorTubes"] = detector_tubes
    ReductionSingleton().reduction_properties["DetectorWing"] = detector_wing

def AzimuthalAverage(
        binning=None,
        suffix="_Iq",
        error_weighting=False,
        n_bins=100,
        n_subpix=1,
        log_binning=False,
        align_log_with_decades=False):
    # Suffix is no longer used but kept for backward compatibility
    ReductionSingleton().reduction_properties["DoAzimuthalAverage"] = True
    if binning is not None:
        ReductionSingleton().reduction_properties["IQBinning"] = binning
    elif "IQBinning" in ReductionSingleton().reduction_properties:
        del ReductionSingleton().reduction_properties["IQBinning"]
    ReductionSingleton().reduction_properties["IQNumberOfBins"] = n_bins
    ReductionSingleton().reduction_properties["IQLogBinning"] = log_binning
    ReductionSingleton().reduction_properties["NumberOfSubpixels"] = n_subpix
    ReductionSingleton().reduction_properties[
        "ErrorWeighting"] = error_weighting
    ReductionSingleton().reduction_properties[
        "IQAlignLogWithDecades"] = align_log_with_decades

```

This all sets properties in the Reducer: `Reducer.reduction_properties`.

**Script 2:**

```python
Reduce()
# Or without executing algorithms
ReductionSingleton().pre_process()
```
`ReductionSingleton().pre_process()` does not execute any of the algorithms:
 - Just sets properties in the `PropertyManagerDataService`.
 -





Note in `ReductionSingleton().set_instrument`:
```
setup_algorithm="SetupHFIRReduction"
reduction_algorithm="HFIRSANSReduction")
```


`SetupHFIRReduction` is a C++ algorithm that accepts 


