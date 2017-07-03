# WorkspacePropertyWithIndex Type

This document relates to an algorithm property type which can be used to specify a workspace and desired input index type(s). Index translation will will be handled by the new `IndexInfo` (design [here](https://github.com/mantidproject/documents/blob/master/Design/spectrum_number_and_workspace_index_abstraction.md)) object internally. Badly unit tested code and inconsistencies in validating user indices would be absorbed by this type. This design complements `IndexInfo` and reinforces some of the design concepts. **Note**:This property is only related to situations where workspace index is required, it does not cater for applications that directly require SpectrumNumber of DetectorID for example.

## Motivation
The `IndexInfo` object recently included in the Mantid framework introduces a strict policy for the definition of and translations between index types. However, this has not yet been reflected at the algorithm property level. There is still user-facing confusion among index types. Algorithms inconsistently capture and use index types without a clear mechanism for defining them e.g spectrum number, spectrum index, workspace index, workspace id, detector index, detector id etc. This is compounded by the soon to be implemented MPI build of Mantid. Indices captured by algorithms must be translated in accordance with data partitioning across MPI ranks. The mechanism in place for this translation exists within *IndexInfo* `IndexInfo::makeIndexSet` but developers must manually make this translation upon obtaining a workspace property.

```cpp
MatrixWorkspace_sptr inputWs = getProperty("InputWorkspace");
std::vector<int> indices = getProperty("WorkspaceIndices");
auto indexSet = inputWs->indexInfo().makeIndexSet(indices);
```
 A developer could easily miss this step which would have undefined results in an MPI situation. It would be more sensible to abstract this away from the developer. The `WorkspacePropertyWithIndex` type will obviate the need to perform this translation by doing this internally and returning the correct index set for use by the algorithm. In summary, this property type presents the following benefits:

- Maintaining consistency in how index types are presented and used.
- Reduce the likelihood of errors due to incorrect use of `IndexInfo`.
- Hide the details of MPI from the developer.

## Current Situation
The points are taken from the original `IndexInfo` design document linked in the first section.

- There is no consistent way of defining index ranges or lists for algorithms.
  This is done individually in each algorithm, and properties may be defined for spectrum numbers or workspace indices, and sometimes the interpretation of index properties even seems to depend on the facility (`LoadEventNexus`, see [13475](https://github.com/mantidproject/mantid/issues/13475)).
- Validation of index ranges and behavior on errors such as out-of-range indices is likewise done individually in all algorithms.
  - Algorithms behave inconsistently depending on errors (throw and error, print a warning, ignore silently).
  - There are bugs in some range validations (see [15414](https://github.com/mantidproject/mantid/issues/15414)).
  - Some algorithms do not validate for duplicate spectrum numbers and double-process the corresponding spectra (see [16651](https://github.com/mantidproject/mantid/issues/16651)).
  - Validations are not unit-tested to a good extent.

## Design Goals
 - Provide a property type which can specify a workspace and allowed (and predefined) input index types.
 - Unified behaviour on error (when bad indices are provided).
 - Hide index translations from the developer (this will take place internally within the property).
 - Automatically generate the required GUI input controls based on the specified index types.
 - Return the workspace and correct index set simultaneously in one call to `PropertyManager::getProperty`. 
 - Consistent and unit-tested translation without code duplication.
 - Consistent and unit-tested validation without code duplication.
 - Consistent and simple way of defining index properties without code duplication.
 - Consistent user interface.
 
## Implementation

### Basics

- Extend the `ArrayProperty<int>` to create an `IndexProperty` type which will accept user input for the indices of interest.
- Extend `PropertyWithValue` to create an `IndexTypeProperty` type which accepts user input for the type of indices supplied (WorkspaceIndices/SpectrumNumbers/DetectorIDs).
- Add a set of flags which control allowed index types (for use in the constructor).
- Create a series of methods within Algorithm which manage the creation and handling of these properties.

### Details

1. The `IndexProperty` type constructor will accept the following flags (or combinations of flags which will be forwarded to `IndexTypeProperty`):
	- `IndexType::SpectrumNumber` for list of global<sup>1</sup> spectrum numbers typically from 1-N.
	- `IndexType::WorkspaceIndex` for list of global workspace indices typically from 0-N.
	- `IndexType::DetectorID` for list of detector ids within the instrument.
2. Users will be restricted to entering only one of the allowed index types at the GUI level. 
3. The `IndexProperty` constructor will also take a reference to a `WorkspaceProperty` and an `IndexTypeProperty`. These will be used for validation and generation of the `SpectrumIndexSet`.
3. Validation will occur in `IndexInfo::makeIndexSet`(which throws for bad indices), not in every algorithm.
4. A method `declareIndexProperty` will be defined in `Mantid::API::Algorithm` which creates and ties a `WorkspaceProperty`, `IndexTypeProperty` and `IndexPropery` together. The name of these properties will then be reserved. Users will be restricted from creating new properties for this algorithm using these names. 
5. A method `setIndexProperty` will be defined in `Mantid::API::Algorithm` which will accept input for setting the all three properties simultaneously. Developers will be restricted to setting all three properties at once in client code. Attempts to set the properties individually will result in runtime errors.
6. A method `getIndexProperty` will be defined in `Mantid::API::Algorithm` which will return a tuple of the selected workspace and `SpectrumIndexSet`. Users will be restricted to only accessing this data simultaneously. Attempts to use `getProperty` will result in runtime errors.
6. `IndexInfo` will be used to translate the indices at the point of access i.e. `Algorithm::getIndexProperty()`.

<sup>1</sup><sub>The distinction is made here between local (a subset of all data partitioned on an MPI Rank) and global (entire data set). This will not be visible at the GUI or client API level.</sub>

### Example usage

**Property Declaration**:

Declaring the property in C++:
```cpp
//Property name may be fixed?
declareIndexProperty("InputWorkspace", IndexType::SpectrumNumber|IndexType::WorkspaceIndex);
//IndexType::WorkspaceIndex is the default
declareIndexProperty("InputWorkspace");
```  

**Algorithm Dialog Box (GUI)**:

**InputWorkspace** [ _________________ ]<br>
( **.** ) **SpectrumNumber** (  ) **WorkspaceIndex**<br>
**Indices** [ _________________ ]
 
**Client Code Access**:

*C++*:

Setting the property manually (tuple is created internally):

```cpp
setIndexProperty("InputWorkspace", ws, std::vector<SpectrumNumber>{1, 2, 3, 4});
//or
setIndexProperty("InputWorkspace", "ws", IndexType::SpectrumNumber, "1:33,42");
```

Accessing the property:

```cpp
MatrixWorkspace_const_sptr inputWS;
IndexSet indices;
std::tie(inputWS, indices) = getIndexProperty("InputWorkspace");//returns tuple
```

*Python*:

Algorithm function calls in Python would take the following form:
```python
# The index types could accept a range as a string or
# a numpy array which contains the values.
ChangePulseTime2(TimeOffset=10, InputWorkspace=ws, InputWorkspaceSet="1:33" )
ChangePulseTime2(TimeOffset=10, InputWorkspace=ws, InputWorkspaceIndexType=IndexType::SpectrumNumber, InputWorkspaceSet=[1,3,5,7])
```

Property Access would then take the form:
```python
inputWS, indices = getIndexProperty("InputWorkspace")
```

### Development Stages and Roll-Out

- The first release of this type will only include support for `IndexType::SpectrumNumber` and `IndexType::WorkspaceIndex`. The `DetectorID` translation, which is rarely used, is tricky and is not currently supported within IndexInfo, another translator specific to detector ids must be developed before this mode can be supported.
- The Roll-out for this would be simple since it is completely independent for all algorithms. However, this could become more complex in situations where there are non-standard conventions in validation and translation (e.g silently ignoring bad indices).
