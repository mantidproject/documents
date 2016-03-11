class: center, middle

# Data Processor Algorithms

What does it give me for free?

---

## Quick review of Algorithm

```python
def PyInit(self):
    # bunch of inconsistently named properties
    # mostly strings that are parsed in the PyExec

def PyExec(self):
    # as long of a function as you can imagine
```

---

## Did you know?

Grouping properties in the GUI

```python
def PyInit(self):
    self.declareProperty(MatrixWorkspaceProperty('InputWorkspace', '',
                                                 Direction.Input),\
                         doc="")
    self.declareProperty(FileProperty(name='InputFile',defaultValue='',
                                      action=FileAction.OptionalLoad,
				      extensions = ['_event.nxs']),
                         doc='')
    grp1 = 'Fancy Label'
    self.setPropertyGroup('InputWorkspace', grp1)
    self.setPropertyGroup('InputFile', grp1)
```

---

## Did you know?

Cross checking properties

```python
def validateInputs(self):
    issues = dict()

    if (not self.getProperty('InputWorkspace').isDefault()) \
            and (not self.getProperty('InputFile').isDefault()):
        issues['InputWorkspace'] = 'cannot set with "InputFile"'
        issues['InputFile'] = 'cannot set with "InputWorkspace"'

    return issues
```

...which runs before `PyExec`

---

## What is a `DataProcessorAlgorithm`?

* Base class for "workflow" algorithms
* Automatically handles nested history
* Intended to handle "common" use cases
* Helps with `PropertyManager` and chunking

---

## copyProperty

Copy a property from another algorithm including name, default value,
and documentation.

from [LoadEventAndCompress.init](https://github.com/mantidproject/mantid/blob/master/Framework/WorkflowAlgorithms/src/LoadEventAndCompress.cpp#L56)
```C
  // algorithms to copy properties from
  auto algLoadEventNexus =
      AlgorithmManager::Instance().createUnmanaged("LoadEventNexus");
  algLoadEventNexus->initialize();
  ...

  // declare properties
  copyProperty(algLoadEventNexus, "Filename");
  copyProperty(algLoadEventNexus, "OutputWorkspace");
  copyProperty(algDetermineChunking, "MaxChunkSize");
  declareProperty("CompressTOFTolerance", .01);
```

---

## mapPropertyName

Declare what a property is called in the algorithm and in the supplied
`PropertyManager` parameter

from [AlignAndFocusPowder.init](https://github.com/mantidproject/mantid/blob/411ba917b926f67def3784ee04ebd9a20019d759/Framework/WorkflowAlgorithms/src/AlignAndFocusPowder.cpp#L115)
```C
declareProperty(new ArrayProperty<double>("DMin"),
                "Minimum for Dspace axis. (Default 0.) ");
mapPropertyName("DMin", "d_min");
declareProperty(new ArrayProperty<double>("DMax"),
                "Maximum for Dspace axis. (Default 0.) ");
mapPropertyName("DMax", "d_max");
...
declareProperty("ReductionProperties", "__powdereduction", Direction::Input);
```

---

## mapPropertyName - What does this do?

In [DataProcessorAlgorithm](https://github.com/mantidproject/mantid/blob/f821234b70f872355f8be2a3735e17d00f31ff40/Framework/API/src/DataProcessorAlgorithm.cpp#L148)
```C
std::string
DataProcessorAlgorithm::getPropertyValue(const std::string &name) const {
  // explicitely specifying a property wins
  if (!isDefault(name)) {
    return Algorithm::getPropertyValue(name);
  }

  // return it if it is in the held property manager
  auto mapping = m_nameToPMName.find(name);
  if (mapping != m_nameToPMName.end()) {
    auto pm = this->getProcessProperties();
    if (pm->existsProperty(mapping->second)) {
      return pm->getPropertyValue(mapping->second);
    }
  }

  // let the parent class version win
  return Algorithm::getPropertyValue(name);
}
```

---

## determineChunk and loadChunk

[DataProcessor](https://github.com/mantidproject/mantid/blob/f821234b70f872355f8be2a3735e17d00f31ff40/Framework/API/src/DataProcessorAlgorithm.cpp#L194)
```C
ITableWorkspace_sptr
DataProcessorAlgorithm::determineChunk(const std::string &filename) {
  UNUSED_ARG(filename);

  throw std::runtime_error(
      "DataProcessorAlgorithm::determineChunk is not implemented");
}

MatrixWorkspace_sptr DataProcessorAlgorithm::loadChunk(const size_t rowIndex) {
  UNUSED_ARG(rowIndex);

  throw std::runtime_error(
      "DataProcessorAlgorithm::loadChunk is not implemented");
}
```

---

## Examples - C++:

* AccumulateMD
* AlignAndFocusPowder
* CalculateResolution
* CalculateSlits
* ComputeSensitivity
* ConvolutionFitSequential
* CreateMD
* CreateTransmissionWorkspaceAuto
* CutMD
* DgsReduction
* LoadEventAndCompress
* MuonProcess
* PeformIndexOperations
* ReflectometryReductionOneAuto
* ReflectometryWorkflowBase
* SANSBeamFluxCorrection
* SofQW

---

## Examples - Python:

* DetectorFloodWeighting
* ElasticWindowMultiple
* EVSDiffractionReduction
* ILLIN16BCalibration
* IndirectAnnulusAbsorption
* IndirectCalibration
* IndirectCylinderAbsorption
* IndirectFlatPlateAbsorption
* IndirectILLReduction
* IndirectResolution
* ISISIndirectDiffractionReduction
* ISISIndirectEnergyTransfer
* MSDFit
* MuscatSofQW
* PDToPDFgetN
* SANSFitShiftScale
* SANSStitch
* SNSPowderReduction
* SofQWMoments
* SwapWidths
* TOSCABankCorrection

---

background-image: url(algorithmstagcloud.png)
