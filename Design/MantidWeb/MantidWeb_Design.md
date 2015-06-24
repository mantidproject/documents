# MantidWeb

## Introduction

One of the major goals for the Mantid v3.6 release is a web based Mantid UI.
For my final year project at university, I (Harry Jeffery) will be developing
a web based user interface for Mantid. This document describes the design I
currently intend to implement.

## User Requirements

For the interface to be useful to users, I have identified some requirements
that the interface must fulfil to be useful, and some additional requirements
that I'd like to fulfil, but aren't essential.

### Hard Requirements

* It must be possible to run an instance locally
* It must be possible to run multiple instances on a single server for multiple
  users to connect to.
* Users must be able to instantiate and run algorithms
* Users must be able to view and plot workspaces
* Users must be able to load and save their data
* Separate users' instances must not interfere with one another

### Soft Requirements

* The interface should be usable on a tablet
* Users should be able to control the same instance of Mantid from more than
  one browser at a time.
* The ability for users to use Python within Mantid safely, i.e. unable to
  interfere with the server running Mantid.

### Long term possibilities

* Users could be given the ability to share their instances of Mantid with
  another user. i.e. The ability for an instrument scientists to remotely access
  a users' instance of MantidWeb and assist them with it.

## Technical Requirements

The following requirements are implementation details that need to be taken into
account to enable such an interface to be maintained and developed long term.

* As few new technologies as possible should be used. C++, Python and JavaScript
  should be the only languages required for maintenance.
* Centrally hosted clusters of MantidWeb should be reasonably easy to manage.

## Design Overview

The design I propose consists of two main components:

* **MantidWeb** - A HTML+JavaScript interface
* **MantidHTTP** - A C++ shim over the Mantid Framework providing a HTTP or
  websockets API for MantidWeb to interact with.

These two components should communicate using a clearly defined API to keep
them loosely coupled. It ought to be possible for several different MantidWeb
implementations to exist, all able to communicate with MantidHTTP, but in
practice I expect there to only be one.

MantidHTTP should be a very simple command-line application with as few
dependencies as possible. It should be simple enough that *all* of its options
can be set as command line flags. Upon launching it starts listening on a given
port, providing the HTTP/websockets interface to an instance of the Mantid
Framework. Through its command line options it should be possible to define
which interface and port to listen on, which directories should the user be
able to access and load or save data from or to, and possibly the ability to
blacklist algorithms, or set resource usage quotas. It must be possible to
set an *authentication token* that acts as a password to connect to that
specific instance. The handling of such an auth token would happen invisibly to
users.

MantidWeb is the more sophisticated part of the design. It is a HTML and
JavaScript web application that connects to MantidHTTP and provides a graphical
interface for users to interact with Mantid through.

I also suggest a third, optional component: the *gateway*. The gateway would be
a fairly simple web application written in Python. Its purpose is to act as an
entry point to the web interface when many instances are being hosted centrally
for users, such as at a facility.

Its responsibilities consist of authenticating users, serving users MantidWeb,
and starting up instances of MantidHTTP for MantidWeb to connect to. It would do
all this transparently for the user. The user simply connects to the gateway and
logs in with whichever credentials the gateway has been programmed to accept.
The gateway then sends the user's browser MantidWeb along with the address and
*authentication token* of their instance of MantidHTTP. The user would simply
see MantidWeb open, ready to use.

Delegating these tasks to the gateway brings great flexibility. Different users
can be given different versions of MantidWeb, or even be given a choice of which
to use. Users can have their MantidHTTP sessions persist between connections,
and be reconnected to their existing session. Users could even be allowed to
have multiple sessions to choose from, or be able to share their session with
other users. The gateway can be on a completely separate machine from all the
instances of MantidHTTP, and those instances could be load balanced across
many servers if required, and since the only time the gateway is required is
at login, the load upon it would be fairly low.

To give a clearer picture of how this would work in practice, here is an ascii
art sequence diagram showing how a user connecting to MantidWeb for the first
time might look.

```
    +---------+          +---------+               +---------------+
    | browser |          | gateway |               | mantid server |
    +----+----+          +----+----+               +-------+-------+
         |                    |                            |
  |      |      connect       |                            |
  |T     |------------------->|                            |
  |i     |    login form      |                            |
  |m     |<-------------------|                            |
  |e     |   login details    |                            |
  |      |------------------->|                            |
  V      |                    |   start an instance        |
         |                    |--------------------------->|
         |                    |      instance details      |
         |                    |<---------------------------|
         |  HTTP + javascript |                            |
         |   interface and    |                            |
         |  instance details  |                            |
         |<-------------------|                            |
         |                    +                            |
         |                                                 |
         |         API requests and responses              |
         |<----------------------------------------------->|
         +                                                 +

```

Another advantage of delegating all these responsibilities to the gateway is 
that it becomes very easy for both users and developers to run isolated
instances locally. All it takes is a small python script that launches
MantidHTTP on a local port, and the python module *SimpleHTTPServer* to serve
MantidWeb locally.

Large scale deployment of this architecture is also straightforward. Individual
instances of MantidHTTP can be run inside of docker containers, allowing for
easy administration and isolation of users. If a user is misbehaving and using
all of the server's CPU time then their instance can be shut down without any
risk of disrupting other users. Users can also be allowed access to Python as
they are isolated inside their container, and so there is no risk of them
damaging the server.

Using tools like docker swarm, or even some custom python scripts, new instances
of MantidHTTP could be started in seconds and load balanced across an unlimited
number of servers with a very low administrative burden.

## MantidHTTP Implementation

Since the Mantid Framework is implemented in C++, MantidHTTP can only be
implemented using C++ or Python. I have investigated using Python but found the
Python bindings too limited for the purposes of MantidHTTP, so this component
must be written in C++.

This component should be kept as slim as possible, but easy to extend. It needs
to provide access to algorithms and workspaces in a generic way at the very
minimum. Other than the Mantid Framework, the only dependency this should have
is the C++ library or libraries required to provide the HTTP API. *Qt* must not
be required. There should be no interdependency with MantidPlot so that this
can be run on a headless server with no graphical interface. The fewer
dependencies this component has, the easier it is to deploy in production.

## MantidWeb Implementation

Due to its nature, this component must obviously be developed in HTML with CSS
and JavaScript. However, within these technologies there is a rich variety of
frameworks, libraries and techniques to choose from. Whichever approach is used
must be clearly documented and straight-forward to extend, as this will be the
most difficult component to maintain long term, and will be the most complex.

It's worth noting that due to Mantid Framework's fairly generic interface for
algorithms, support only needs to be added for creating algorithms and modifying
their properties before running them to support almost all of the functionality
of Mantid. The same is true of workspaces, and with the multitude of both 2D and
3D plotting libraries available for JavaScript it should be fairly easy to add
support for beautiful plots and graphs.

## Custom Interfaces

The one key area of Mantid that's notably missing from this proposal is
custom interfaces, and that is because they are strongly tied to MantidPlot and
Qt, and short of re-implementing them in JavaScript, there's not much that can
be done to provide them in MantidWeb.

One long term possibility is to provide an abstraction over workflow algorithms
that provides a step-by-step interface for processing data. They would exist as
Python scripts that emit generic forms, perhaps as XML or JSON. These forms
would then be turned into either Qt or HTML interfaces, providing the user with
information on what inputs are expected. The user could then fill in the forms
and the values would be given to the script for processing. The script could
then emit a new form, and this process would continue in a step-by-step format.

With this technique, a set of cross-interface custom interfaces could be
developed, providing an easy way for users to process their data. The main
drawback to this is it's only appropriate for a limited number of techniques.
Interfaces such as the fitting or reflectometry reduction interfaces do not suit
this an abstraction at all, and would require something more specialised.

## Data Management

Users' ability to access their data is critical to the usefulness of this
interface. The approach I propose is for MantidHTTP to expose a configurable
directory for loading and saving data. Users could then browse the directory
and its children for their data, load it, process it, and then save their
results to either the same directory, or another. Allowing users to upload
or download files from this directory is out of scope, and ought to be managed
as a separate system. All MantidHTTP should care about is which directories
users are allowed to see, and whether they can read them or write to them.

It should also be possible for users to retrieve their data using ICAT, using
Mantid's ICAT algorithms. A MantidWeb interface could be constructed to allow
doing this easily from within the web ui.

## EOF

This document is a proposal for how I would go about building such an interface,
and nothing is set in stone. Feedback would be very much appreciated at this
stage, so that a design that accommodates the users' needs can be developed
before any code is written.
