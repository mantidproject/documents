More Flexible LiveListener Interface
====================================

Motivation
----------

The LiveListeners are not flexible enough and cause problems at collaborator facilities and external facilities where Mantid is used. Specific problems listed below.


Problems To Fix
---------------

**Mandatory**

1. *Listener Properties* in StartLiveData should update dynamically based on properties that the specific `LiveListener` has.
1. Should support multiple LiveListeners (multiple addresses/connection string) per instrument.
1. Should be able to create a specific LiveListener via the StartLiveData algorithm by specifying the address and class, without querying the facilities.xml / InstrumentInfo.
1. Should be able to plug new specific LiveListener implementations into an existing Mantid install.


How Things Currently Work
-------------------------

* The **Facilities.xml** file allows you to specify listeners like this `<livedata address="NDXENGINX:10000" listener="ISISLiveEventDataListener" />`. The listener is the concrete ILiveListener class name that will be used to create ILiveListener objects. If a listener is not specified at the instrument level, then the listener at the facilities level of the xml hierarchy will be used instead.
* Listeners specified in the **Facilities.xml** file are created in the `LiveListenerFactory` via [DynamicFactory::create](https://github.com/mantidproject/mantid/blob/master/Framework/API/src/LiveListenerFactory.cpp#L44:L45) from a `std::string`
* The bare listener objects are connected via `ILiveListener::connect(const Poco::Net::SocketAddress &address)`
* Once a connection has been made. The listener can be Started, Stopped.  
* The main hook point is extractData() `virtual boost::shared_ptr<Workspace> extractData() = 0;`
* Each implementation of the `ILiveListener` has the ability to receive and use additional properties at runtime. More below.


ILiveListener as a PropertyManager
----------------------------------

* `ILiveListener` inherits from `PropertyManager` 
* `LiveDataAlgorithm` is the base type of `StartLiveData` and other algorithms using the live data streams.
* `LiveDataAlgorithm` calls the `LiveListenerFactory` via it's `LiveDataAlgorithm::getLiveListener()` method [here](https://github.com/mantidproject/mantid/blob/master/Framework/LiveData/src/StartLiveData.cpp#L146)
* Crucially in `LiveDataAlgorithm::getLiveListener()` it passes a pointer to itself through to the `LiveListenerFactory::create()`.
* Remembering that `LiveDataAlgorithm` is also a type of `PropertyManager`, the `LiveListenerFactory::create()` is then able to copy all it's properties over to the specific `ILiveListener` type. This is done [here](https://github.com/mantidproject/mantid/blob/master/Framework/API/src/LiveListenerFactory.cpp#L48)
* Now the `LiveDataListener` has the same properties as the calling algorithm, it has access to things like the `SpectraList` off the calling algorithm. Example [here](https://github.com/mantidproject/mantid/blob/master/Framework/LiveData/src/ISISHistoDataListener.cpp#L105)


Order of Connection
-------------------

As used at the moment, `LiveDataAlgorithm` has a gateway function called [getLiveListener](https://github.com/mantidproject/mantid/blob/master/Framework/LiveData/src/LiveDataAlgorithm.cpp#L186:L197), which forces `LiveListenerFactory::create()` to return a `ILiveDataListener` on which connect has been called because the connect argument is set to true. `getLiveListener` also starts the listener. If you don't have enough information to start the connection at that point, the connection will simply fail.


Questions
---------
Mark mentioned that we are missing a Watcher Algorithm. It's unclear what is required that's not already handled by `MontiorLiveData` and `LoadLiveData` via `StartLiveData`?


Partial Solution Options
------------------------

### Option 1: Add Named Component Option

The general problem we are trying to solve is that the instrument is assumed to have a single live listener. This solution introduces the possibility of more than one live listener per instrument and introduces a name key. The resulting xml can then take this form

```xml
 <instrument name="LET_EVENT" shortname="LET">
    <zeropadding size="8"/>
    <technique>Neutron Spectroscopy</technique>
    <technique>TOF Direct Geometry Spectroscopy</technique>
    <livedata default_name="instrument">
     <connection address="NDXLET:10000" listener="ISISLiveEventDataListener" name="instrument" />
     <connection address="NDXLET:10001" listener="ISISLiveEventDataListener" name="detector1" />
     <connection address="NDXLET:10002" listener="ISISLiveEventDataListener" name="bank1" />
    </livedata>
  </instrument>
```
The `LiveDataAlgorithm` base class is then given the ability to provide an optional name input.


#### Solution Details

1. Currently LiveListener XML gets parsed [here in FacilityInfo](https://github.com/mantidproject/mantid/blob/master/Framework/Kernel/src/FacilityInfo.cpp#L139:L146) for facility level listeners  and [here in InstrumentInfo](https://github.com/mantidproject/mantid/blob/master/Framework/Kernel/src/InstrumentInfo.cpp#L223:L250) for instrument level listeners. The latter is the most important in this context. `InstrumentInfo` has `m_liveDataAddress` and `m_liveListener` (name of class to create object from).
1. We create with a new type called `LiveListenerInfo`. The two attributes should be members of this new type. `name` should also be added as a member, but may not be initialized (empty string). `LiveListenerInfo` should be first-class citizen in Mantid like `FacilityInfo` and `InstrumentInfo`.
1. Refactor Mantid to use the above `LiveListenterInfo`. For example, it could be returned from [InstrumentInfo::livelistener()](https://github.com/mantidproject/mantid/blob/master/Framework/Kernel/inc/MantidKernel/InstrumentInfo.h#L68).
1. Give InstrumentInfo the ability to return all LiveListenerInfo (as a collection) via a new method.
1. [Fix this](https://github.com/mantidproject/mantid/blob/master/Framework/API/src/LiveListenerFactory.cpp#L36) to take a name string, that defaults to an empty string. If specified it should use that to select the right LiveListenerInfo to create the LiveListener from. Otherwise it should just create one without any name specified. [LiveDataAlgorithm::getLiveListener](https://github.com/mantidproject/mantid/blob/master/Framework/LiveData/src/LiveDataAlgorithm.cpp#L186:L197) should take the name string and forward it to the above method. `LiveDataAlgorithm` should provide an additional non-mandatory property called "Name", if the "Name" property is provided, it should be checked at validateInputs() time against possible Name options available for the selected "Instrument" property declared in [LiveDataAlgorithm](https://github.com/mantidproject/mantid/blob/master/Framework/LiveData/src/LiveDataAlgorithm.cpp#L55)


### Option 2: Overload the `LiveListenerFactory` connect

Currently `LiveListenerFactory::create` as called by `LiveDataAlgorithm` will:

1. Load the Instrument and then InstrumentInfo for the specified *Instrument* name argument. All taken from the Facility file.
1. Extract the concrete ILiveListener from the above and create an instance of one.
1. Connect it from the address specified in the Facilities.xml.

The only thing that any `create` method should do is create the relevant object, and we should have a way of providing the ILiveListener class name ourselves, and connecting the product ourselves.

The completed solution would allow users to specify the stuff usually loaded from the facilities.xml file directly in `StartLiveData`. Namely, the address, ILiveListener name and component name. If provided, the code would not try to then fetch that information from the instrument.

**In this solution users would be able to use `StartLiveData` and completely bypass the Facilities.xml file.** Again, this can be added in parallel to the above fixes.


Proposed Solution
-----------------

#### Requirement 1

Dynamic properties for listeners were already supported previously, but this feature was removed in [PR #234](https://github.com/mantidproject/mantid/pull/234) in response to [Trac #11059](http://trac.mantidproject.org/mantid/ticket/11059) because it interfered with help generation and Python API support.

Reverting this PR will satisfy this requirement, but we will need to deal with the help and Python issues in a different way. This is beyond the scope of this design and can be handled separately.

#### Requirement 2

Support for multiple LiveListeners can be implemented using Option 1, described above.

This will require changes to the way existing code and interfaces work. Facilities.xml should also be updated to replace workaround constructs like:

```xml
  <instrument name="ENGIN-X" shortname="ENGINX" >
    <zeropadding size="8"/>
    <technique>Neutron Diffraction</technique>
    <livedata address="NDXENGINX:6789" />
  </instrument>

  <instrument name="ENGIN-X_EVENT" shortname="ENGINX" >
    <zeropadding size="8"/>
    <technique>Neutron Diffraction</technique>
    <livedata address="NDXENGINX:10000" listener="ISISLiveEventDataListener" />
  </instrument>
```

With a single instrument that has two connection types:

```xml
  <instrument name="ENGIN-X" shortname="ENGINX" >
    <zeropadding size="8"/>
    <technique>Neutron Diffraction</technique>
    <livedata default="histo">
      <connection name="histo" address="NDXENGINX:6789" listener="ISISHistoDataListener" />
      <connection name="event" address="NDXENGINX:10000" listener="ISISLiveEventDataListener" />
    </livedata>
  </instrument>
```

#### Requirement 3

Supporting direct LiveListener instantiation using a class name and connection string will require either modifying the existing `LiveListenerFactoryImpl::create` method, as per Option 2 above, or overloading it. The proposed solution is to overload it to provide an alternative while minimizing impact on existing code.

The existing `create` method can be modified to function the same way it does now, but internally call the new `create` method, passing in the class name and address retrieved from Facilities.xml. `LiveDataAlgorithm` and `StartLiveData` (as well as its dialog) will need to be modified as well, to provide a user interface and call LiveListenerFactory accordingly.

By adding a "Connection" group under the "Instrument" drop down box, to select an address / listener pair defined in the Facilities.xml using a drop down box, or to specify a custom address and listener, we could support both the general use case and allow for custom setups.

#### Requirement 4

This feature is already supported, but poorly documented and therefore not well known. The proposed solution is to improve documentation and provide a minimal but fully working example implementation to showcase how one could plug a new specific listener into an existing Mantid install without rebuilding any part of Mantid.
