#Problem
The current tab separated values parsing implementation is ugly, fragile, and awkward to maintain.

```cpp
for (line++; line!=flist.end(); ++line)
{
  QStringList fields = (*line).split("\t");
  if (fields[0] == "geometry") {
    restoreWindowGeometry(app, w, *line);
  } else if (fields[0] == "ColWidth") {
    w->setColumnsWidth(fields[1].toInt());
  } else if (fields[0] == "Formula") {
    w->setFormula(fields[1]);
  } else if (fields[0] == "<formula>") {
    QString formula;
    for (line++; line!=flist.end() && *line != "</formula>"; ++line)
      formula += *line + "\n";
    formula.truncate(formula.length()-1);
    w->setFormula(formula);
  } else if (fields[0] == "TextFormat") {
    if (fields[1] == "f")
      w->setTextFormat('f', fields[2].toInt());
    else
      w->setTextFormat('e', fields[2].toInt());
  } else if (fields[0] == "WindowLabel") { // d_file_version > 71
    w->setWindowLabel(fields[1]);
    w->setCaptionPolicy((MdiSubWindow::CaptionPolicy)fields[2].toInt());
  } else if (fields[0] == "Coordinates") { // d_file_version > 81
    w->setCoordinates(fields[1].toDouble(), fields[2].toDouble(), fields[3].toDouble(), fields[4].toDouble());
  } else if (fields[0] == "ViewType") { // d_file_version > 90
    w->setViewType((Matrix::ViewType)fields[1].toInt());
  } else if (fields[0] == "HeaderViewType") { // d_file_version > 90
    w->setHeaderViewType((Matrix::HeaderViewType)fields[1].toInt());
  } else if (fields[0] == "ColorPolicy"){// d_file_version > 90
    w->setColorMapType((Matrix::ColorMapType)fields[1].toInt());
  } else if (fields[0] == "<ColorMap>"){// d_file_version > 90
    QStringList lst;
    while ( *line != "</ColorMap>" ){
      ++line;
      lst << *line;
    }
    lst.pop_back();
    w->setColorMap(lst);
  } else // <data> or values
    break;
}
```

#Proposed Solution

Simplify reading and writing loading/saving code by writing a helper class to
handle all the parsing of tab-separated-values and sections.

##Loading

This actually implements the same deserialisation logic as in the problem example,
except with better error handling opportunities.

```cpp
TSVSerialiser tsv(lines);

//The most basic use
if(tsv.selectLine("ColWidth"))
  w->setColumnsWidth(tsv.asInt(0));

//Sometimes, you just want to pass the line through to something else.
if(tsv.hasLine("geometry"))
  restoreWindowGeometry(app, w, tsv.lineAsString("geometry"));

//We can also handle missing lines gracefully.
if(tsv.selectLine("Formula"))
{
  w->setFormula(tsv.asString(0));
}
else
{
  //No 'Formula' line found.
  //We can throw an error, warn the user, or pick a value ourself.
}

//This approach has the advantage of clearly showing the order of the
//values and how they're used.
if(tsv.selectLine("TextFormat"))
{
  std::string format;
  int param;

  tsv >> format >> param;

  w->setTextFormat(format, param);
}

//This is the same thing (plus the type cast), but arguably less readable.
if(tsv.selectLine("WindowLabel"))
{
  w->setWindowLabel(tsv.asString(0));
  w->setCaptionPolicy( (MdiSubWindow::CaptionPolicy) tsv.asInt(1) )
}

//With many parameters, using the overloaded '>>' operator becomes much
//more readable compared to the .asType() methods.
if(tsv.selectLine("Coordinates"))
{
  double top_x, top_y, bottom_x, bottom_y;
  tsv >> top_x >> top_y >> bottom_x >> bottom_y;
  w->setCoordinates(top_x, top_y, bottom_x, bottom_y);
}

if(tsv.selectLine("ViewType"))
  w->setViewType( (Matrix::ViewType) tsv.asInt(0) );

if(tsv.selectLine("HeaderViewType"))
  w->setHeaderViewType( (Matrix::HeaderViewType) tsv.asInt(0) );

if(tsv.selectLine("ColorPolicy"))
  w->setColorMapType( (Matrix::ColorMapType) tsv.asInt(0) );

//We can easily handle multiple sections with the same name.
//The string is the complete contents of the <section></section>
//We count occurrences of <section> and </section> so nested <sections>
//are handled correctly. i.e. Are left untouched, as the body of this
//section.
std::vector<std::string> formulae = tsv.sections("formula");
for(auto it = formulae.begin(); it != formulae.end(); ++it)
{
  //Do something with each formula. In this case, we just overwrite the last one.
  w->setFormula( QString( *it ) );

  //In most real-world cases, we'll just be passing it through to
  //another system to interpret for itself.
}
```

##Saving

Saving is far easier than loading, so I won't go into too much detail.

```cpp
TSVSerialiser tsv;

tsv.writeLine("prop1") << val1 << val2 << val3;
//prop1<tab>val1<tab>val2<tab>val3\n
tsv.writeLine("prop2") << val1 << val2;
//prop2<tab>val1<tab>val2\n

//... generate contents of a section, be it through another TSVSerialiser
// or a subsection
tsv.writeSection("sectionName", sectionBody);
//<sectionName>sectionBody</sectionName>
```

##Edge Cases
With the project file format there are some awkward edge cases to the
general format of TSV lines and sections.

###The first three lines of the file do not conform.

These lines do not behave like regular lines or sections in the mantid
project file, and would break parsing.

```
MantidPlot 0.9.5 project file
<scripting-lang>	Python
<windows>	4
```

This can be sidestepped just by treating the first three lines as a
special case, handling them manually and then using TSVSerialiser
on the rest of the file.

###Lines are not guaranteed to have unique names.

For this edge case there are several options, but I've found this seems
to have the best readability:
```cpp
//We're handling the inside of a <graph> section,
//which has multiple 'scale' lines to handle.
for(int i = 0; tsv.selectLine("scale", i); ++i)
{
  //We're now in a for_each loop over the 'scale' lines.
  //Grab all the values from this line (with descriptive variable names)
  double p1, p2, p3, p4, p5;
  tsv >> p1 >> p2 >> p3 >> p4 >> p5;
  //and now do something with them
}

```

##Class Definition

This is the design of the class, as it stands so far.
It's written as pseudocode essentially, and has not been
commented to Mantid's usual coding standards.

```cpp
class TSVSerialiser
{
public:

  //----------------------------------------------------
  //Set up and tear down
  //----------------------------------------------------
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
  void writeSection(std::string name, std::string body);

private:

  //Details omitted...

  //Maps section names to a vector of the contents of sections with that name.
  std::map<std::string,std::vector<std::string> > m_sections;

  //Maps line names to a vector of the lines with that name.
  std::map<std::string,std::vector<std::string> > m_lines;
};

```

##Transitioning

Owing to the TSVSerialiser's handling of sections, the simplest way to refactor the
loading and saving across would be to start from the outside in. Take the outermost layer
of loading/saving code and rewrite it to use TSVSerialiser. The underlying routines to
handle specific sections should see no difference, and would continue functioning as
normal. They could then also be rewritten one by one, allowing a (hopefully) smooth
transition between the legacy code and the new code.

##Potential Improvements

- The handling of the edge case of multiple lines with the same name isn't particularly
  idiomatic C++. A iterator based solution may be preferable.

- Providing two sets of derserialisation methods (>> as well as asType) could cause
  fragmented styles of deserialisation. It may be better to decide on one set to keep
  and discard the other set.

- It still "feels" a little inconsistent somehow. I'm unsure of how this could be
  improved though at this point.
