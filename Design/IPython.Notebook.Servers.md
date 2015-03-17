# IPython Notebook Servers

The purpose of this document is to examine the possibility of hosting an IPython
notebook server, upon which instrument scientists, and possibly users, can work
with Mantid.

This is for ticket [#10826](http://trac.mantidproject.org/mantid/ticket/10826).

## Overview

Currently (v3.4), the Mantid Framework seems to work very well inside of IPython
Notebooks. All the features provided by the Python bindings are functioning
correctly, with the obvious exception of the MantidPlot integration.

Example IPython Notebooks demonstrating the use of Mantid are available from the
[Mantid Download Page](http://download.mantidproject.org/). These use Mantid to
load and process data, and pymatplotlib to embed graphs of the data into the
IPython Notebook.

## Security

Executing code sent from the client side is always a risky prospect from a
security perspective, and it's notoriously difficult to sandbox Python without
some operating system level support.

The official stance of the IPython project is simply to only allow trusted users
the ability to access the notebooks, or execute code at all. They provide the
ability to protect the notebook by requiring a password to login, and supporting
TLS (i.e. HTTPS). This approach is perfectly adequate if for users running their
own private notebooks and wanting remote access, but unsuitable for the use case
of providing multiple notebooks to multiple users on a single server.

It is possible to provide our own security around the notebook by running a
reverse proxy with authentication that gives users access to their own personal
instance of IPython Notebook running inside a container. This could be achieved
with a tool such as [docker](https://www.docker.com). Using docker could
simplify administration, and provide an easy way to scale the back-end across
many machines.

## Use Cases

While an IPython Notebook server can feasibly be set up with Mantid in a secure
and scalable way, it's still unclear what exactly it would be used for.

One use would be for instrument scientists to provide examples and
demonstrations on how to work with data from a particular instrument. However,
it's arguable that such examples would be better of being part of the main
documentation.

Another use case is for users to actually work with their data
on a high-performance server from a low-power laptop, or even a tablet. While
this is an attractive prospect, it also has its disadvantages:
limited integrated documentation, an awkward graphing interface, and no custom
interfaces.
