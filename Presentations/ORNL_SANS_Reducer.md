# ORNL SANS Reducer

## Python interface overview

Documentation: http://docs.mantidproject.org/nightly/concepts/ORNL_SANS_Reduction.html

The code is in the folder:
`mantid/scripts/reduction_workflow`

### Reduction script

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

### Code

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



![](https://s22.postimg.org/f1ykyjlk1/Diagram1.png)


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

This sets properties in the Reducer attribute :`Reducer.reduction_properties`.

**Script 2.1:**

Last call:

```python
# Or without executing algorithms
ReductionSingleton().pre_process()
```
`ReductionSingleton().pre_process()` does not execute any of the algorithms. Just call `setup_algorithm` which sets properties (name - value) in the `PropertyManagerDataService`.

Note in `ReductionSingleton().set_instrument`:
```
setup_algorithm="SetupHFIRReduction"
reduction_algorithm="HFIRSANSReduction")
```

The `setup_algorithm="SetupHFIRReduction"` is now instantiated and all the properties defined by that algorithm, whose values exist in `Reducer.reduction_properties`, are set. Finnaly the algorithm is executed.

E.g., if the `Reducer` has a property:
- `reduction_properties["Normalisation"] = "Timer"`
and the `SetupHFIRReduction` has an input property called `Normalisation`, that poperty will be set with the value `Timer`.

The `setup_algorithm` is a CPP algorith with some logic inside. It also calls algorithms.

```
$ find Framework/ -iname "*.cpp" | grep Setup
Framework/WorkflowAlgorithms/src/SetupEQSANSReduction.cpp
Framework/WorkflowAlgorithms/src/SetupHFIRReduction.cpp
Framework/WorkflowAlgorithms/src/SetupILLD33Reduction.cpp
```

**Script 2.2:**

Last call:

```python
Reduce()
```

The `Reduce()` calls the `Reducer.reduce()`. The latter calls `Reducer.pre_process()` to set the properties in the `PropertyManagerDataService` and starts the Reduction process.

`Reducer.reduce()` intantiates `reduction_algorithm="HFIRSANSReduction"` and sets the input properties of the `reduction_algorithm` including the name of the `ReductionProperties` set by `Reducer.pre_process()`.

`HFIRSANSReduction` is here: https://github.com/mantidproject/mantid/blob/master/Framework/PythonInterface/plugins/algorithms/WorkflowAlgorithms/HFIRSANSReduction.py

It goes through all the properties and executes algorithms and sets the respective properties. See below.


### Dump the properties:

Reduce one file with all defaults:

```python
'''
Dummy setup
'''
import mantid
from mantid.simpleapi import *
from reduction_workflow.instruments.sans.hfir_command_interface import *

BIOSANS()
AppendDataFile(["/home/rhf/Documents/SANS/BioSans/BioSANS_exp270_scan0000_0001.xml"])

# I just want to see the Properties set, no need for algorithm execution:
# Reduce()
ReductionSingleton().pre_process()
```

Let's print the properties in the PropertyManager:

```
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
        PersistentCorrection -> True bill hamilton
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

## Adding a new instrument

* Add the new instrument specification command to the corresponding SNS / HFIR command interface:

- HFIR: https://github.com/mantidproject/mantid/blob/master/scripts/reduction_workflow/instruments/sans/hfir_command_interface.py
- SNS: https://github.com/mantidproject/mantid/blob/master/scripts/reduction_workflow/instruments/sans/sns_command_interface.py	

```
def <instrument name>():
    Clear()
    ReductionSingleton().set_instrument("<instrument name>",
                                        setup_algorithm="Setup<instrument name>Reduction",
                                        reduction_algorithm="<HFIRSANSReduction|SANSReduction>")
    # Default operations that should be performed by the Reducer
    TimeNormalization()
    SolidAngle()
    AzimuthalAverage()
```

* Eventualy add new functionality

```
def <directive name>():
    ReductionSingleton().reduction_properties["<key>"] = "<value>"
```

* Make the "<key>" as input property in the `setup_algorithm`

For example, if in the command interface there's:

```python
def TimeNormalization():
    ReductionSingleton().reduction_properties["Normalisation"] = "Timer"

def MonitorNormalization():
    ReductionSingleton().reduction_properties["Normalisation"] = "Monitor"

def NoNormalization():
    ReductionSingleton().reduction_properties["Normalisation"] = "None"
```

In the setup algorithm the following definitions must exist:


```c++

void SetupHFIRReduction::init() {
  
  //(.....)
  
  // Normalisation
  std::vector<std::string> incidentBeamNormOptions;
  incidentBeamNormOptions.emplace_back("None");
  incidentBeamNormOptions.emplace_back("Monitor");
  incidentBeamNormOptions.emplace_back("Timer");
  this->declareProperty(
      "Normalisation", "Monitor",
      boost::make_shared<StringListValidator>(incidentBeamNormOptions),
      "Options for data normalisation");

void SetupHFIRReduction::exec() {
  
  //(.....)
  
  // Normalization
  const std::string normalization = getProperty("Normalisation");
  
  if (!boost::contains(normalization, "None")) {
    IAlgorithm_sptr normAlg = createChildAlgorithm("HFIRSANSNormalise");
    normAlg->setProperty("NormalisationType", normalization);
    auto normAlgProp = make_unique<AlgorithmProperty>("NormaliseAlgorithm");
    normAlgProp->setValue(normAlg->toString());
    reductionManager->declareProperty(std::move(normAlgProp));
    reductionManager->declareProperty(
        Kernel::make_unique<PropertyWithValue<std::string>>(
            "TransmissionNormalisation", normalization));
  } else
    reductionManager->declareProperty(
        make_unique<PropertyWithValue<std::string>>("TransmissionNormalisation",
                                                    "Timer"));
  
```


Existing setups:
```
$ find ./Framework/ -iname "Setup*.cpp"
./Framework/WorkflowAlgorithms/src/SetupEQSANSReduction.cpp
./Framework/WorkflowAlgorithms/src/SetupHFIRReduction.cpp
./Framework/WorkflowAlgorithms/src/SetupILLD33Reduction.cpp
```

