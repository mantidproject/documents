
Introduction
============

This is a tiny document to specify where the different Python plotting
modules should go and what namespaces should be used for them.

Proposed changes for 3.4
========================

Main changes
------------

* Bring future.pyplot out of future and import it as pyplot. In
[mantidplotrc.py](https://github.com/mantidproject/mantid/blob/master/Code/Mantid/MantidPlot/mantidplotrc.py) or in mantidplot.py (imported from there) there would an import like this:
```python
import pymantidplot.pyplot
from pymantidplot.pyplot import *
```
to import the module and bring it into the standard MantidPlot
namespace.

* This will cause at least one name clash with the traditional
  mantidplot plot() function. This function could be moved into a
  (new) module `qtiplot` which would be also imported in
  [mantidplotrc.py](https://github.com/mantidproject/mantid/blob/master/Code/Mantid/MantidPlot/mantidplotrc.py).

* As the change from `plot()` to `qtiplot.plot()` breaks backwards
  compatibility, the documentation (and also course material, etc.)
  needs to be checked and updated.

Additional changes
------------------

* For the names of the tools in the plot commands, there will be
  aliases with and without the `tool_` prefix, and for the `spectrum`
  tool there will be a shorter alias: `sp`.

