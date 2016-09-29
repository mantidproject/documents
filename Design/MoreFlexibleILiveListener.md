More Flexible LiveListener Interface
====================================

Motivation
----------

The LiveListeners are not flexible enough and cause problems at collaborator facilities and external facilities where Mantid is used. Specific problems listed below.


Problems To Fix
---------------

**Mandatory**

* Should be able to create a specific LiveListener via the StartLiveData algorithm by specifying the address and class, without querying the facilities.xml / InstrumentInfo.
* Should support multiple LiveListeners (multiple addresses/connection string) per instrument
* Should be able to plug new specific LiveListener implementations into an existing Mantid install.


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


