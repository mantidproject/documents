
Introduction
============

This is a tiny document to specify where the different Python plotting
modules should go and what namespaces should be used for them.

Proposed changes for 3.4
========================

Main changes
------------

* Bring future.pyplot out of future and import it as pyplot. In
[mantidplotrc.py](https://github.com/mantidproject/mantid/blob/master/Code/Mantid/MantidPlot/mantidplotrc.py)
there would be a line like:
```python
import pyplot
```

* This will cause at least one name class with the traditional
  mantidplot plot() function. This function could be moved into a
  module `qtiplot` which would be also imported in
  [mantidplotrc.py](https://github.com/mantidproject/mantid/blob/master/Code/Mantid/MantidPlot/mantidplotrc.py).

* As the change from plot() to qtiplot.plot() breaks backwards
  compatibility, the documenation (and also course material, etc.)
  needs to be checked and updated.

Additional changes
------------------

* As Nick came up with the same idea to drop the `tool_` prefix as was
  already proposed in [trac ticket
  #11075](http://trac.mantidproject.org/mantid/ticket/11075), it would
  be worth discussing this again.

* Provide an alias for `tool_spectrum`: `tool_sp`, or `sp` if we drop the `tool_` prefix.
