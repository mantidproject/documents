Design for the long term handling of embedding Nexus IDFs
==================================
Design for the long term handling of embedding Instrument Definition Files (IDFs) and instrument Parameter files (param files) in raw Nexus files.


When IDF not embedded 
----------

For instruments where we don’t embed IDFs and associated param files we have a long term solution. This simply consists of having all IDFs and param files in one directory named ‘instrument’ and where

1. Multiple IDFs for an instrument may exist which are valid based on a valid-from XML attribute.

2. and a unique parameter can be associated with any IDF file using the rule: “If you want one parameter file for your IDF file, name your IDF file XXX\_Definition\_Yyy.xml and the parameter file XXX\_Parameters\_Yyy.xml , where Yyy is any combination a characters you find appropriate”, see  http://www.mantidproject.org/InstrumentParameterFile#Naming_and_Using_a_Parameter_File.

This setup means that IDFs and parameter files can be corrected over time, meaning that any future Mantid release containing such corrections will be able to provide a gradual better experience (as more corrected have been included) for the analysis of new and historical data. 

A fact of life is that there will be incorrect IDFs and parameter files for a given Mantid release, this has for example be the frequent cause of path releases.

The discussion here is to come up with a design that provides a mechanism for doing this when IDF and param information is embedded in Nexus files. 

The current situation when IDF embedded  
----------

Leaving out a few details, the current behaviour when IDF and/or param file information is embedded in ISIS/SNS raw Nexus file is: 

1. The embedded IDF is loaded and applied 
2. The embedded parameter file (currently as string copy of a workspace parameter map) is loaded and applied
3. If the instrument name is XXX, then the loader will look for the external file XXX\_Parameters.xml and if exist load it 

This solution cannot handle the case where parameter corrections are needed for an instrument for more than one time period and where corrections are needed for the IDF. 

Also, for the case where the embedded information in the IDF and parameter file is correct the loader should (must) by default not look for an external file. Is there a good reason for keeping the hard-coded lookup of XXX\_Parameters.xml? Unless, something argues otherwise, my preference would be to drop step 3 above. I.e. as soon as we have embedded instrument information in the Nexus file then the loader will not attempt to look for an external file, and, if a known external param file is required then it is applied (with LoadParameterFile) after Load is executed. A temporary backward compatibility step could be to keep step 3 for the case where an IDF is embedded but not a parameter file, although as of writing this I am not a massive fan of this suggestion.

Proposed long term solutions   
----------

The aim here is to come up with a long term way to correct incorrect embedded instrument information in Nexus files.

A suggestion is listed below. Anyone else, do not hesitate to add other suggestions.


### Suggestion 1: adding subdirectory to instrument folder 

Create a subdirectory to the ‘instrument’ folder, for example call it, ‘embedded-instrument-corrections’. For each instrument, say a specific instrument is called XXX, have optionally two files "XXX\_IDF\_Correction.xml" and "XXX\_Param\_Correction.xml". The content of XXX\_IDF\_Correction.xml is something along the lines of:

    <embedded-IDF-correction name=”POLREF”>
       <correction  from-date=””  end-date=”” 
                          with-file=”name of file”/>
    .
    .   
    .
       <correction  from-date=””  end-date=”” 
                          with-file=”name of file”/>
    </ embedded-iIDF-correction>

It simply contains a list of <correction> entries with start and end dates and the what-file (IDF) to use instead of a corrupt embedded IDF file.

The content of XXX_Param_Correction.xml is exactly the same format except for an added attribute ‘append’:

    <embedded-Param-correction name=”POLREF”>
       <correction  from-date=””  end-date=”” 
                          with-file=”name of file” append=’false’/>
    .
    .   
    .
       <correction  from-date=””  end-date=”” 
                          with-file=”name of file” append=’true’/>
    </ embedded-Param-correction>

If ‘append’=’false’ (suggested default) then the what-file is used instead of the embedded parameter map. If ‘append’=’true’ then the embedded parameter is applied, and the what-file is applied afterwards. Where this latter option might be useful is where the embedded parameter map is 99% OK, and potentially very large, but only a few parameter values needs correcting.

The reason for suggestion to have two files: XXX\_IDF\_Correction.xml and XXX\_Param\_Correction.xml is that I imagine that, by far, most of the errors will be for embedded parameter values and not for IDF, and therefore the split will make it faster to look up that this is the case. 
