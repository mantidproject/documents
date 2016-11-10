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

This sets properties in the Reducer: class attribute :`Reducer.reduction_properties`.

**Script 2:**

```python
Reduce()
# Or without executing algorithms
ReductionSingleton().pre_process()
```
`ReductionSingleton().pre_process()` does not execute any of the algorithms:
 - Just sets properties in the `PropertyManagerDataService`.

Note in `ReductionSingleton().set_instrument`:
```
setup_algorithm="SetupHFIRReduction"
reduction_algorithm="HFIRSANSReduction")
```

The `setup_algorithm="SetupHFIRReduction"` is now instantiated and all the properties defined by that algorithm whose values exist in `Reducer.reduction_properties` are set and the algorithm called.

E.g. we set:
`reduction_properties["Normalisation"] = "Timer"`
The `SetupHFIRReduction` has an input property called `Normalisation` whose value assigned will be `Timer`


### Dump the properties:

```python

'''
Dummy setup
'''
import mantid
from mantid.simpleapi import *
from reduction_workflow.instruments.sans.hfir_command_interface import *

BIOSANS()
AppendDataFile(["/home/rhf/Documents/SANS/BioSans/BioSANS_exp270_scan0000_0001.xml"])
Reduce()

# This line is important and should always be used to validate the options above.
ReductionSingleton().pre_process()


'''
Print properties after SetupSwans...
'''



PropertyManagerDataService
i = PropertyManagerDataService.Instance()
property_name = i.getObjectNames()[0]
s = i[property_name]

for algo_name in s.keys():
	algo = s[algo_name]
	print algo.name, '::', algo.value
	try:
		for key in algo.value.keys():
			print '\t', key, '->', algo.value[key].value
	except:
		pass

```

Output:
```

InstrumentName :: HFIRSANS
ProcessInfo :: 
OutputDirectory :: 
LoadAlgorithm :: {"name":"HFIRLoad","properties":{"OutputWorkspace":"__TMP0x7fc8e00272e0"},"version":1}

        Filename -> 
        OutputWorkspace -> None
        NoBeamCenter -> False
        BeamCenterX -> 8.98846567431e+307
        BeamCenterY -> 8.98846567431e+307
        SampleDetectorDistance -> 8.98846567431e+307
        SampleDetectorDistanceOffset -> 8.98846567431e+307
        Wavelength -> 8.98846567431e+307
        WavelengthSpread -> 0.1
        OutputMessage -> 
        ReductionProperties -> __sans_reduction_properties
DefaultDarkCurrentAlgorithm :: {"name":"HFIRDarkCurrentSubtraction","properties":{"OutputWorkspace":"__TMP0x7fc8e1967800","ReductionProperties":"__reduction_parameters_nP9lQ"},"version":1}

        InputWorkspace -> None
        Filename -> 
        OutputWorkspace -> None
        PersistentCorrection -> True
        ReductionProperties -> __reduction_parameters_nP9lQ
        OutputDarkCurrentWorkspace -> None
        OutputMessage -> 
SANSSolidAngleCorrection :: {"name":"SANSSolidAngleCorrection","properties":{"OutputWorkspace":"__TMP0x7fc8e19681c0"},"version":1}

        InputWorkspace -> None
        OutputWorkspace -> None
        DetectorTubes -> False
        DetectorWing -> False
        OutputMessage -> 
        ReductionProperties -> __sans_reduction_properties
NormaliseAlgorithm :: {"name":"HFIRSANSNormalise","properties":{"NormalisationType":"Timer","OutputWorkspace":"__TMP0x7fc8e1969960"},"version":1}

        InputWorkspace -> None
        NormalisationType -> Timer
        OutputWorkspace -> None
        OutputMessage -> 
TransmissionNormalisation :: Timer
MaskAlgorithm :: {"name":"SANSMask","properties":{"Facility":"HFIR","MaskedEdges":""},"version":1}

        Facility -> HFIR
        Workspace -> None
        MaskedDetectorList -> []
        MaskedEdges -> []
        MaskedComponent -> 
        MaskedFullComponent -> 
        MaskedSide -> None
        OutputMessage -> 
IQAlgorithm :: {"name":"SANSAzimuthalAverage1D","properties":{"Binning":"","ComputeResolution":"1","OutputWorkspace":"__TMP0x7fc8e196dc10","ReductionProperties":"__reduction_parameters_nP9lQ"},"version":1}

        InputWorkspace -> None
        Binning -> []
        NumberOfBins -> 100
        LogBinning -> False
        AlignWithDecades -> False
        NumberOfSubpixels -> 1
        ErrorWeighting -> False
        ComputeResolution -> True
        ReductionProperties -> __reduction_parameters_nP9lQ
        OutputWorkspace -> None
        NumberOfWedges -> 2
        WedgeAngle -> 30.0
        WedgeOffset -> 0.0
        OutputMessage -> 
IQXYAlgorithm :: {"name":"EQSANSQ2D","properties":null,"version":1}

        InputWorkspace -> None
        OutputWorkspace -> 
        NumberOfBins -> 100
        OutputMessage -> 
SetupAlgorithm :: {"name":"SetupHFIRReduction","properties":{"Normalisation":"Timer","OutputMessage":"HFIR reduction options set","ReductionProperties":"__reduction_parameters_nP9lQ"},"version":1}

        SampleDetectorDistance -> 8.98846567431e+307
        SampleDetectorDistanceOffset -> 8.98846567431e+307
        SolidAngleCorrection -> True
        DetectorTubes -> False
        DetectorWing -> False
        Wavelength -> 8.98846567431e+307
        WavelengthSpread -> 0.1
        BeamCenterMethod -> None
        BeamCenterX -> 8.98846567431e+307
        BeamCenterY -> 8.98846567431e+307
        BeamCenterFile -> 
        BeamRadius -> 8.98846567431e+307
        Normalisation -> Timer
        DarkCurrentFile -> 
        SensitivityFile -> 
        MinEfficiency -> 8.98846567431e+307
        MaxEfficiency -> 8.98846567431e+307
        UseDefaultDC -> True
        SensitivityDarkCurrentFile -> 
        SensitivityBeamCenterMethod -> None
        SensitivityBeamCenterX -> 8.98846567431e+307
        SensitivityBeamCenterY -> 8.98846567431e+307
        SensitivityBeamCenterFile -> 
        SensitivityBeamCenterRadius -> 8.98846567431e+307
        OutputSensitivityWorkspace -> None
        TransmissionMethod -> Value
        TransmissionValue -> 8.98846567431e+307
        TransmissionError -> 8.98846567431e+307
        TransmissionBeamRadius -> 3.0
        TransmissionSampleDataFile -> 
        TransmissionEmptyDataFile -> 
        TransmissionBeamCenterMethod -> None
        TransmissionBeamCenterX -> 8.98846567431e+307
        TransmissionBeamCenterY -> 8.98846567431e+307
        TransmissionBeamCenterFile -> 
        TransSampleSpreaderFilename -> 
        TransDirectSpreaderFilename -> 
        TransSampleScatteringFilename -> 
        TransDirectScatteringFilename -> 
        SpreaderTransmissionValue -> 1.0
        SpreaderTransmissionError -> 0.0
        TransmissionDarkCurrentFile -> 
        TransmissionUseSampleDC -> True
        ThetaDependentTransmission -> True
        BackgroundFiles -> 
        BckTransmissionMethod -> Value
        BckTransmissionValue -> 8.98846567431e+307
        BckTransmissionError -> 8.98846567431e+307
        BckTransmissionBeamRadius -> 3.0
        BckTransmissionSampleDataFile -> 
        BckTransmissionEmptyDataFile -> 
        BckTransmissionBeamCenterMethod -> None
        BckTransmissionBeamCenterX -> 8.98846567431e+307
        BckTransmissionBeamCenterY -> 8.98846567431e+307
        BckTransmissionBeamCenterFile -> 
        BckTransSampleSpreaderFilename -> 
        BckTransDirectSpreaderFilename -> 
        BckTransSampleScatteringFilename -> 
        BckTransDirectScatteringFilename -> 
        BckSpreaderTransmissionValue -> 1.0
        BckSpreaderTransmissionError -> 0.0
        BckTransmissionDarkCurrentFile -> 
        BckThetaDependentTransmission -> True
        SampleThickness -> 8.98846567431e+307
        MaskedDetectorList -> []
        MaskedEdges -> []
        MaskedComponent -> 
        MaskedSide -> None
        MaskedFullComponent -> 
        AbsoluteScaleMethod -> None
        AbsoluteScalingFactor -> 1.0
        AbsoluteScalingReferenceFilename -> 
        AbsoluteScalingBeamDiameter -> 0.0
        AbsoluteScalingAttenuatorTrans -> 1.0
        AbsoluteScalingApplySensitivity -> False
        DoAzimuthalAverage -> True
        IQBinning -> []
        IQNumberOfBins -> 100
        IQLogBinning -> False
        IQAlignLogWithDecades -> False
        NumberOfSubpixels -> 1
        ErrorWeighting -> False
        NumberOfWedges -> 2
        WedgeAngle -> 30.0
        WedgeOffset -> 0.0
        Do2DReduction -> True
        IQ2DNumberOfBins -> 100
        ProcessInfo -> 
        OutputDirectory -> 
        OutputMessage -> HFIR reduction options set
        ReductionProperties -> __reduction_parameters_nP9lQ

```
