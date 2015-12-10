More flexible live listener interface
=====================================

Motivation
----------

ILiveListener interface requires that an implementation takes only the instrument name and a network address to create itself. 
If these are not enough there is no way to pass additional information in. For external facilities, we need the ability to provide flexible listners via the plugin/dll mechanism offered via the dyanmic factories, that way custom dependencies can be managed by those external facilities and not added to all distributions of Mantid.

How Things Currently Work
-------------------------

* The *Facilities.xml* file allows you to specify listeners like this `<livedata address="NDXENGINX:10000" listener="ISISLiveEventDataListener" />`
* Listeners speicified in the *Facilities.xml* file are created via the LiveListenerFactory DynamicFactory [here](https://github.com/mantidproject/mantid/blob/master/Framework/API/src/LiveListenerFactory.cpp#L44:L45) from a `std::string`
* The bare listener objects are connected via `connect(const Poco::Net::SocketAddress &address)`
* Once a connection has been made. The listener can be Started, Stopped. See full API for more functions. 



Possible solutions
------------------

### Dynamic properties on StartLiveData

1. `ILiveData` is a property manager and can have properties.
2. `StartLiveData` creates disconnected instance of a ILiveListener in its init() method.
3. It copies properties from the listener (dynamic properties). 
4. The properties are set by the caller.
5. The exec() method passes the set properties to the listener and connects it.

The instrument name should be enough for creating a disconnected listener. ILiveListener::connect() doesn't have to have an argument.
The neccessary information can be provided through properties.

### Not using ILiveListener

Unofficial Mantid plugins do not have to use ILiveListener to collect live data. If the interface is incompatible with the
instrument's systems the plugin can define an independent custom algorithm for collecting data. MantidPlot can be configured
to use this algorithm instead of StartLiveData in Load->Live Data button menu.
