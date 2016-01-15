# Mantid MPI support

## Motivation

Current neutron facilities are pushing Mantid to its usability limits, performance and memory-consumption wise. Latest with ESS going into operation we will reach the point where running Mantid on a single computer is not feasible anymore.

A certain amount of work has been put into Mantid MPI support previously, but the scope and spread are so far limited.

Data reduction generally seems to be a good target for parallelization across many computers, since many parts of the problem are only loosely coupled.


## Current status

- Support for certain work flows (in particular `SNSPowderReduction`).
- Requires special preparation of reduction script.


## Requirements

- Support for all (big) instruments.
- Low latency for live reduction.
- Scalable, i.e., the design should not put a fixed requirement on number of processes (MPI ranks) for any instrument.
- Mostly transparent to developers of a `WorkflowAlgorithm`, and partially transparent for developers of a normal `Algorithm`. That is, we should not introduce anything that will require from all our developers to know how to use MPI.


## Design

### Basic concept

Generally, algorithms deal with large number of spectra (or event lists) that are being processed serially (or partially in parallel when threading is implemented). The key to the proposed design is, that **many algorithms treat all spectra independently**. Thus it is in many cases efficient to put different spectra on different MPI ranks. We choose this as the basic concept for the MPI design.

The basics of the proposed design are quite simple. We need to add just two new concepts which together facility running Mantid with MPI:

1. Data corresponding to a workspace may be stored in different ways across MPI ranks. We logically think of a single workspace, even if it is spread out to many MPI ranks (and thus technically we have an instance of a workspace on each rank). We refer to this as *storage mode* of a workspace.

2. Algorithms are executed in a way that depends on the storage mode of the input workspaces and possibly flag arguments to the algorithm. We refer to this as *execution mode* of an algorithm. The storage mode of all output workspaces is determined and set by the algorithm.

### Implementation

The following basic changes are required:

- Add a flag `StorageMode` to `Workspace`.
  * `StorageMode::Cloned` There is a copy (clone) of the Workspace on each rank.
  * `StorageMode::Distributed` Each rank holds parts of the Workspace (spectra).
  * `StorageMode::MasterOnly` The master/root rank has the Workspace.
- `Algorithm` determines its `ExecutionMode` based on:
  * `StorageMode` of the input workspaces.
  * Optional flags (this should be used as little as possible, since it will basically require from script authors to know about MPI).
- Possible execution modes are:
  * `ExecutionMode::Invalid` Indicates a state where execution is not possible. This should not happen in normal operation and is used for reporting errors.
  * `ExecutionMode::Serial` Serial execution (non-MPI build or MPI build with single rank).
  * `ExecutionMode::Identical` Independent execution in the same way on each rank.
  * `ExecutionMode::Distributed` Distributed execution, may involve communication.
  * `ExecutionMode::MasterOnly` Execution only on the master rank.
- `Algorithm` determines and sets the `StorageMode` of all output workspaces:
  * Typically input `StorageMode` and `ExecutionMode` are enough to determine the `StorageMode` of the outputs.
  * In some special cases it may be necessary to have a user-set flag (for example in a `Load` algorithm, which does not have input workspaces).

In the proposed design the implementation is almost trivial for most algorithms. The basic mechanism of determining the `ExecutionMode` and the output `StorageMode` can be implemented in `Algorithm::execute()`, which is a non-virtual interface for `exec()`. As a consequence we do *not* need to modify `exec()` for all child classes of `Algorithm`.

Most algorithms are "trivially parallel", i.e., they treat all spectra independently. As a consequence we could run them with `ExecutionMode::Distributed` without any changes. However, making this possible as a default is risky, because then we would need to make really sure to modify all algorithms that are not "trivial". Therefore, we propose:

- In the default implementation an algorithm does not support parallel execution. It will throw an error when attempting this. This will also allow us to do a "guided" port of existing algorithms: We can run a reduction script with MPI, see where it fails, port the failing algorithm for MPI, and repeat.
- To ease porting "trivially parallel" algorithms, we introduce a new base class `TriviallyParallelAlgorithm`. When a developer has convinced himself that an algorithm has no features that would require changes for parallel execution, he can modify it to inherit from `TriviallyParallelAlgorithm` instead of from `Algorithm`.

This approach is minimally invasive and reasonably safe.

- Likewise, there could be another base class, `MasterOnlyAlgorithm`, for algorithms that can run only on one MPI rank (the master rank). This class comprises many `Save` algorithms, since without special changes we can neither write from all ranks to a single file, nor does writing to multiple files make sense (since the number of files would depend on the number of ranks, which is variable).

Further notes:

- Even if a workspace has `StorageMode::MasterOnly`, the workspace will still exist on all ranks. Data in the workspaces on non-master ranks will be ignored. If we would not have a workspace on all ranks, we would not be able to run reduction scripts without modification. The alternative would be to have the workspace only on the master rank. Then all reduction scripts that at some point have workspaces with `StorageMode::MasterOnly` would need to have branches, e.g., something like

  ```python
  if MPI::getRank() == MPI::getMasterRank():
      # Algorithms that should run only on the master rank
  ```
  This would mean severely increased effort, and knowledge about MPI from anyone who wants to use it.


## Mantid components with special design requirements

### MDWorkspace

`MDWorkspace` is not based on a discrete list of spectra, but a multi-dimensional volume. We can parallelize this with MPI by cutting the volume into blocks (not necessarily contiguous). There is no fundamental problem with this, however there are quite a few subtleties and aspects that require a significant effort to implement.

- There are transitions from `Workspace` to `MDWorkspace`, e.g., when events are inserted into an `MDWorkspace`, so the MPI design must be able to support both in the same run.
- Not all coordinates in an `MDWorkspace` are necessarily equal. Computationally, there may be a stronger coupling along certain directions in the volume, e.g., λ vs. Q.
- The volume does not have a simple structure: The relevant volume is often not cubic, and there are regions of high and low density. As a consequence we need to be able to split the volume in a very flexible way to balance the load, and probably also need to be able to redistribute on the fly.
- In summary, we need the following:
  * A ways to split an `MDGridBox`.
  * Partitioning strategies and algorithms.
  * Redistribution of `MDGridBox`, i.e., a ways to move remove a specific box from the workspace on one rank and add it on another.
  * A solution for load balancing, both static (i.e., at startup) and dynamic (i.e., during a run, when large load imbalance occurs).

### Monitors

The simplest approach to monitors is to load and process them on all ranks. Then each rank has the required information for, e.g., a normalization available. The proposed design would support this mode of operation by loading monitors into a workspace with `StorageMode::Cloned`, i.e., there is a clone of all data on each rank.

This may however not be enough. Depending on the instrument and facility monitor data can be large. In particular:

- It could be large enough to make the computation time for monitor data significant. That is, with `StorageMode::Cloned` (and thus `ExecutionMode::Identical`) we would duplicate a potentially large computational cost. It might then be necessary to process the monitors on a dedicated MPI rank which could then distribute the required results to all ranks.
- It could be large enough that a single dedicated rank is too slow or does not have sufficient memory. It would then be necessary to distribute also processing of the monitors. This could be simple if there are several monitors with equal rate, but hard if there are only few monitors with very high event rates or time resolution.

The conclusion for the time being is:

- We need to get more information on monitors, such that we can estimate the performance requirements. This includes ESS, where we do not yet have any information on monitors.
- It is very likely that we may need dedicated ranks for monitors. That is, we may have a non-uniform MPI structure. We should thus ensure that the implementation is flexible with respect to MPI communicators. We should not make the mistake and assume that we always just have `MPI_COMM_WORLD`, but different sub-communicators for different purposes.

I do not see a good reason for changing the basic design due to monitors (or rather, I do not see a better solution). The conclusion from the discussion in this section is that monitor data is not necessarily available locally (e.g., we might need to introduce another `StorageMode`). The hope is that this fact can be hidden behind the current (or potential future) interface that algorithms use when accessing monitor data. We should probably investigate this a bit more and make sure that adding another `StorageMode` can be done without having to modify algorithms that were previously ported.

### Loading

To make the MPI design worthwhile also for non-live reduction, we need to ensure that we can efficiently load a file in parallel run from a network file system. The basic problem is that the way we split the data in memory (different spectra on different ranks) is not reflected in the structure of our files (e.g., Nexus). This is not only a problem of current files, but impossible in general, since the number of MPI ranks and the way we split is flexible. For files that store large events list contiguously a naive load would be rather efficient, but for a file that was written from a stream, we would probably have small frames of event data, where each frame just adds few events to each spectrum. Thus the data belonging to different MPI ranks would be scattered all of the file.

The most efficient way to read a file is in big blocks. We can do this in parallel and then redistribute the data via MPI once loaded. On a cluster node with Infiniband we have more than 10 GB/s bi-directional network bandwidth available, which is faster than the read from the network file system, so redistribution is definitely feasible.

- The basic concept is clear:
  * All ranks load big chunk of file.
  * Sort and split chunk according to target rank.
  * Send split data to all other ranks.
- It may be non-trivial to obtain good performance. The communication would be all-to-all with variable sizes, so some thought has to be put into this.

### Saving

Many save operations deal with small data, so this can simply be done from the master rank. However, there will also be large data to save, e.g., a processed event workspace. In that case we will need parallel writing. This is supported by HDF5 (the file format underlying Nexus). Basically we just need to gather more detailed requirements and figure out an implementation. This should pose no new problems for the MPI design as such, but will require some effort.

### Visualization

Mantid has various ways of visualizing data. Unless all data is available on the master rank there is no simple solution for combining this with an MPI-based data reduction.

- The distributed nature of our data is not necessarily only due to computation cost, but in many cases also due to the data volume, i.e., it is technically not possible to move all data to a single rank for visualization purposes.
- ParaView deals with basically the same problem and has MPI support. We should look into how ParaView solves this and figure out how we can benefit from that.
- No matter what, we may needs ways to access data on other ranks. This does not seem to put any significant limitations for the proposed design.

### Interactive workflow

The Mantid GUI provides:

- Views into data (visualization/plotting, access of underlying arrays of data).
- Interaction with data via algorithms.

Views into data are a generalization of the discussion in Sec. **Visualization** and will not be discussed here.

It is unclear how interaction with MPI-based data reduction could work, maybe we can learn from ParaView also here. See also the [ESS live-data protoype](https://github.com/DMSC-Instrument-Data/live-data-prototype), which tries to solve a similar problem with a design based on a reduction back end that is controlled via a front end with reduced functionality.

## Miscellaneous remarks

### Distribution

How would we distribute MPI builds of Mantid? Unless we want to ship a specific MPI library with Mantid this does not make much sense. The specific library (implementation and maybe even version) has probably to be known at compile- or latest link-time, and it is not of advantage to limit our users to specific MPI version. That is, we have two options:

- Provide Mantid MPI builds linked with specific MPI version.
- Provide Mantid MPI only as source.

### Testing

Setting up tests for an MPI implementation is a bit cumbersome. For unit tests the best way might be to mock all calls to the MPI library.
