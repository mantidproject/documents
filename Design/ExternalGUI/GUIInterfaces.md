## Summary

This document details a design for robust handling of registering user interfaces with the MantidPlot workbench, whether the code be internal to the [mantid repository][mantid_repo] or externally managed.

## Current Implementation

We currently have 2 approaches for registering a new user interface such that it can be started from MantidPlot:

1. C++ interfaces use the [`DECLARE_SUBWINDOW`][macro_subwindow] macro to register themselves into the [InterfaceFactor][interface_factory] when
their shared library is loaded. MantidPlot startup code checks these registrations and populates the menu accordingly. The menu under "Interfaces"
is specified by the `category()` method on the main window.
1. Python interfaces define a startup file, e.g.
[HFIR_Powder_Diffraction_Reduction.py][hfir_startup_file] and also place
an entry in the `mantidqt.python_interfaces` key in the [properties file][properties_file]. MantidPlot startup code separately checks this key and populates
the menu accordingly. The menu is specified by the text preceding the forward slash in the properties file.

While this is functional it requires maintenance of two entirely separate mechanisms of registration. The Python mechanism also requires changes in two
locations of the code that are entirely separate from each other the mapping from the keys to the interfaces menu is not clear.

Externally-managed interfaces, for example [MSlice][mslice_repo], are developed to be able to be used standalone but also need
to be able to be accessed from inside MantidPlot. The current mechanism makes this more difficult due to lack of a defined interface to the Python-based GUIs.


## Proposed Solution

It is proposed that the current mechanism for registration in C++ be slightly refactored and extended to Python as described in the following diagram:

![InterfaceDescription Class Diagram](InterfaceMetadata.png?raw=true)

The `InterfaceMetadata` class separates the metadata describing a given user interface with the interface itself. Currently the `name`/`category` information
is directly attached to main window of the C++ interfaces using static methods so that the classes do not need to be instantiated on registration. At runtime
the base implementations throw an exception if they have not been overridden. In the new scheme the metadata classes are lightweight classes using pure-virtual
methods allowing this kind of missing behaviour to be detected at compile time.

The `showUI` method accepts an optional parent widget and is responsible for constructing & showing the UI itself.

By exposing the `InterfaceMetadata` and `InterfaceFactory` classes to Python we can expand this registration mechanism to encompass the Python interfaces also. This will
require minimal modification to the current startup files (see below). MantidPlot will then have single point, `InterfaceFactory` where it is able to query for
information regarding the various customized interfaces. The `InterfaceFactory::populateMenu` method will fill a given `QMenu` instance with the known list of
items without requiring external code to extract and parse stored list.

### Sample Python Metadata File

Below is an example of updating the current [HFIR powder GUI][hfir_startup_file] startup file to understand the new mechanism. It is written to be able to be started
standalone from the command line or from within MantidPlot.

```python
import sys

from HFIRPowderReduction import HfirPDReductionGUI
from PyQt4 import QtGui

def show():
    reducer = HfirPDReductionGUI.MainWindow() #the main ui class in this file is called MainWindow
    reducer.show()
	return reducer

if __name__ == "__main__":
    from PyQt4 import QtGui
    qapp = QtGui.QApplication.instance() if QtGui.QApplication.instance() else QtGui.QApplication(sys.argv)
	show()
	qapp.exec_()
else:
	import mantidqt

	class HFIRPowderMetadata(mantidqt.InterfaceMetadata):

	    def name(self):
            return "HFIR Powder Diffraction Reduction"

        def category(self):
            return "Diffraction"

        def showUI(self):
            show()

    mantidqt.InterfaceFactory.subscribe(HFIRPowderMetadata)
```

## Code Layout

While not a prerequisite for these changes it would be beneficial while analysing the interface code to assess the current layout in the repository. We have two locations for
interfaces at the time of writing:

1. C++ interfaces live in the [MantidQt/CustomInterfaces][mantidqt_custominterfaces] library
1. Python interfaces are scattered in the [scripts][scripts] directory.

A overview simply overview of the code directories does not given any simple indication of how many interfaces are contained within the project. Ideally the C++ "CustomInterfaces" shared
library would be refactored to split each interface into its own library and own set of directories with the Python interfaces living along side them so that

1. an interface is isolated from all others and changes to one along with its tests does not require a full rebuild of all C++ interfaces.
1. easier to find interface code and see what is related to a single one.
1. modification of a Python interface would no longer trigger a build of the system tests on a PR as we could exclude those folders.

**Question: Is this scope creep?**

## Externally-Managed Code

PLACEHOLDER

### Documentation

PLACEHOLDER


<!-- Link definitions -->

[mantid_repo]: https://www.github.com/mantidproject/mantid
[mslice_repo]: https://www.github.com/mantidproject/mslice
[macro_subwindow]: https://github.com/mantidproject/mantid/blob/636367aff41d00a13f23514f90065f5aa1044dfa/MantidQt/API/inc/MantidQtAPI/UserSubWindow.h#L9
[hfir_startup_file]: https://github.com/mantidproject/mantid/blob/master/scripts/HFIR_Powder_Diffraction_Reduction.py
[interface_factory]: https://github.com/mantidproject/mantid/blob/master/MantidQt/API/inc/MantidQtAPI/InterfaceFactory.h
[properties_file]: https://github.com/mantidproject/mantid/blob/master/Framework/Properties/Mantid.properties.template
[mantidqt_custominterfaces]:https://github.com/mantidproject/mantid/tree/636367aff41d00a13f23514f90065f5aa1044dfa/MantidQt/CustomIntefaces
[scripts]:https://github.com/mantidproject/mantid/tree/636367aff41d00a13f23514f90065f5aa1044dfa/scripts
