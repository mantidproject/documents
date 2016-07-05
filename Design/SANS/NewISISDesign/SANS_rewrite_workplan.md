This document contains the required steps to implement the new ISIS design

## Core elements

1. Develop basic `SANSState` elements and `SANSStateBuilder`
  * Write User File parser
  * Write `SANSStateDirectorUserFile`
  * Develop validators


2. Develop `SANSLoadData` and the required sub-loaders and factories
 * Functionality which checks for instrument
 * Functionality which checks for IDF
 * Functionality which checks file type
 * Functionality which checks for periods
 * Functionality for tagging loaded workspaces with a hash
 * Functionality for basic event + separate monitor loading
 * Functionality for basic histogram + separate monitor loading
 * Functionality for basic raws + separate monitor loading (check if this is possible)
 * Functionality for loading periods
 * Functionality for loading added workspaces
 * Functionality for adding on the fly (2nd iteration?)
 * ADS functionality
 * Tubecalibration correction for loaded workspaces

3. Develop `SANSMoveWorkspace`
 * Create factory
 * Functionality for move, ie x, y for SANS2D, phi, y for LARMOR, etc.
 * Integrate with BeamCentreFinder requirements
 * reset to zero functionality

### Left to do in this section:
  * Handle added data
  * make use of parallel loading
  * No director for user file --> has not been necessary yet

## Basic reduction flow

1. Develop `SANSBatchReduction`
 * Develop initial batch skeleton
 * Iterator over each passed in state --> parallelisation opportunity
 * Funcionality to run loader for each state
 * Functionality to detect if there are more sub states required, i.e. if multiperiod of for event slicing, what is with multiple wavelength regimes?
 * Potential splitter for each state --> most of work here probably
 * Functionality for running single reduction --> parallelisation opportunity
1. Develop `SANSSingleReduction`
 * Develop initial skeleton
 * Handle the reduction selection --> HAB, LAB, BOTH, or merged --> is there a more general approach to this? does merge mean when there are more than two detectors?
 * Functionality for reduced can optimization
 * Functionality for can reduction tagging --> serialize full reduction state and create a hash
 * Functionality for stitch mechanism
1. Develop core of the single reduction algorithm
 * Create factories with place holders for each reduction step. Actually it might be the other way around that the factory is inside the actual algorithms
 * Think about NullProducts for factories

## Core defintitions for ISIS

1. Develop elements of the `SANSSingleReductionCore`
 * Should all be workflow algorithms

## GUI development

1. Create `SANSStateDirectorGUI`
1. Mockup of new GUI
TODO:
* Check with Raquel about the Python exposure of the Batch Reduction interface
1. Add presenter layer to interface GUI with `SANSBatchReduction` and other logic
1. Extend GUI

## Python interface

1. Create `SANSStateDirectorPythonInterface`
2. Replicate functionality of current functions

## Integration to BeamCentreFinder

TODO
