## The IndexProperty Summary

The `IndexProperty` is a new property type in Mantid which can be used in general for accessing all of, or a subset of, workspace spectra. The property uses an underlying `IndexInfo` object to create a `SpectrumIndexSet` from a set of user defined input indices (or spectrum numbers).

See [here](https://github.com/mantidproject/mantid/blob/b623edb03ae604aaaed4dc225fbb080642031d41/docs/source/concepts/IndexProperty.rst) for more details.


Refactor example `ChangePulsetime`. Original implementation:

```cpp
void ChangePulsetime::init() {
  declareProperty(make_unique<WorkspaceProperty<EventWorkspace>>(
                      "InputWorkspace", "", Direction::Input),
                  "An input event workspace.");
  declareProperty(make_unique<ArrayProperty<int>>("WorkspaceIndexList", ""),
                  "An optional list of workspace indices to change. If blank, "
                  "all spectra in the workspace are modified.");
  //etc
}

//----------------------------------------------------------------------------------------------
/** Execute the algorithm.
 */
void ChangePulsetime::exec() {
  EventWorkspace_const_sptr in_ws = getProperty("InputWorkspace");
  EventWorkspace_sptr out_ws = getProperty("OutputWorkspace");
  if (!out_ws) {
    out_ws = in_ws->clone();
  }

  // Either use the given list or use all spectra
  std::vector<int> workspaceIndices = getProperty("WorkspaceIndexList");
  int64_t num_to_do = static_cast<int64_t>(workspaceIndices.size());
  bool doAll = false;
  if (workspaceIndices.empty()) {
    doAll = true;
    num_to_do = in_ws->getNumberHistograms();
  }

  double timeOffset = getProperty("TimeOffset");

  Progress prog(this, 0.0, 1.0, num_to_do);
  PARALLEL_FOR_NO_WSP_CHECK()
  for (int64_t i = 0; i < num_to_do; i++) {
    // What workspace index?
    int64_t wi;
    if (doAll)
      wi = i;
    else
      wi = workspaceIndices[i];

    // Call the method on the event list
    out_ws->getSpectrum(wi).addPulsetime(timeOffset);

    prog.report(name());
  }

  setProperty("OutputWorkspace", out_ws);
}

```


Refactored Code:

```cpp
void ChangePulsetime::init() {
  // IndexType::WorkspaceIndex is default other options include:
  // IndexType::SpectrumNum
  // IndexType::DetectorID (coming soon)
  declareWorkspaceInputProperties<EventWorkspace>("InputWorkspace");
  //etc
}

//----------------------------------------------------------------------------------------------
/** Execute the algorithm.
 */
void ChangePulsetime::exec() {
  EventWorkspace_const_sptr in_ws;
  Indexing::SpectrumIndexSet indexSet;

  std::tie(in_ws, indexSet) =
      getWorkspaceAndIndices<EventWorkspace>("InputWorkspace");

  EventWorkspace_sptr out_ws = getProperty("OutputWorkspace");
  if (!out_ws) {
    out_ws = in_ws->clone();
  }

  // Either use the given list or use all spectra
  double timeOffset = getProperty("TimeOffset");

  Progress prog(this, 0.0, 1.0, indexSet.size());
  PARALLEL_FOR_NO_WSP_CHECK()
  for (int64_t i = 0; i < static_cast<int64_t>(indexSet.size()); i++) {
    // What workspace index?

    // Call the method on the event list
    out_ws->getSpectrum(indexSet[i]).addPulsetime(timeOffset);
    prog.report(name());
  }

  setProperty("OutputWorkspace", out_ws);
}

```
