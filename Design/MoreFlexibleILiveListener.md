More flexible live listener interface
=====================================

Motivation
----------

ILiveListener interface requires that an implementation takes only the instrument name and a network address to create itself. 
If these are not enough there is no way to pass additional information in. For external facilities, we need the ability to provide flexible listeners via the plugin/dll mechanism offered via the dyanmic factories, that way custom dependencies can be managed by those external facilities and not added to all distributions of Mantid.

How Things Currently Work
-------------------------

* The *Facilities.xml* file allows you to specify listeners like this `<livedata address="NDXENGINX:10000" listener="ISISLiveEventDataListener" />`. The listener is the concrete ILiveListner class name that will be used to create ILiveListener objects. If a listner is not specified at the instrument level, then the listener at the facilities level of the xml hierachy will be used instead.
* Listeners speicified in the *Facilities.xml* file are created via the `LiveListenerFactory` `DynamicFactory`  [here](https://github.com/mantidproject/mantid/blob/master/Framework/API/src/LiveListenerFactory.cpp#L44:L45) from a `std::string`
* The bare listener objects are connected via `connect(const Poco::Net::SocketAddress &address)`
* Once a connection has been made. The listener can be Started, Stopped.  
* The main hook point is extractData() `virtual boost::shared_ptr<Workspace> extractData() = 0;`
* Each implementation of the `ILiveListner` has the ability to receive and use additional things at runtime. More below.

ILiveListner as a PropertyManager
##################################

* `ILiveListener` inherits from `PropertyManager` 
* `LiveDataAlgorithm` is the base type of `StartLiveData` and other algorthims using the live data streams.
* `LiveDataAlgorithm` calls the `LiveListenerFactory` via it's `LiveDataAlgorithm::getLiveListener()` method [here](https://github.com/mantidproject/mantid/blob/master/Framework/LiveData/src/StartLiveData.cpp#L146)
* Crutially in `LiveDataAlgorithm::getLiveListener()` it passes a pointer to itself through to the `LiveListenerFactory::create()`.
* Remembering that `LiveDataAlgorithm` is also a type of `PropertyManager`, the `LiveListenerFactory::create()` is then able to copy all it's properties over to the specific `ILiveListener` type. This is done [here](https://github.com/mantidproject/mantid/blob/master/Framework/API/src/LiveListenerFactory.cpp#L48)
* Now the `LiveDataListener` has the same properties as the calling algorithm, it has access to things like the `SpectraList` off the calling algorithm. Example [here](https://github.com/mantidproject/mantid/blob/master/Framework/LiveData/src/ISISHistoDataListener.cpp#L105)

Problems To Fix
---------------

**Mandatory**

* As used at the moment, LiveDataAlgorithm has a gateway function called [getLiveListener](https://github.com/mantidproject/mantid/blob/master/Framework/LiveData/src/LiveDataAlgorithm.cpp#L186:L197), which forces `LiveListenerFactory::create()` to returns a `ILiveDataListener` on which connect has been called because connect is set to true. getLiveListener also starts the listener.If you don't have enough information to start the connection at that point. The connection will simply fail. In addition, even if you have dynamic properties that could be used to create a connection, these cannot be used because `LiveListenerFactory::create()` will establish the connection first, and then copy dynamic properties over.
* Knowing the Instrument is not enough. The `LiveListenerFactory` uses the instrument name to get the `InstrumentInfo` and from that the connection properties. But this does not allow support for more than one live data stream per instrument.

**Nice To Fix**

* Reliance on runtime properties is cumbersome. If I want to create an ILiveListner, I need to call it from something that implements all the machinery of `PropertyManager`.

Questions
---------
Mark mentioned that we are missing a Watcher Algorithm. It's unclear what is required that's not already handled by `MontiorLiveData` and `LoadLiveData` via `StartLiveData`?


Possible solutions
------------------

### Dynamic properties on StartLiveData

One problem is that properties are applied after connections are made. A simple fix would be to reorder the `LiveListenerFactory::create` so that properties are always copied between calling `Algorithm` and `ILiveListener` immediately after creation of the `ILiveListner` and before any connection is called. This will give much more power to each subtype of `ILiveListener` to decide to override the standard connection information such as address etc if it has been provided as a dynamic property.

### Not using ILiveListener

Unofficial Mantid plugins do not have to use ILiveListener to collect live data. If the interface is incompatible with the
instrument's systems the plugin can define an independent custom algorithm for collecting data. MantidPlot can be configured
to use this algorithm instead of StartLiveData in Load->Live Data button menu.
