# State Object of the new SANS reduction workflow

The aim of this document is to introduce a new way to store reduction state information for an ISIS SANS reduction.

## Terms

| Term | Defintion|
| ----|-----------|
| GUI | Graphical User Interface|

## Motivation

The motivation for a State object approach of ISIS SANS can be found [here](../Design_Document.md). The [current status](#CurrentStatus) demonstrates the complexity of the current information distribution among the `ReductionSingleton`, the `ReductionStep`s and the `ISISInstrument`. Besides being "all over the place", there is a tight coupling of the reduction's state and the GUI.

## Current status  <a name="CurrentStatus"></a>

### State in the backend

A detailed analysis of how the state is spread in the current implementation can be found here [here](./SANS_mapping_of_backend_variables.md)

#### State in the GUI

A detailed analysis of the GUI and its coupling to the
current reducer back-end can be found [here](./SANS_mapping_of_GUI_variables.md).

## State Object approach

### Arguments for a state approach

Some issues with the current approach are:

1. The current ISIS SANS back-end elements contain interdependencies. Currently, for example, the `TransmissionCalc` obtains wavelength binning information from `UnitsConvert`. This means that if `TransmissionCalc` is to be dynamically replaced (because a new instrument might need a completely different way to do transmission calculation), then this will most certainly break the reduction system.
2. The `ReductionSingleton` owns the `ReductionStep`s, but upon execution of a `ReductionStep`, passes itself into the `execute` method of that step. This means that each `ReductionStep` has explicit knowledge of the `ReductionSingleton` and very often even of the implementation of the `ReductionSingleton`.
3. The GUI reads and writes directly to the back-end elements.
4. Creating a new reduction setup often means that the `ReductionSingleton` needs to be created again. This often resulted in files being loaded again, since it was very hard to figure out what the previous state had been.

Having a clearly localized data structure which contains the complete state required for a reduction will allow us to:


1. Eliminate interdependencies by passing all necessary information via the state object to each unit of work (formerly `ReductionStep`) separately and independently.
2. Eliminate the need of the unit of work to have knowledge about its owner (or caller), since all required information is in the state object
3. Eliminate any coupling to the GUI, as a state is manipulated entirely on the GUI side, and then passed to the reduction system for processing.
4. Allow for easy tracking of state change. Having a localized, simple data structure with the entire state makes the comparison trivial (e.g. hashsums of the data structure)

### State design

The state will have to contain more than 100 configuration variables of which a large fraction are available to the user. The state itself should be (almost) a passive data structure. The only functionality which could be conceivable here is a type of self-consistency check (but the implementation might force us to have this check in place when the object is being created. Alternatively, we a type of schemer object is possible.)

The entire information required for a SANS reduction should be contained in a `SANSState` object. The configuration of this state should be handled by a `SANSStateBuilder` which in turn is/can be governed by a `SANSStateDirector`.

Due to the choices of input types into Mantid algorithms, the `SANSState` and the sub-states which are described below have to be convertible into a `PropertyManager` object since this is the only complex data strucutre which can be currently used as an input property for Mantid algorithms.

#### Where will the state be generated?

There are several scenarios where a `SANSState` can be generated.

1. It can be generated when a user file is read in. This converts the information on the user file into a state object. Note that this is not a complete state object, since it will be missing important components such as data information. This would require a `SANSStateDirectorUserFile`
2. A GUI side request for a reduction. From the GUI settings a list of `SANSState` objects is created which is passed on to `SANSBatchReduction`. This requires a `SANSStateDirectorGUI`.
3. A user sets information via the PI. Using the current PI forces the a global object onto the design. This can be achieved by defining a `SANSStateDirectorPythonInterface` which is essentially a Singleton object.
4. A `SANSState` is passed into the `SANSBatchReduction` for processing. The algorithm splits the old state up into a `SANSState` per period which is to be processed. This is achieved via a `SANSStateDirectorPeriod`.


### Sub-states
Since a reduction in the SANS work-flow can depend on more than 100 variables it is advisable to not store them in a flat data structure. Hence a  `SANSState` object should be composed of sub-`SANSState` objects which contain information relevant for a unit of work, e.g. a work-flow algorithm, or a specific domain, e.g. instrument information.

The envisioned sub-states are:

| sub-`SANSState`     |  Information content |
|---------------------|----------------------|
| `SANSStateData`     | Contains the full file paths for the data which is to be reduced. (sample_scatter, sample_transmission, sample_direct, can_scatter, can_transmission, can_direct)|
| `SANStateMoveWorkspace` | Contains general instrument information. Contain a map to the available detector banks and the detector which is currently being investigated.  It has all the required settings to move an instrument of a specified type.|
| `SANSStateMask`  | Contains mask information (detector dependent!)|
| `SANSStateConvertToQ` | Contains information for the q binning conversion
| `SANSStateMultiplyVolumeAndAbosoluteScale` | Contains information about geometry and absolute information |
| `SANSStateConvertEventToHistogram` | Contains information to convert an event workspace into a histogram workspace |
| `SANSStateConvertToWavelength` | Contains information about the wavelength conversion |
|`SANSStateCreateAdjustmentWorkspace`| Contains everything which is related with creating adjustment workspaces, e.g normalization, transmission calculation, etc |
| `SANSStateReduction` | Contains information about which reductions to perform, i.e. if LAB, HAB, both or merged |
| `SANSStateSliceEvent` | Contains inforamtion about the event slice |
| `SANSState` | Is clearly defined  collection of sub-states. |
## State design for ISIS SANS

The proposed `SANSState` is shown below:

![](../Images/SANSState.png)


## State Builder and State Directors

The issue of constructing the states has been mentioned above. The state objects are constructed via a `SANSStateBuilder` which is orchestrated by a `SANSStateDirector`. The director is appropriate for the current environment in which the state is being generated, e.g. in the PI or the GUI.

![](../Images/SANSBuilder.png)

Not all sub-states will be set separately. Setting `SANSStateData` causes the `SANSStateBuilder` to choose the correct `SANSStateMoveWorkspace` for the type of instrument associated with the data files. For ISIS data this should then provide the correct settings for LARMOR, SANS2D and LOQ.


## Implementation

Using the `SANSState` as an input entity for work-flow algorithms limits our choice to how these state objects can be implemented. The requirement of a map-like data structure limits us to `PropertyManager`s as an input entity for the `SANSState` information. This means that the we have a layered `PropertyManager` of depth three:
1. `SANSState` tself which defines a complete reduction.
2. The individual sub-states.
3. Some of the sub-states require a map in order to store detector-dependent information

This does not mean though that the information should exist the entire time as a `PropertyManager` object. A more purposeful data structure which can be converted to and from a `PropertyManager` object would allow us to only have to depend on the `PropertyManager` object when the information is set on the algorithm. Out- and inside the algorithm the `PrropertyManager` is converted to and from a `SANSState` object which includes inbuilt validation logic and makes passing a large chuck of strucutred data into an algorithm much safer.

A prototype implementation could look like this:

```python
from abc import (ABCMeta, abstractmethod)
import inspect
from mantid.kernel import PropertyManager


# -------------------------------------------------------
# Parameters
# -------------------------------------------------------
class TypedParameter(object):
    def __init__(self, name, parameter_type, validator=lambda x: True, default=None):
        self.name = "_" + name
        self.parameter_type = parameter_type
        self.value = default if isinstance(default, parameter_type) else None
        self.validator = validator

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, self.parameter_type):
            raise TypeError("Trying to set {} which expects a value of type {}."
                            " Got a value of {} which is of type {}".format(self.name, str(self.parameter_type),
                                                                            str(value), str(type(value))))
        if self.validator(value):
            setattr(instance, self.name, value)
        else:
            raise ValueError("Trying to set {} with an invalid value of {}".format(self.name, str(value)))

    def __delete__(self):
        raise AttributeError("Cannot delete the attribute {}".format(self.name))


# ---------------------------------------------------------------
# Validators
# ---------------------------------------------------------------
def is_not_none(value):
    return value is not None


def is_positive(value):
    return value >= 0


# ------------------------------------------------
# SANSStateBase
# ------------------------------------------------
class SANSStateBase:
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def property_manager(self):
        pass

    @property_manager.setter
    @abstractmethod
    def property_manager(self, value):
        pass

    @abstractmethod
    def validate(self):
        pass


class PropertyManagerConverter(object):
    def __init__(self):
        super(PropertyManagerConverter, self).__init__()

    @staticmethod
    def convert_state_to_property_manager(instance):
        descriptor_values = PropertyManagerConverter.get_descriptor_values(instance)

        # Add the descriptors to a PropertyManager object
        property_manager = PropertyManager()
        for key in descriptor_values:
            value = descriptor_values[key]
            if value is not None:
                property_manager.declareProperty(key, value)
        return property_manager

    @staticmethod
    def convert_state_to_dict(instance):
        descriptor_values = PropertyManagerConverter.get_descriptor_values(instance)
        # Add the descriptors to a dict
        return {key: value for key, value in descriptor_values.iteritems() if value is not None}

    @staticmethod
    def get_descriptor_values(instance):
        # Get all descriptor names which are TypedParameter of instance's type
        descriptor_names = []
        for descriptor_name, descriptor_object in inspect.getmembers(type(instance)):
            if inspect.isdatadescriptor(descriptor_object) and isinstance(descriptor_object, TypedParameter):
                descriptor_names.append(descriptor_name)

        # Get the descriptor values from the instance
        descriptor_values = {}
        for key in descriptor_names:
            value = getattr(instance, key)
            descriptor_values.update({key: value})
        return descriptor_values

    @staticmethod
    def set_state_from_property_manager(instance, property_manager):
        keys = property_manager.keys()
        for key in keys:
            value = property_manager.getProperty(key).value
            setattr(instance, key, value)
```


And:

```python
from SANSStateBase import (SANSStateBase, TypedParameter, is_not_none, is_positive, PropertyManagerConverter)


# -----------------------------------------------
#  SANSStateData Setup for ISIS
# -----------------------------------------------
class SANSStatePrototype(SANSStateBase):
    parameter1 = TypedParameter("parameter1", str, is_not_none)
    parameter2 = TypedParameter("parameter2", int, is_positive, 1)

    def __init__(self):
        super(SANSStatePrototype, self).__init__()
        self.converter = PropertyManagerConverter()

    @property
    def property_manager(self):
        # Once algorithms accept Property Managers we can use the version below
        # return self.converter.convert_state_to_property_manager(self)
        # otherwise we use this version
        return self.converter.convert_state_to_dict(self)

    @property_manager.setter
    def property_manager(self, value):
        self.converter.set_state_from_property_manager(self, value)

    def validate(self):
        is_valid = dict()
        if self.parameter1 is None:
            is_valid.update({"parameter1": "Parameter may not be none"})
        if not is_valid:
            raise ValueError("SANSStatePropertyType: Parameters are not valid")
```

And:

```python

from mantid.api import DataProcessorAlgorithm
from mantid.kernel import PropertyManagerProperty
from SANSStatePrototype import SANSStatePrototype


class SANSAlgorithmPrototype(DataProcessorAlgorithm):
    def category(self):
        return 'SANS'

    def summary(self):
        return 'Prototype Algorithm'

    def PyInit(self):
        self.declareProperty(PropertyManagerProperty("SANSStatePrototype"))
        self.declareProperty('Factor', defaultValue=Property.EMPTY_DBL, direction=Direction.Input,
                             doc='Factor')

    def PyExec(self):
        a = 1
        b = 2
        print a
        property_manager = self.getProperty("SANSStatePrototype").value
        state = SANSStatePrototype()
        state.property_manager = property_manager
        # Do things here

    def validateInputs(self):
        errors = dict()
        #Check that the input can be converted into the right state object
        property_manager = self.getProperty("SANSStatePrototype").value
        try:
            state = SANSStatePrototype()
            state.property_manager = property_manager
            state.validate()
        except ValueError, e:
            # Would have to be more understandable
            errors.update({"SANSStatePrototype": str(e)})
        return errors

AlgorithmFactory.subscribe(SANSAlgorithmPrototype)
```

A use case would look like:

TODO: Add usage here
