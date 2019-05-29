# Trivially Exportable Citations

## Motivation

Both us (Mantid developers) and users want to ensure correct citations on publications that make use of Mantid.
Currently this is an issue for two main reasons; non-obvious citations for the Mantid project and difficulty in citing any methods used.

## Solution

The ideal scenario is that given a workspace containing the data a user intends to publish, there is a utility that will take this workspace and generate a list of citations.

- The list should include citations for the version(s) of Mantid used, citations for Mantid dependencies (e.g. MPI) where appropriate, and citations of algorithms used.
- The user may select the format to export the citations in (e.g. DOI only, Bibtex, Endnote).
- If the processing of a workspace spans multiple Mantid versions then the citations shall include every version of Mantid that has touched the workspace.
- Citations for algorithms are static and cannot depend on algorithm properties.

It should be programatically possible to add a citation to the workspace history given the workspace.
This allows parts of Mantid that are not algorithms but still citable to be cited.
An example of this are the Muon and Indirect GUIs.

Any algorithms that currently contain a citation in their user documentation will have this removed and added in code.
Documentation tooling should be produced to automatically populate citations on documentation pages.

The instructions of what to cite thet are shown when you launch Mantid will be removed.
They will be replaced with instructions of how to export the citations from a workspace.

## Design

This is largely based on what Savu does to solve the same problem.

### Citation data type

A new data type (`Citation`) will be created to store citations.
This type will be exported to Python.

As conversion between citation formats is non trivial, the algorithm developer is required to supply the citation in all formats.

The bare minimum for this type will be something similar to the following:
```cpp
struct Citation
{
  std::string doi;
  std::string bibtex;
  std::string endnote;

  void loadNexus(...);
  void saveNexus(...);
};
```

Some helper "toString" methods may be beneficial.

### Algorithm citations

An additional `static` method will be added to `IAlgorithm` that returns a `std::vector<Citation const> const`.
The developer has the option to overload this if the algorithm has relevant citations.
By default the implementation in `IAlgorithm` will return an empty vector.

### Citation recording

- `WorkspaceHistory` and `AlgorithmHistory` shall be extended to include storage for framework and algorithm level citations respectively
  - a `std::vector<Citation>` is likely sufficient
- The requisite IO methods will be extended to handle loading and saving these citations to NeXus
  - `WorkspaceHistory::loadNexus`
  - `WorkspaceHistory::saveNexus`
  - `AlgorithmHistory::saveNexus`

### Citation exporting

There will be functionality to generate plain text lists of citations in all supported formats.
This will be similar to the way we currently generate Python scripts form algorithm histories.

A new algorithm `ExportCitations` shall be implemented.
This algorithm takes a workspace as a property, gives the option of the desired export option and will output a file.

The Algorithm History GUI may be extended to provide this functionality in a similar manner to Python scripts generated from the algorithm histories.

### Documentation

TODO: look at existing documentation tooling and determine how this should be done.

## Design considerations

### Property dependant citations

I briefly considered making the citations returned for algorithms dependant on the algorithm being run.
This allows the algorithm to record what citations it used during execution.

The advantage this gives is greater accuracy of citations (e.g. toggling an option may divert control flow away from a particular citable method).

It was chosen not to go down this route for the following reasons:
  - It adds complexity
  - It adds runtime dependency
    - This prevents tooling for algorithm documentation

### Backwards compatibility

What happens when loading old workspaces with no citations in the NeXus file?

### `constexpr`

Is it worth using `char *` as the string format to be able to `constexpr` the `Citation` structure?

### Citing in algorithm documentation

How would a developer cite one of the algorithm citations in the algorithm documentation?
