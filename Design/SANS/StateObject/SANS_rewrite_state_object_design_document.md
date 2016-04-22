# State Object of the new SANS reduction workflow

## Abreviations

The following abreviations will be used below:
* `ISISCammondInterface` : ICI
* in-place: i-p
* Graphical User Interface. Essentially the `C++` part: GUI
* CentreFinder: CF

## Motivation

The SANS reduction workflow makes use of the so-called `ReductionSingleton`, which
essentially stores the configurational state either directly or in an `ISISInstrument`
object. The individual reduction steps extract their required state from this
`RedcutionSingleton`. The reduction steps are deeply coupled to the  `ReductionSingleton`,
which makes it hard to unit test them (and probably explains why such tests do not exist).
In addition there is a strong coupling of this `ReductionSingleton` to the
GUI logic, which essentially renders the ISIS SANS reduction a monolithic block.

A more modern approach is to use Mantid WorkflowAlgorithms. This mechanism avoids
the deep coupling. Individual steps would be supplied the required workspaces
and additional information and they return an adequate output workspace.
This would create an ideal environment for unit testing and documentation.

## Current status

### State in the backend

As described above the state is stored in the `ReductionSingleton`, the `ISISInstrument`
and its implementations and partially also in the `ReductionSteps` themselves.

For a detailed analysis of how the state is spread in the current implementation,
please see [here](./SANS_Mapping_of_backend_variables.md)

#### State in the GUI

For a detailed analysis of the GUI and its coupling to the
reducer backend see [here](./SANS_Mapping_of_GUI_variables.md)


## State Object approach

### Sub State approach

### Using Mantid's `PropertyManager` as maps

### Mapping of old state to new State Object
