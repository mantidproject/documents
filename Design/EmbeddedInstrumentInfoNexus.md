Design for the long term handling of embedding Nexus IDFs
==================================
Design for the long term handling of embedding Instrument Definition Files (IDFs) and instrument Parameter files (param files) in raw Nexus files.

Use cases
----------

There is essential two use cases which are related. 

1. Where wrong information about the instrument and/or instrument parameters gets embedded and this is discovered some time after the raw nexus files have been created and archieved. 
2. Where due to continued improvement of Mantid a user would like to update/modify information embedded in raw Nexus files - for the benefit of Mantid analysis.

The preferred option for 1. is to cure the problem at source, i.e. where this can be done amend the raw nexus files in the archieve to correct for the wrong information. 

For use case 2 above a mechanism needs to be in place to amend/replace/update embedded information in raw nexus file, as is already the case for a collection of ISIS LET runs. 

For information: When IDF not embedded - we already have a solution 
----------

For instruments where we don’t embed IDFs and associated param files we already have a long term solution. This consists of having all IDFs and param files in one directory named ‘instrument’ and where

1. Multiple IDFs for an instrument may exist which are valid based on a valid-from XML attribute.

2. The default parameter file that is loaded with any IDF is done according to the rule: “If you want one parameter file for your IDF file, name your IDF file XXX\_Definition\_Yyy.xml and the parameter file XXX\_Parameters\_Yyy.xml , where Yyy is any combination a characters you find appropriate”, see  http://www.mantidproject.org/InstrumentParameterFile#Naming_and_Using_a_Parameter_File.

IDFs and parameter files for any given instrument can be corrected over time, and made available either as part of future Mantid releases or as part of the soon to be implemented instrument-repository. 


The current situation: when IDF and/or param file is embedded  
----------

Leaving out a few details, the current behaviour when IDF and/or param file information is embedded in a ISIS/SNS raw Nexus file is: 

1. The embedded IDF is loaded and applied 
2. The embedded parameter file, if exist, is loaded and applied
3. In case no parameter file is embedded, the loader will look for the external file XXX\_Parameters.xml 

Focussing on instrument parameters, the current approach will for example fail in the following scenario:

1. For a given instrument, a user have set of raw Nexus files created between two dates and would like to update these with parameters A, and for another set of Nenux files created between two dates the user would like to update these with parameters B


Proposed long term solutions   
----------

The aim here is to come up with a long term way to correct embedded instrument information in raw Nexus files.

Suggestions are listed below. Anyone else, do not hesitate to add any other suggestions.

### Suggestion 1: allow exist parameter files to be date sensitive

I believe this would not work for two reasons. Firstly, some users have multiple parameter files in the instrument folder which may be valid for the same runs, and where the use these dependent on the analysis they conduct or otherwise. Secondly, we already have a transparent mechanism for selected default parameter files to load with different IDFs for the same instrument, e.g. if you have an IDF XXX\_Definition\_something.xml it will by default look for XXX\_Parameters\_something.xml. I can't see how this can work in a transparent way if we in addition allow parameter files to become date sensitive (but maybe I am wrong here?).... Note also, within the same cycle, an instrument scientist may chose to have some runs with and without embedded IDF+param file information, this is e.g. the case on LET where they have been experimenting with embedded IDF information into raw nexus files. 

### Suggestion 2: adding subdirectory to instrument folder 

Create a subdirectory to the ‘instrument’ folder, for example call it, ‘embedded-instrument-corrections’. If this folder contains nothing then is means no correction with be applied to any raw nexus file containing embedded information. If, for example, for instrument XXX, a user would like to update instrument parameter information then the user adds a file XXX\_Parameter\_Corrections.xml (don't hesitate to suggest an alternative name). The content of XXX\_Parameter\_Corrections.xml is:

    <embedded-parameter-corrections name=”XXX”>
       <correction  valid-from=””  valid-to=”” file=”filename” append=’false’/>
    .
    .   
    .
       <correction  valid-from=””  valid-to=”” file=”filename” append=’true’/>
    </ embedded-parameter-corrections>

Suggested behaviour of what will happen during Load is:

1. Embedded IDF is loaded and if exist embedded parameter files is loaded 
2. check if XXX\_Parameter\_Corrections.xml exist, if yes, then check if date of raw Nexus file is between any of the valid-from/valid-to dates. If answer is no, stop here, otherwise continue with step 3
3. The default for append is 'true'. If append='false' run ClearParametersFile
4. Run LoadParametersFile with "filename". 

An alternative to the above is (which is faster where embedded parameter file is large and append='false', otherwise the same speed, but slightly more complex code):

1. Embedded IDF is loaded 
2. check if XXX\_Parameter\_Corrections.xml exist, if yes, then check if date of raw nexus file is between any of the valid-from/valid-to dates. If the answer is no, continue with step 4, otherwise continue with step 3
3.  If append is 'true' load embedded parameter file (if exist) and then run LoadParametersFile with "filename". If append is 'false' run ClearParametersFile and then run LoadParametersFile with "filename"
4.  Load embedded parameter file if exist

Along the same lines we could provide a mechanism for correcting the instrument itself. Hence, a user may add XXX\_IDF\_Corrections.xml:

    <embedded-IDF-corrections name="XXX”>
       <correction  valid-from=””  valid-to=”” file=”filename”/>
    .
    .   
    .
       <correction  valid-from=””  valid-to=”” file=”filename”/>
    </ embedded-IDF-corrections>

Here it is suggested that there is no append attribute. 

Suggested behaviour of what will happen during Load is:

1. check if XXX\_IDF\_Corrections.xml exist, if yes, then check if date of file is between any of the valid-from/valid-to dates. If the answer is no, continue with step 3, otherwise continue with step 2
2.  Load IDF specified with "filename". Stop here, i.e. don't continue with step 3
3.  Load embedded IDF
