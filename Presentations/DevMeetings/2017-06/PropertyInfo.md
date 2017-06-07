In addition to addressing algorithm name violations and inconsistencies, we have also been looking into algorithm properties. Proposed changes can be listed under four categories:

1. Naming Violations and Inconsistencies
	- Some property names go against naming conventions. Rules are in place which define casing (camel case), first letter capitalization and illegal characters.
	- Some algorithm property names are inconsistently defined. For example, `WavelengthMin vs MinWavelength`, `StartWorkspaceIndex vs StartIndex`, `Xmin vs MinX`, `Filename vs FileName`.
2. InOut workspaces 
	- InOut workspaces are unecessary and produce inconsistency in the way algorithms are defined
	- Some algorithms have separate input and output workspaces. 
	- The InOut mechanism for workspaces is no longer advantages, this functionality of overwriting the input workspace can be achieved without using InOut workspaces.
	- Heavily used algorithms which will be affected: LoadInstrument, MaskDetectors, AddSampleLog, GetEi, AddPeak.
3. Hidden Properties
	- There are some algorithms which create output properties during execution. This practice should be abandoned as it increases the difficulty of maintining/verifying standards for property naming. Examples include FilterEvents and RefReduction. Properties could be set to optional and set depending on chosen execution path.
4. Index confusion
	- There is currently a lot of confusion with the number of ways to define indexing into workspaces and how users can input these index types. Currently used terms include WorkspaceIndex, SpectrumIndex, SpectrumNumber, DetectorID and DetectorIndex. 
	- Algorithm developers currently have the freedom to design algorithms which accept indices in any of the forms described above which serves to further complicate matters and add to this confusion.
	- A new proposed property type `WorkspacePropertyWithIndex` seeks to create a consistent interface for handling indices.
	- Client code will be better able to define and retrieve indices as a part of this property (the below text is taken from the initial plan for this type):
		WorkspacePropertyWithIndex
		--------------------------
		
		The index property was suggested as a mechanism for cleaning up the current mess with indexing in mantid algorithms. Graphically this property could take the form:
		
		```
		(*) Spectrum Number | ( ) Detector ID | ( ) Workspace Index
		List: [                   ] e.g 1-100 or 1, 5, 6, 200 etc.
		``` 
		
		Users could then declare the property using flags to determine which index types are allowed:
		
		```cpp
		declareProperty(make_unique<WorkspacePropertyWithIndex>("InputWorkspaceAndIndex", UseSpectrumNumber|UseDetectorID|UseWorkspaceIndex));
		```
		
		Users would then retrieve a tuple of values:
		```cpp
		const MatrixWorkspace_const_sptr inputWS;
		const IndexSet indexSet;
		std::tie(inputWS, indexSet) = getProperty("InputWorkspaceAndIndex");
		```
		
		or in python:
		```python
		inputWS, indexSet = getProperty("InputWorkspaceAndIndex");
		```
