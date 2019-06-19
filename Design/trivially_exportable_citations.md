# Trivially Exportable Citations

## Motivation

Both us (Mantid developers) and users want to ensure correct citations on publications that make use of Mantid.
Currently this is an issue for two main reasons; non-obvious citations for the Mantid project and difficulty in citing any methods used.

The proposal to do this now is prompted by discussions regarding reproducability of data at SINE2020 WP10.

This aims to provide the following benefits:
  - Method developers receieve correct citations
  - Mantid recieves correct citations
  - Mantid dependencies receieve correct citations
  - Processed data can outlive Mantid

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
class Citation
{
  Citation();

  std::string description;
  std::string url;
  std::string doi;
  std::string bibtex;
  std::string endnote;

  void loadNexus(...);
  void saveNexus(...) const;
};
```

The fields here mirror those of [`NXcite`](http://download.nexusformat.org/doc/html/classes/base_classes/NXcite.html#nxcite).
The following restrictions apply to ensure that in all cases somehting citable is allowed to exist:
  - `description` is always optional (this isn't needed for citation, but gives insight as to why this citation is relevant)
  - if `bibtex` is provided `endnote` must also be provided, and vice-versa (BibTex and Endnote contain essentially the same information, they can both be created if one can be. BibTex and Endnote do not imply a DOI is minted)
  - if `doi` is provided, `url`, `bibtex` and `endnote` must all be provided (BibTex and Endnote can be generated from DOIs)
  - if none of `doi`, `bibtex` or `endnote` are provided, `url` must be provided (there must be something there, even if this isn't citable a URL is better than nothing)

Some helper "toString" methods may be beneficial.

### Constructing a citation

Citations themselves will store the same data as `NXcite` however some helper functionality will be implemented to make creating them easier.

`Citation` could have several constructors that take `struct`s that define information required for each citation type.
Such `struct`s may look something like (by no means complete, just to give an idea):
```cpp

struct OnlineCitation
{
  std::string url;
  std::string whenAccessed;
};

struct BookCitation
{
  std::vector<std::string> authors;
  std::string title;
  std::string publisher;
  std::string pages;
};

struct PaperCitation
{
  std::vector<std::string> authors;
  std::string title;
  std::string journal;
  int year;
  std::string doi;
};

```

In the constructor for the relevant `struct`, `Citation` would then call `to_bibtex` and `to_endmode` functions to obtain citations in the required formats.
DOI and URL fields can be directly extracted where possible.

As an example, creating a citation could be done like so:
```cpp
auto const savu = Citation(PaperCitation{
  {"Wadeson, N", "Basham, M"}, "Savu: A Python-based, MPI Framework for Simultaneous Processing of Multiple, N-dimensional, Large Tomography Datasets", "", 2016, ""}
);
```

### Algorithm citations

An additional `virtual` method will be added to `IAlgorithm` that returns a `std::vector<Citation const> const`.
The developer has the option to overload this if the algorithm has relevant citations.
By default the implementation in `IAlgorithm` will return an empty vector.

### Citation recording

- `WorkspaceHistory` and `AlgorithmHistory` shall be extended to include storage for framework and algorithm level citations respectively
  - a `std::vector<Citation>` is likely sufficient
- The requisite IO methods will be extended to handle loading and saving these citations to NeXus
  - `WorkspaceHistory::loadNexus`
  - `WorkspaceHistory::saveNexus`
  - `AlgorithmHistory::saveNexus`

Citations will be recorded in NeXus files using the [`NXcite`](http://download.nexusformat.org/doc/html/classes/base_classes/NXcite.html#nxcite) class.

### Citation exporting

There will be functionality to generate plain text lists of citations in all supported formats.
This will be similar to the way we currently generate Python scripts form algorithm histories.

A new algorithm `ExportCitations` shall be implemented.
This algorithm takes a workspace as a property, gives the option of the desired export option and will output a file.

The Algorithm History GUI may be extended to provide this functionality in a similar manner to Python scripts generated from the algorithm histories.

### Documentation

There are two main requirements for documentation integration:
  - Listing the citations in the algorithm documentation page
  - Allowing the documentation writer (developer) to cite the citations at specific points in the documentation

The first point is trivial as we already do similar things for properties, related algorithms, etc.

The second will involve more work.
I don't have enough Sphinx know-how to suggest how this may be implemented.

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

## Follow on work

Work that should be looked into in the future.
Not to be considered for an initial implementation.

### Data citations

Facilities that mint DOIs for data collections could have this added to the workspace citations during the loading step.
Such citations should ideally be provided as `NXcite` in the raw data.
