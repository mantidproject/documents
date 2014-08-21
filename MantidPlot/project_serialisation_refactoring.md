#Project Serialisation Refactoring

##Current Implementation

###Loading Projects
Loading a project is started with a call to `ApplicationWindow::openProject`. This function opens
the given filename, and begins parsing the file.

`openProject` parses the file in three stages. In the first stage, it reads several lines from the
top of the project file, such as the file version, scripting language used, and number of
windows.

In the second stage it iterates over all of the remaining lines in the file, checking each line in
a large `else if` block. It specifically looks for lines that opens sections, such as `<matrix>` in
which case it will fast-forward until the accompanying `</matrix>` line appears, and call another
method, such as `ApplicationWindow::openMatrix` with the contents. The method it calls will
typically instantiate a matrix window and parse the lines it was given. `<folder>` and `</folder>`
lines are treated specially. `<folder>` lines result in a new folder being created as a child of
the current folder, and the new folder becoming the current folder.  `</folder>` lines set the
current folder to the parent of the current folder.

The third stage is very similar to the second, in that it iterates over the entire project file
again, but this time it only parses plots and graphs, unlike the second stage which only handles
windows, workspaces and matrices.

A call graph would look something like this:
```
ApplicationWindow::openProject(...)
  ApplicationWindow::openMatrix(...)
    Matrix::Matrix(...)
    //Call various setters on Matrix.
  ApplicationWindow::openMatrix(...)
    Matrix::Matrix(...)
    //...
  ApplicationWindow::openNote(...)
    Note::Note(...)
    //...
  ApplicationWindow::openMultiLayer(...)
    MultiLayer::MultiLayer(...)
    //<graph> and <spectrogram> are actually inside <multiLayer>
    //so openGraph and openSpectrogram are called by openMultiLayer.
    ApplicationWindow::openGraph(...)
    //...
    ApplicationWindow::openSpectrogram(...)
    //...
```

###Saving Projects
Project saving is started by calling `ApplicationWindow::saveProject`, which does a little bit of
housekeeping before calling `ApplicationWindow::saveFolder`, which handles the actual saving.

`saveFolder` works by creating an empty string to represent the contents of the project file.
First, any open workspaces or workspace groups are serialised by calling `MantidUI::saveToString`
and appending the result to the project file string. Then if the scripting window is open, it's
serialised by calling `ScriptingWindow::saveToString` and appending the result to the project file
string.

Next `saveFolder` iterates through each folder in the hierarchy, creating the appropriate
`<folder>` and `</folder>` sections, and iterating over every `MdiSubWindow` in that folder and
calling `saveToString` on it, finally appending all this to the project file string.

Next the project file string has some global information prepended to it, such as the version,
the scripting language and how many windows were serialised.

And finally, the project file string is written out to disk.

##Proposal
There are some problems with the current approach: `ApplicationWindow` is simply doing too much.
Different windows should be responsible for serialising themselves, rather than having
`ApplicationWindow` doing almost everything by itself.

To this end, as much of the serialisation and deserialisation logic should be moved from
`ApplicationWindow` to the relevant classes as possible. To this end, a new interface,
`IProjectSerialisable` is created, defining two methods, one for serialisation, and one for
deserialisation.

Instead of iterating over each line of the project file manually, `openProject` should use a helper
class to parse the project file and extract the data. The same helper class could also be used for
serialisation, ensuring consistency.

The design of the helper class, `TSVSerialiser` is described in detail later on in this document.

###Loading Projects

Loading would only consist of two main steps: parsing the project file's header (version, and other
special case lines), and then loading the body.

Using the new helper class, instead of parsing line by line, loading the project file would be
broken down into its individual sections. `openProject` would simply kick off the recursive
function, `ApplicationWindow::openProjectFolder` with the contents of the project's main folder.

`openProjectFolder` then parses the lines it is given, instantiating the new folder as a child of
the current folder, and setting the current folder to be the new folder.

The bulk of `openProjectFolder` consists of checking if a certain type of window has been saved in
that folder, and if it has, instantiating it and then calling the deserialisation method defined by
`IProjectSerialisable`. This way, each window is responsible for deserialising itself, and
`ApplicationWindow` does as little of the work as possible. The idea is for `openProjectFolder` to
behave like a static factory.

However, due to a lot of legacy edge cases, existing windows are not that easy to deserialise. In
such cases, an intermediate function may be required to handle that window, taking care of
instantiating it, doing some preliminary parsing, and then calling the deserialisation method
defined by `IProjectSerialisable`. With additional refactoring work, such cases should all be able
to be removed.

Next, `openProjectFolder` parses and calls each folder it contains itself in turn, forming a
recursive call chain, matching the structure of how the folders are structured within the project.

Finally, `openProjectFolder` sets the current folder to its parent before returning, to traverse
the folder hierarchy correctly.

Long term, the call graph would end up looking something like this:
```
ApplicationWindow::openProject(...)
  ApplicationWindow::openProjectFolder(...)
    //a <matrix> section
    Matrix::Matrix(...)
    Matrix::loadFromProject(...)

    //a <note> section>
    Note::Note(...)
    Note::loadFromProject(...)

    //a <multiLayer section>
    MultiLayer::MultiLayer(...)
    MultiLayer::loadFromProject(...)

    //a subfolder
    ApplicationWindow::openProjectFolder(...)
      //a <matrix> section
      Matrix::Matrix(...)
      Matrix::loadFromProject(...)

      //a subsubfolder
      ApplicationWindow::openProjectFolder(...)
        //...

    //a subfolder
      //a <note> section
      Note::Note(...)
      Note::loadFromProject(...)
```

###Saving Projects

Project saving will be started, as before, by calling `ApplicationWindow::saveProject`. It will do
any housekeeping it needs to before calling a new function, `ApplicationWindow::saveProjectFolder`.
`saveProjectFolder`, like its counterpart, `openProjectFolder` is recursive. It iterates over all
of its `MdiSubWindow`s, finding those that implement `IProjectSerialisable` and calls the
deserialisation function defined by `IProjectSerialisable`. Once it has serialised all of its
windows, it calls `ApplicationWindow::saveProjectFolder` on its child folders, including their
result in its own.

In this way, `ApplicationWindow::saveProject` will build up a string representing the project. It
then only needs to prepend the correct header to the string and write it out to file.

The call graph would look something like this:
```
ApplicationWindow::saveProject(...)
  ApplicationWindow::saveProjectFolder(...)
    Matrix::saveToProject(...)
    Note::saveToProject(...)
    MultiLayer::saveProject(...)
    ApplicationWindow::saveProjectFolder(...)
      Note::saveToProject(...)
      Matrix::saveToProject(...)
```

###Adding new windows to project files

Adding a new window to a project file ought to be relatively straightforward for a developer.

The overall process is as follows:

1. Have your window inherit from the `IProjectSerialisable` interface.
2. Implement `loadFromProject` and `saveToProject`.
3. Add an entry to `ApplicationWindow::openProjectFolder` to handle your window.

It is unnecessary to add an entry to `ApplicationWindow::openProjectFolder` because of how it
functions. It can find your window instance itself, and if implemented, will call your
implementation of `saveToProject`, including the result in the project file for you.

###Serialisation Helper Class

To unify the logic for reading/writing the tab separated values and xml-like sections used in
project files I have created a serialisation helper class called `TSVSerialiser`.

####Loading Example

```cpp
TSVSerialiser tsv(lines);

//The most basic use
if(tsv.selectLine("ColWidth"))
  setColumnsWidth(tsv.asInt(0));

//Sometimes, you just want to pass the line through to something else.
if(tsv.hasLine("geometry"))
  restoreWindowGeometry(app, w, tsv.lineAsString("geometry"));

//We can also handle missing lines gracefully.
if(tsv.selectLine("Formula"))
{
  setFormula(tsv.asString(0));
}
else
{
  //No 'Formula' line found.
  //We can throw an error, warn the user, or pick a value ourselves.
}

//This approach has the advantage of clearly showing the order of the
//values and how they're used.
if(tsv.selectLine("TextFormat"))
{
  std::string format;
  int param;

  tsv >> format >> param;

  setTextFormat(format, param);
}

//Same thing, another way
if(tsv.selectLine("WindowLabel"))
{
  setWindowLabel(tsv.asString(0));
  setCaptionPolicy( (MdiSubWindow::CaptionPolicy) tsv.asInt(1) )
}

//With many parameters, using the overloaded '>>' operator becomes much
//more readable compared to the .asType() methods.
if(tsv.selectLine("Coordinates"))
{
  double top_x, top_y, bottom_x, bottom_y;
  tsv >> top_x >> top_y >> bottom_x >> bottom_y;
  setCoordinates(top_x, top_y, bottom_x, bottom_y);
}

if(tsv.selectLine("ViewType"))
  setViewType( (Matrix::ViewType) tsv.asInt(0) );

if(tsv.selectLine("HeaderViewType"))
  setHeaderViewType( (Matrix::HeaderViewType) tsv.asInt(0) );

if(tsv.selectLine("ColorPolicy"))
  setColorMapType( (Matrix::ColorMapType) tsv.asInt(0) );

//We can handle multiple sections with the same name like this.
//The string is the complete contents of the <section></section>
//We count occurrences of <section> and </section> so nested <sections>
//are handled correctly. i.e. Are left untouched, as the body of this
//section.
std::vector<std::string> formulae = tsv.sections("formula");
for(auto it = formulae.begin(); it != formulae.end(); ++it)
{
  //Do something with each formula. In this case, we just overwrite the last one.
  setFormula( QString( *it ) );

  //In most real-world cases, we'll just be passing it through to
  //another system to interpret for itself.
}
```

####Saving Example

```cpp
TSVSerialiser tsv;

tsv.writeLine("prop1") << val1 << val2 << val3;
//prop1<tab>val1<tab>val2<tab>val3

tsv.writeLine("prop2") << val1 << val2;
//prop2<tab>val1<tab>val2

tsv.writeSection("sectionName", sectionBody);
//<sectionName>
//sectionBody
//</sectionName>

tsv.writeInlineSection("sectionName", sectionBody);
//<sectionName>sectionBody</sectionName>
```

####Class Definition

This is a pseudo-code definition of the TSVSerialiser class.

```cpp
class TSVSerialiser
{
public:

  TSVSerialiser();

  //Constructs and calls the read method.
  TSVSerialiser(std::string lines);

  void read(std::string lines);

  //Returns the serialised lines and sections.
  std::string write()

  //----------------------------------------------------
  //Reading specific lines
  //----------------------------------------------------

  //Returns whether a line with the given name exists.
  bool hasLine(std::string name);

  //Returns the raw line named. Returns an empty string on failure.
  std::string lineAsString(std::string name, int i = 0);

  //Returns a vector of the values found on the named line as strings.
  std::vector<std::string> values(std::string name, int i = 0);

  //----------------------------------------------------
  //Reading sections
  //----------------------------------------------------

  //Sections are the contents of one or more lines between <name> and </name>
  //This counts occurrences of <name> and </name> to handle nesting correctly.
  //A vector of the sections at this depth with the given name is returned.
  std::vector<std::string> sections(std::string name);

  //----------------------------------------------------
  //Reading individual values from a line randomly.
  //----------------------------------------------------

  //Selects the named line for deserialisation.
  //Returns true on success, false if line not found.
  bool selectLine(std::string name, int i = 0);

  //Deserialises the value from the currently selected line at index i.
  //Throws an exception on failure.
  int         asInt(int i);
  double      asDouble(int i);
  std::string asString(int i);

  //----------------------------------------------------
  //Reading multiple values from a line sequentially.
  //----------------------------------------------------

  //Deserialises the next value from the currently selected line.
  TSVSerialiser& operator>>(std::string& val);
  TSVSerialiser& operator>>(double& val);
  TSVSerialiser& operator>>(int& val);

  //----------------------------------------------------
  //Writing values to a line
  //----------------------------------------------------

  //Creates a new line with the given name for serialisation.
  TSVSerialiser& writeLine(std::string name);

  //Serialises the value to the currently selected line.
  //Throws an exception if not in writing mode (i.e. writeLine)
  TSVSerialiser& operator<<(std::string& val);
  TSVSerialiser& operator<<(double& val);
  TSVSerialiser& operator<<(int& val);

  //Create a new section called name, and fill it with body.
  //Inserts newlines before and after the body for you.
  void writeSection(std::string name, std::string body);

  //Create a new section called name, and fill it with body
  //Does not insert newlines before and after the body for you.
  void writeInlineSection(std::string name, std::string body);
};

```
