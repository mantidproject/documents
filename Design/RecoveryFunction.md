# Introducing a recovery function

## Motivation

Several users have commented that it would be very useful if Mantid could recover the final state after a crash. The motivation for this is quite clear. However, there are also some additional benefits that could arise from such a functionality.
* The history used for recovery could provide useful diagnostics of crash instances
* The history used for recovery could also be used to re-load workflows, rather than saving data, which is quicker for data-intensive users, such as single crystal diffraction

## Requirements

The recovery function should generate a script, this should:
* Be capable of recreating all workspaces present when it was last generated
* Be automatically generated at regular intervals
* Result in as efficient a re-load process as possible
* Have minimal overhead for running
* Allow some level of user choice of how much of the history to re-run

## Implementation possibilities

Currently the preferred option is to have a script that can amalgamate the workspace histories in the current instance of Mantid and generate a single script. This can be done by comparing time/date-stamps, algorithm names and input parameters.

### Notes/considerations

The algorithm timestamp is going to have to go to shorter denominations - in the `Muon-esque` example there is a case where two algorithms are run at the "same" time, then end up in different workspace history files and as a result are re-assembled in the wrong order.

In sequential fitting algoritms may run with the same timestamp, but have different outputs. This suggests that string comparison as well as timestamp comparison will be necessary.

Workspace history will not delete workspaces that might have been deleted during the uptime. This could become an issue if there are a lot of these.

If a workspace is a member of a grouped workspace and another member of that group has been deleted, the original group workspace command will fail, as there is no record of all workspaces in the group. This is realted to `ADSValidator`.

Places where `ADSValidator` occurs:
* `Framework/Algorithms/src/DeleteWorkspaces.cpp`
* `Framework/Algorithms/src/GroupWorkspaces.cpp`
* `Framework/Muon/src/ConvertFitFunctionForMuonTFAsymmetry.cpp`
* `Framework/Algorithms/src/Stitch1DMany.cpp`
* `Framework/Algorithms/src/SumOverlappingTubes.cpp`
* `Framework/Algorithms/src/ConjoinXRuns.cpp`
* `Framework/WorkflowAlgorithms/src/ExtractQENSMembers.cpp`
* `Framework/Algorithms/src/MergeRuns.cpp`
* `Framework/Algorithms/src/PolarizationEfficiencyCor.cpp`

Check how `ConjoinWorkspaces` deals with history.

Certain actions performed in instrument view require a new workspace to be created before the algorithm can be executed. An example of this is `AddPeak`, in instrument view this creates a new peak workspace behind the scnenes, but this is not captured in the workspace history. As a result the script does not work properly when re-run. This can be re-created by running the unscripted diffraction test number 1 (ask Keith about this test if unsure).

Group/ungroup workspaces is not captured in the WS history

We must be able to deal with multiple instances of mantid running on either the same machine or different machines that share a home directory on a mounted network drive.

### Recovery Folder Structure

The recovery information will be written into a `recovery` subdirectory of the Mantid user config area (`%APPDATA%\mantidproject\mantid` on Windows or `$HOME/.mantid` on Linux/MacOS),
referred to as `RECOVERY_ROOT` from now on. This will then have additional subdirectories of the form:

```
RECOVERY_ROOT
  |-- *hostname*
      |-- *pid*
          |-- timestamp-1
          |-- timestamp-2
          |-- timestamp-3
```

where *hostname* is the machine name and *pid* is the process ID of the running process. On a clean exit of MantidPlot only the *pid* folder would be removed for the current machine.

Each timestamped folder will contain a marker file whilst the checkpoint is being written, which is removed after the write has completed. Any time stamped folders containing this file, indicating a partial save point, will not be offered for recovery.

On starting a new session of MantidPlot the recovery function would generated a list of recovery directories for its hostname. It would then get a list of all PIDs of the currently running MantidPlot processes and remove any of
these running PIDs from the original recovery list. If more than 1 recovery option is available then a selection will be offered to the user.

#### Note for v3.13

Due to time constraints a more limited system that simply checks if any other `MantidPlot` process is running and disables project recovery will be considered, and implemented if the full implementation is not possible in time.


## Open questions

* How much overlap would this functionality have with Project Saving?
* Should the functionality be in MantidPlot or Framework?
  * It probably makes sense to have the workspace recovery fn available within the framework, while the ui elements can only be in the ui.  We would need to be able to disable it in the properties file for developers, automated tests and auto reduction.

## Actions

Keith to work on prototyping and testing the proposed implementation. (30 May 2018)

David to look at the separation of workspace and plotting states in `Save Project`. (June 2018)


## Implementation steps

1. POC
   1. POC Saving: Script to generate history, and graph and window saving
   2. POC recovery: Recovery to previous state using script manually in the script editor
   3. Performance evaulation
2. Early integration
   1. Automatic svaing of workspace script and window saving (seperate thread every n minutes)
   2. Detection of recovery script on startup, option to ignore or send to script editor.  Script complete including creating windows & plots.
   3. Stability evaulation
   4. Fix already identified holes in history (workspace list porpoerties, etc.)
3. Improve integration
   1. Keep workspace script more up to date using signals from the ADS and timestamps from the hitory and script to incrementally keep workspace script current
   2. Add option to automatically recover, including a progress bar of some sort, and abort option.
   3. Usability testing
   4. Project saving suport for Muon, refl
