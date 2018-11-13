
Project Saving for Mantid Workbench
==============================
Motivation
--------------
In MantidPlot it was possible to save all currently open windows and all workspaces, and then be able to load then back in the exact(-ish) state that they were in previously. To achieve this goal again in Mantid Workbench, the problem will be split into two where window serialization and saving and therefore reopening will be separate in implementation, from saving workspaces.

The reason for the split is so that it can be handled in a more abstract manor. Instead of thinking of the task as one great big issue it can be split into the two smaller problems and then split further from there, later on in design.

This document exists because Project Saving is a non-trivial challenge to tackle when it comes to ideas with saving and loading interfaces created in both Python and C++ as well as saving and loading of workspaces. This issue should be fairly simple to understand, simply users should be able to save their projects and load them back in, to at least the standard that MantidPlot was able to achieve.

Changes to MantidWorkbench needed
-----------------------------------------------
- MainWindow should track all of the open windows (as well as if they are serializable or not) similar to MantidPlot
- File->Save Project needs to be added
- File->Load Project needs to be added
- A GUI for picking where to Save

Options for Implementation of Workspace Saving
--------------------------------------------------------
**Python:**
- Pickling
	- Pros: Built in library of Python
	- Cons: Need to add _ _ getstate_ _ and _ _ setstate_ _ functions to every UI class which must return a pickle-able type (dict, list, int, string etc). Then setstate function. Unconfirmed if possible or not.
- JSON Encoding
	- Pros: Built in library of Python, "faster" than Pickling: https://www.benfrederickson.com/dont-pickle-your-data/, Potential to be integrated with C++ as it's universal
	- Cons: Needs methods in every class

**C++**
- Serialization with boost 
	- Pros: We already have it, simple, uses an archive type for template serialization, has forward compatibility when classes change.
	- Cons: We need to give Friend access to each UI class for the boost::serialize::access, not python.
- Serialization with cereal
	- Pros: Very easy to implement using a template of Archive type.
	- Cons: We don't already have the cereal library, plus we'd need to cite it, as per licensing, not python.

**Both C++ and Python**
- Our own method of serialization utilizing a JSON back-end
	- Pros: We can pass C++ values to Python based serializer and back to C++, we can determine file format, we can write custom conversions for types (Most Qt types have a QVariant type conversion to JSON anyway), highly flexible
	- Cons: Requires extra work to implement that a already available library 


Implementation of save window, the recommended Method
-------------------------------------------------------------------------
Utilizing the serializing method with a JSON back-end, will likely be best as not only will it use a standard file type, it should be easy to change the file type by changing a few functions inside the serializer. Each UI that is serializable should have an X and Y function where X would create a Dictionary with a string as the key and the value set to whatever object you would need to save. Y would use the string key to get back X's value and emplace the original value again, and update the GUI to represent these values.

An Example X:
```python
def X(self):  
    return_list = {}  
    return_list["name"] = "TestUI"  
    return_list["spinBox"] = self.ui.spinBox.value()  
    return_list["lineEdit"] = self.ui.lineEdit.text()  
    return_list["dateEdit"] = self.ui.dateEdit.text()  
    return_list["radioButton"] = self.ui.radioButton.isChecked()      
    return_list["checkBox"] = self.ui.checkBox.isChecked()  
    return_list["label_7Visible"] = self.ui.label_7.isVisible()  
    return return_list
```
An Example Y:
```python
def Y(self, dict):  
    self.ui.spinBox.setValue(dict["spinBox"]) 
    self.ui.lineEdit.setValue(dict["lineEdit"]) 
    self.ui.dateEdit.setValue(dict["dateEdit"]) 
    self.ui.radioButton.setValue(dict["radioButton"]) 
    self.ui.checkBox.setValue(dict["checkBox"])
    self.ui.label_7.setVisible(dict["label_7Visible"])
```
One problem is how the Python JSON module will represent these QStrings, QStringList and other types that are necessary to save. Inside Qt and PyQt there is a type called QVariant which allows for constructions from the majority of Qt types and normal types, which then allows you to convert them to many formats including string and QJsonArray.

However the usage of QVariant is not necessary as long as you are mostly requiring QString, bool, and int, as it will just be converted to a string by the dictionary creation. Then the JSON module will be able to convert the dictionary into a JSON string.

A basic example of how a line of JSON that may be generated from an object that uses the X function's output, the output is passed as the variable dict. Using indent=4 makes it a more human readable form when actually written out than with no indent as it would be on a single line:
```python
def json_line_from_dict(dict):  
    import json  
    return json.dumps(dict, indent=4) 
 ```

One potential implementation is to force usage of serialization for current and new GUIs, create a class which inherits from QWidget/QMainWindow (depending on how PyQt/Mantid Workbench implements a window), which includes a basic copy of X and Y from which windows must inherit/must implement the methods of X and Y. That was a simple list of windows can be held by the main application and a call to X and Y made on them, for saving and loading respectively. This implementation will allow for not only other methods to be forced upon GUI designers that may be required but will also guarantee there is a method for project saving.

For the implementation of X and Y, we need to have a copy of the variables that needs to be serialized on the GUI, so for example if a value needs to be serialized then save it just grab the value and load it back in, in the methods, X and Y.

Options for Implementation of Workspace Saving
--------------------------------------------------------
**Python and C++**
- Use save algorithms on all of the workspaces
	- Pros: We can optimize WorkspaceGroup/Multi-period workspaces like in MantidPlot, Can save only given workspaces, Uses already in place features, have a good idea of what to do from previous MantidPlot implementation.
	- Cons: Can be slower than other implementations

**C++ Only**
- Use boost::serialize or cereal libraries
	- Pros: Faster than old implementation, already made libraries that should be well maintained
	- Cons: Sizeable extra code added to already bloated Workspace and requires more coding effort than calling SaveNexus.

Implementation of save workspaces, the recommended Method
------------------------------------------------------------------------------
Utilizing the already implemented SaveNexusProcessed and SaveMD algorithms, the suggestion is to implement a python version of how MantidPlot currently implements saving workspaces. This seems like a better option than utilizing the libraries because they are only really available to C++, whilst feasible it makes more sense to move to python/cross language support which is similar to how MantidPlot implements it already.

Call SaveNexusProcessed for most workspaces and SaveMD for EventWorkspaces. Saving a copy of the names of the saved workspace .nxs files in a JSON format in the same file as the output from the serialization of the windows, it may look like this:
```JSON
{
	workspacenames : ["workspace1", "workspace2", "workspace3", "workspace4"]
}
```
The way this will work alongside the Serialization is that it will all be saved in the same folder, this is the same as the previous implementation (in MantidPlot), for saving and loading workspaces. However a key differences are that this will be produced in Python as that is what Workbench has been produced in, and the output folder will consist of .nxs workspaces and a .json file with the details of the windows.

A workspace should only save over an already saved version of that workspace if it has changed since last save. This can be done by checking the last modified of any files with the same name as a workspace's name and then comparing it to that workspace's history for it's most recent entry.

Diagram to display functionality
----------------------------------------
Saving starts from the GUI, and from there it passes on the selected options to the Project Saver which will in turn delegate tasks to saving workspaces and windows. The output of workspace saver and window saver are both put into the output folder.
![Project Flow](file:project-saveflow.png)

