# Architecture

This document describes the architecture of the new workbench. It includes the intended design for the `mantdidqt` package.

For reference the overall layout mockup is shown here:

![Overall Workbench Layout](main-layout.png)

The central widget will be a tabbed-widget that will not be movable and 1 tab will be reserved for the embedded IPython console. It should be possible to drag an individual tab out of the window to be displayed on another monitor, for example.

- **Question: Where should the controls for script execution go? I would suggest just on the main menu, with appropriate shortcuts set.**


# Automated Testing

One of the most common complaints about the existing MantidPlot application is stability. We must take a proactive approach to automated testing within the new workbench. Where possible we will use common patterns such as
[MVP][mvp-fowler] to facilitate automated testing of the GUI elements and provide a better seperation of concerns within the code.

For existing code and code that would possibly be rendered more difficult to work with using MVP then the suggestion would be to supplement the pattern approach with testing via the [Qt Test][qttest] library. It allows
unit testing of Qt applications and libraries. Particularly for our existing interface/widget code this would provide some sort of automated testing that is currently lacking. This seems to be used quite successfully within
the [Jupyter Qt Console][jupyter-qtconsole], for example.

# User Interface Registration

It is proposed that the current mechanism for interface registration in C++ be slightly refactored and extended to Python as described in the following diagram:

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

**Note: This obseletes the design in [this pull request](https://github.com/mantidproject/documents/pull/40).**

# `mantidqt` library

This library will form the guts if the new application and will contain most of the components that will be pieced together to form the workbench. The details of the built/installed layout are:

```
mantidqt
  |-- plotting
  |   |-- cli
  |-- reduction_gui
  |-- scripting
  |-- tests # contains testing for the package
  |-- utils
  |   |-- __init__.py
  |   |-- qt.py
  |-- widgets
  |   |--common
  |   |  |-- _widgets.dll # sip wrapped library from C++ widgets, includes InterfaceMetaData class from above.
  |   |  |-- new_python_widget.py
  |   |-- plugins
  |   |   |-- algorithm_dialogs
  |   |-- instrumentview
  |   |   |-- tests
  |   |-- sliceviewer
  |   |   |-- tests
  |   |-- spectrumviewer
  |   |   |-- tests
  |-- __init__.py
```


## Widgets

The intention is that the workbench be comprised, as much as possible and sensible, of reusable widgets. These widgets will live in a new `mantidqt.widgets` subpackage (see [layout](design-layout.md) for it's layout within the rest of the source code). Other packages should be able reuse these widgets so they must not make an assumption about their running environment.

The current list of widgets contained within the existing [widgets][mantidwidgets] library will be resued where appropriate. Some more commonly used widgets shall be supplemeted with tests using the Qt Test framework rather than
writing them from scratch. A notable exception to this list would be the new variable explorer. As this is significantly different to the current workspace list view it would be better implemented from scratch.

### Plugins

This subpackage will contain plugins such as the algorithm dialogs. This will be loaded on demand the first time the InterfaceFactory is requested to create a dialog. This should again reduce the loading overhead.

### Instrument View/Slice Viewer/Spectrum Viewer...

These will be separate libraries so that for example another application could embed the instrument view widget. The DLLs internal to those subpackages will only be loaded when that subpackage is imported to reduce
the loading overhead and to not make users pay for features they do not use.

### Reduction Gui

This will contain the `reduction_gui` framework currently used by many customized interfaces.

### Scripting

This will contain the code related to executing scripts including a "runner" class that can execute arbitrary code, a code editor plus an in-process Qt IPython console.

## Plotting

`matplotlib` will provide the plotting abilities within the new workbench. It exposes all classes as an object-oriented API but also provides a procedural, state-machine api, `pyplot` interactive programming.

In `pyplot` matplotlib provides a default window/toolbar that provides basic tools. This will be inadequate for our users so we will develop a custom toolbar for our the 1D, 2D and 3D plot types. We will provide a `cli` module
that mimics the `pyplot` api but uses our defaults (configurable) for toolbars/window etc. Matplotlib uses a [tool][mpl-boilerplate] to generate their `pyplot` api. We can do something similar.

By providing an alternate `cli` module we can preserve access to the standard `matplotlib.pyplot` module should anyone want access to this. A snippet of code such as:

```python
try:
    import mantiqt.plotting.cli as plt
except ImportError:
    import matplotlib.pyplot as plt
```

would allow a script to function either using our cli or the built-in matplotlib one.

### 1D Plots

![1D Plot](1d-plot-window.png)

### 2D Plots

![2D Plot](2d-plot-window.png)

These figures are meant to serve as a guide and will need to be tweaked as they are developed.

### Figure Management

It is desirable within the plotting framework to have a mechanism for controlling how figures are managed. For example, when `plot` is called without specifying a window then we must make a choice of either:

 - create a new figure or
 - merge/overplot with an existing figure.

The initial propsosal is to borrow ideas from the [mslice][mslice] and have a controls on the figures so that users can indicate what is to be done with this window. In the figures above each figure contains a pair of
buttons `Hold/Active` or `Held/Active` (depending on its state). These buttons control what happens when a plotting function is called without explicit intent as to which figure it should affect.

- Hold: This window should be *frozen* and left as it is. Further plotting should be done in a new window. The text of the button changes to *Held* and the background colour to *red*.
- Active: This window is the *active* window for this plot type (separate lists maintained for 1D, 2D, 3D). Further plotting will **replace** the contents of this window. The  background colour of Active goes to  *green* and the `Held/Hold` button text is set back to *Hold* and its background back to gray.

The default state for new windows, i.e. whether held or active will be user configurable.

### Templates

Matplotlib provides a [stylesheet][mpl-stylesheets] mechanism that allows predefined styles to be applied to plots. This mechanism will be used to provide users with the ability to save a template of their plot configuration
for future use.

### Utils

This will be a subpackage for the inevitable utility-type code that will be required. One such example is the `mantidqt.utils.qt.py` that will define the shim from which allow PyQt imports are performed.

# Mantid Workbench

A high-level structure of the workbench package is:

```
mantidworkbench
  |-- app
  |   |-- __init__.py
  |   |-- start.py
  |   |-- mainwindow.py
  |   |-- mainmenu.py
  |   |-- splash.py
  |-- config
  |   |-- __init__.py
  |   |-- defaults.py
  |   |-- configdialog.py
  |   |-- plotting.py
  |   |-- firsttimesetup.py
  |-- resources.qrc
  |--__init__.py

```

## app

This subpackage is concerned with the application as a whole such as initialisation, the main window layout, menus etc. It contains the splash screen.

## config

This subpackage will be concerned with configuration. It will be responsible for creating the main tabbed configuration dialog. Any configuration pages must be provided by the packages or widgets that are being configured. For example,
the tabbed scripting interpreter will be a widget and it would be required to provide a widget that could inserted into the main configuration dialog as a complete page. For single widgets this could be done simply by requiring a `CONF_WIDGET` class attribute to point to a widget type to create:

```python
# imports...

class TabbedScriptInterpreter(QWidget):

    CONF_WIDGET = TabbedScriptInterpreterConfig

```

For other items such as plotting configuration the subpackage should provide a `CONF_WIDGET` attribute for the same affect.

This package will also contain the first time setup dialog along with the handling of any default configuration values.


<!-- Links -->
[mvp-fowler]: https://www.martinfowler.com/eaaDev/PassiveScreen.html
[qttest]: http://doc.qt.io/qt-5/qttest-index.html
[jupyter-qtconsole]: https://github.com/jupyter/qtconsole/blob/master/qtconsole/tests/test_console_widget.py
[mantidwidgets]: https://github.com/mantidproject/mantid/tree/master/MantidQt/MantidWidgets
[mslice]: https://github.com/mantidproject/mslice
[hfir_startup_file]: https://github.com/mantidproject/mantid/blob/master/scripts/HFIR_Powder_Diffraction_Reduction.py
[mpl-boilerplate]: https://github.com/matplotlib/matplotlib/blob/master/tools/boilerplate.py
[mpl-stylesheets]: https://matplotlib.org/users/style_sheets.html
