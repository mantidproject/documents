Python : Model View Presenter (MVP) Pattern
============================================

Reasons for using MVP :

- Readability.
- Separation of concerns.
- Future modifications.
- Unit testing (mocking).

Simple Implementation
---------------------

We will now outline a "minimal example" of how to implement MVP in python. It is generally considered good practice to split files up to each contain a single class; in this case since MVP is implemented as classes we will have three files for the MVP; `dummyWidget_model.py`, `dummyWidget_presenter.py` and `dummyWidget_view.py`. We will also have a file for the widget `dummyWidget.py`, but this is optional. Lastly we will need `main.py` which runs the application.

Let's begin with the model, which is responsible for doing the processing of the data (in other words it contains the underlying *logic* to the interface). It should know nothing about the view or presenter and should not know about `PyQt`. Below is the implementation of `dummyWidget_model.py`

```Python
from __future__ import (absolute_import, division, print_function)

class LogTableModel(object):

    def __init__(self):
        self.someVariable = 5

    def doSomething(self):
        return 1
```

Next, we will implement the *view*. The view is responsible for setting the layout of the GUI, it should know nothing about the model and contain as little logic as possible. It necessarily includes a lot of `PyQt`. Below is the implementation of `dummyWidget_view.py`;

```Python
from __future__ import (absolute_import, division, print_function)

from PyQt4 import QtCore
from PyQt4 import QtGui


class LogTableView(QtGui.QWidget):
    buttonSignal = QtCore.pyqtSignal(object)

    def __init__(self, name, parent=None):
        super(LogTableView, self).__init__(parent)
        self.grid = QtGui.QGridLayout(self)
        self.message = name
        btn = QtGui.QPushButton(name, self)
        self.grid.addWidget(btn)
        btn.clicked.connect(self.buttonClick)

    def buttonClick(self):
        self.buttonSignal.emit(self.message)
```

The `__init__` method is responsible for setting up the layout. In this case we are simply adding a push button with text which is supplied to the class constructor. For such simple layouts, this makes sense, but for more complicated interfaces (in terms of number of objects) it is better to work directly with the `.ui` files produced by Qt Designer, and have separate layout class which feeds into the view.

There is a single connect statement which is this case gives us more control on the signal which is emitted from the button click (by sending out `message`). The view inherits from `QWidget`.

Next we will establish the communication between the view and model using the *presenter* class. Concretely, this means establishing the signal/slot relationships between signals emitted from the view and slots within the model. For this to happen the presenter must know about the view and model, and so must take these in its constructor. Ideally the presenter should not have any Qt references (as it is not necessary to).

 Below is the implementation of `dummyWidget_presenter.py`;

 ```Python
class LogTablePresenter(object):

    def __init__(self, view, model):
        self.view = view
        self.model = model

    @property
    def widget(self):
        return self.view
 ```

This minimal example simply stores the view and model, and defines a property `widget` which returns the view. We have not actually added any communication between the model/view explicitly. Now, we wish to bundle the MVP implementation up into a widget, so that the main window can just set this widget without knowing about the guts of the code. Below is the implementation of `dummyWidget.py`;

```Python
from LogTable_view import LogTableView
from LogTable_presenter import LogTablePresenter
from LogTable_model import LogTableModel


class DummyWidget(object):
    """
    """
    def __init__(self, name, parent=None):
        view = LogTableView(name, parent)
        model = LogTableModel()
        self._presenter = LogTablePresenter(view, None)

    @property
    def presenter(self):
        return self._presenter

    @property
    def widget(self):
        return self.presenter.widget
```

First we create the view and model, then we create the presenter (since it requires us to supply the model and view). We define some properties to allow neat access to the view and presenter from calling code. 

That's it, now the widget `DummyWidget` can be placed into a GUI just like any other widget (e.g. push button). To see how we can do that with a minimal example we write the `main.py` file

```Python
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys

from LogTableWidget import DummyWidget

class DummyGUI(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(DummyGUI, self).__init__(parent)

        dummyWidget = DummyWidget("load dummy", self)
        poopWidget = QtGui.QPushButton("Poop", self)

        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(dummyWidget.widget)
        splitter.addWidget(poopWidget)

        self.setCentralWidget(splitter)
        self.setWindowTitle("DummyGUI")


def qapp():
    if QtGui.QApplication.instance():
        _app = QtGui.QApplication.instance()
    else:
        _app = QtGui.QApplication(sys.argv)
    return _app


if __name__ == "__main__":
    app = qapp()
    try:
        ex = DummyGUI()
        #ex.resize(700, 700)
        ex.show()
        app.exec_()
    except RuntimeError as error:
        ex = QtGui.QWidget()
        QtGui.QMessageBox.warning(ex, "Error", str(error))
```

This is a simple main window, which includes our widget, alongside another widget.

More involved example
=====================

Below is the code from the demonstration given in the concept discussion

```Python
from qtpy import QtWidgets, QtGui


class View(QtWidgets.QWidget):

  def __init__(self):
      super(View, self).__init__()

      self.setupUI()

  def setupUI(self):
      layout = QtWidgets.QVBoxLayout()

      self.edit1 = QtWidgets.QLineEdit()
      self.edit2 = QtWidgets.QLineEdit()
      self.edit3 = QtWidgets.QLineEdit()

      self.label = QtWidgets.QLabel("=")

      self.button = QtWidgets.QPushButton()
      self.button.setText("Button")

      layout.addWidget(self.edit1)
      layout.addWidget(QtWidgets.QLabel("+"))
      layout.addWidget(self.edit2)
      layout.addWidget(self.label)
      layout.addWidget(self.edit3)
      layout.addWidget(self.button)
      self.setLayout(layout)

  def get_first_number(self):
      return int(self.edit1.text())

  def get_second_number(self):
      return int(self.edit2.text())

  def set_result(self, result):
      self.edit3.setText(str(result))

  def on_button_clicked(self, slot):
      self.button.clicked.connect(slot)


class Presenter:

  def __init__(self, model, view):
      self.model = model
      self.view = view

      self.view.on_button_clicked(self.handle_button_clicked)

  def show(self):
      self.view.show()

  def handle_button_clicked(self):
      n1 = self.view.get_first_number()
      n2 = self.view.get_second_number()
      result = self.model.add(n1, n2)
      self.view.set_result(result)


class Model:

  def __init__(self):
      pass

  def add(self, n1, n2):
      return n1 + n2


class ParentView(QtWidgets.QWidget):

  def __init__(self, add_widget_view):
      super(ParentView, self).__init__()

      layout = QtWidgets.QVBoxLayout()

      self.addWidget = add_widget_view

      self.selection = QtWidgets.QComboBox()
      self.selection.addItem("Add")

      layout.addWidget(self.addWidget)
      layout.addWidget(self.selection)
      self.setLayout(layout)

  def set_add_widget(self, widget):
      self.addWidget = widget

class ParentPresenter:

  def __init__(self , view, adder):
      self.view = view
      self.adder = adder

  def show(self):
      self.view.show()


if __name__ == "__main__":
  app = QtWidgets.QApplication([])

  view = View()
  parent_view = ParentView(view)
  adder = Presenter(Model(), view)
  window = ParentPresenter(parent_view, adder)
  window.show()
  app.exec_()
  ```