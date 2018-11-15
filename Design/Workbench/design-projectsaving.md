
Project Saving for Mantid Workbench
==============================
Motivation
----------
In MantidPlot it was possible to save all currently open windows and all workspaces, and then be able to load then back in the exact(-ish) state that they were in previously. To achieve this goal again in Mantid Workbench, the problem will be split into two where window serialization and saving and therefore reopening will be separate in implementation, from saving workspaces.

The reason for the split is so that it can be handled in a more abstract manor. Instead of thinking of the task as one great big issue it can be split into the two smaller problems and then split further from there, later on in design.

This document exists because Project Saving is a non-trivial challenge to tackle when it comes to ideas with saving and loading interfaces created in both Python and C++ as well as saving and loading of workspaces. This issue should be fairly simple to understand, simply users should be able to save their projects and load them back in, to at least the standard that MantidPlot was able to achieve.

It should as a requirement allow people to share projects across platforms and seamlessly by zipping and emailing or transferring by different methods. This however should not come in the way of pure functionality.

The Saver/Serializer should take from interfaces it's dictionary from the output and if possible turn it into JSON and then also be able to transfer it back in the exact same form it was recieved when loading the data back in, the rest should be handled by indidual developers implementing and maintaining interfaces. This has the added benefit of allowing someone in the future to rip out the JSON parts and replace it with whatever saver they would like to use.

Changes to MantidWorkbench needed
---------------------------------
- MainWindow should track all of the open windows (as well as if they are serializable or not) similar to MantidPlot
- File->Save Project needs to be added
- File->Load Project needs to be added
- A GUI for picking where to Save

GUI and integration initial ideas
---------------------------------
It is true that this document is mostly focused on the actual implementation of saving the project and they intricacies of how that would work. However, it is important that this is discussed to some extent before hand. The intial thought process is that you would be able to do both a basic SaveAll and Save Advanced. SaveAll will run through a pretty simple Save everything as long as it's not overwriting workspaces. Save Advanced would allow the users to Select workspaces and windows individually, also adding an option as to whether or not they want to overwrite the workspaces that may or may be saved which is so at worst case users can save everything from scratch.

Options for Implementation of Workspace Saving
----------------------------------------------
**Python:**
- Pickling
	- Pros: Built in library of Python
	- Cons: Need to add _ _ getstate_ _ and _ _ setstate_ _ functions to every UI class which must return a pickle-able type (dict, list, int, string etc). Then setstate function. Unconfirmed if possible or not.
- JSON Encoding
	- Pros: Built in library of Python, "faster" than Pickling: https://www.benfrederickson.com/dont-pickle-your-data/, Potential to be integrated with C++ as it's universal
	- Cons: Needs methods in every class, doesn't integrate fully with C++ (It won't translate a C++ class into a JSON file/string without an extra library)

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
-----------------------------------------------------
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

The current plan is to integrate JSON into the serializer and so it would be helpful to talk about custom objects/types. It should be easy enough to write a custom encoder. A custom encoder should be as easy as taking inheriting from json.JSONEncoder on a class and defining default(self, obj). For example [1]:
```python
class ObjectEncoder(json.JSONEncoder):
  def default(self, object):
    if isinstance(object, object_type):
      # Return an already serializable type e.g.
      return str(object_type)
    return json.JSONEncoder.default(self,object)
```

Then this leaves Decoding from JSON to be tackled, a custom decoder is a little harder as it relies on the key name when decoding being something unique to that type so would need to be on a type requirement by requirement basis. So in the JSON a programmer would need to add a _object_type_ or some other unique string to show that a type like that is there, but it's really on a per type basis. For example [1]: 
```python
def object_type(dict):
  # __object_type__ being a key that is unique to that type
  if "__object_type__" in dict:
    # Return an object of the original object type
    return object(dict["object_part1"], dict["object_part2"], dict["object_part3"])
  return dict
```

Similarly with the C++ section of window serialization it would return a boost::python::dict so that it interacts well and will transition well into the python method. An example of how this may interact and look like is:
```C++
boost::python::dict X(){
  boost::python::dict return_list;
  return_list["name"] = "TestUI"; 
  return_list["spinBox"] = ui->spinBox.value()  
  return_list["lineEdit"] = ui->lineEdit.text()  
  return_list["dateEdit"] = ui->dateEdit.text()  
  return_list["radioButton"] = ui->radioButton.isChecked()      
  return_list["checkBox"] = ui->checkBox.isChecked()  
  return_list["label_7Visible"] = ui->label_7.isVisible()  
  return return_list;
}

void Y(boost::python::dict dict){
  ui->spinBox.setValue(dict["spinBox"]) 
  ui->lineEdit.setValue(dict["lineEdit"]) 
  ui->dateEdit.setValue(dict["dateEdit"]) 
  ui->radioButton.setValue(dict["radioButton"]) 
  ui->checkBox.setValue(dict["checkBox"])
  ui->label_7.setVisible(dict["label_7Visible"])
}
```
The nice thing about utilising the boost::python::dict object to transfer from the C++ code to the Python code is that it will translate very easier than say a std::map. This can all be handled by boost::python similarly to how interface objects and other things originally wrote in C++ are being integrated with the new workbench. Overall the actual JSON back-end/writer will be on the Python side of the code so this is nessercary.

Options for Implementation of Workspace Saving
----------------------------------------------
**Python and C++**
- Use save algorithms on all of the workspaces
	- Pros: We can optimize WorkspaceGroup/Multi-period workspaces like in MantidPlot, Can save only given workspaces, Uses already in place features, have a good idea of what to do from previous MantidPlot implementation.
	- Cons: Can be slower than other implementations

**C++ Only**
- Use boost::serialize or cereal libraries
	- Pros: Faster than old implementation, already made libraries that should be well maintained
	- Cons: Sizeable extra code added to already bloated Workspace and requires more coding effort than calling SaveNexus.

Implementation of save workspaces, the recommended Method
---------------------------------------------------------
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
--------------------------------
Saving starts from the GUI, and from there it passes on the selected options to the Project Saver which will in turn delegate tasks to saving workspaces and windows. The output of workspace saver and window saver are both put into the output folder.
![Project Flow](Design/Workbench/project-saveflow.png)

<!---
The Sequence Diagram in the Encoder Sequence below

Title: Sequence of Saving
Workbench->ProjectSaver: Save these
ProjectSaver->MantidQtModule: Get list of interfaces
MantidQtModule->ProjectSaver: List of interfaces
ProjectSaver->EncoderFactory: Get Encoder for interface X
EncoderFactory->ProjectSaver: Encoder for interface X
ProjectSaver->InterfaceXEncoder: Encode interface X
InterfaceXEncoder->InterfaceXAttributes: Get Interface X tags
InterfaceXAttributes->InterfaceXEncoder: List of tags
InterfaceXEncoder->ProjectSaver: Encoded Key value pair
ProjectSaver->ProjectWriter: Write out these encoded key value pairs
ProjecyWriter->ProjectSaver: Done
ProjectSaver->Workbench: Done
-->

To illustrate the Encoder interactions I have produced this rather basic Sequence diagram to attempt to emphasise how the program should produce saved files.
![Encoder Seqeunce](Design/Workbench/projectsave-encoder.svg)

<!--
Title: Decoder Sequence Diagram
Workbench->ProjectLoader: Load this file
ProjectLoader->ProjectReader: Get the key value pairs back from this file
ProjectReader->ProjectLoader: Key value pairs
ProjectLoader->DecoderFactory: Get Decoder for Interface X
DecoderFactory->InterfaceXDecoder: Check if possible to decode this interface
InterfaceXDecoder->DecoderFactory: True
DecoderFactory->ProjectLoader: InterfaceXDecoder
ProjectLoader->InterfaceXDecoder: Recreate the InterfaceX object
InterfaceXDecoder->MantidQt: Create InterfaceX
MantidQt->InterfaceXDecoder: Alias to interface
InterfaceXDecoder->ProjectLoader: Done
ProjectLoader->Workbench: Done
-->

To illustrate the Decoder intractions I have produced this rather basic Sequence diagram to attempt to emphasise how the program should utilise saved files.
![Decode Sequence](Design/Workbench/projectsave-decoder.svg)

Bibliography
------------

[1] Docs.python.org. (2018). json — JSON encoder and decoder — Python 3.7.1 documentation. [online] Available at: https://docs.python.org/3/library/json.html [Accessed 14 Nov. 2018].

