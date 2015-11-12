Guidelines and standards
========================

Here list non existing guidelines and standards which 
*	Save time for any new developer wanting to use Mantid 
*	Save time for the Mantid team by not having to explain the above
*	Save time for existing Mantid team developer 

Fitting
-------
We have user documentation for how to

* add a new fitting function with Python see http://www.mantidproject.org/Introduction_to_Python_Fit_Functions 
* new fitting functions with C++ 
* basic information about how initial starting values for fitting parameters can be set using instrument parameters (http://www.mantidproject.org/MBC_Intelligent_Fitting ). 

What we currently don’t have includes
*	No documentation for how to add new minimizers or cost functions
*	No documentation which gives a good overview of the fitting framework in Mantid including how we make use of GSL, and description of how this match onto the directory structure in https://github.com/mantidproject/mantid/tree/master/Framework/CurveFitting  
*	No documentation for adding more advanced fitting functions where some fitting parameters are functions of other fitting parameters or where fitting functions makes use of geometric information like http://docs.mantidproject.org/nightly/fitfunctions/IkedaCarpenterPV.html 
*	Limitted documentation for how to best tests for new fitting, minimizer or cost functions to mantid, where a developer may want to add both performance test, unit tests, and more systemwide test to test robustness of fitting in general and against different compilers
*	No documentation for how to add MD fitting functions

GUI
---
A developer may want to use to expose the Mantid framework through an existing interface, or the reserve expose an existing framework through Mantid.

We currently have
* [GUI Design Guidelines](http://www.mantidproject.org/GUI_Design_Guidelines)
* [Python GUI Control in Mantidplot](http://www.mantidproject.org/Python_GUI_Control_in_MantidPlot)

Related to this is [Integrate non mantid code with mantid](http://www.mantidproject.org/Integrate_non_Mantid_code_with_Mantid).

Maybe this item is better done by adding a new training course, which a title like "How to add a new GUI to Mantid".

Data formats
------------
As part of adapting a new instrument in Mantid it may not be the case that an existing data loader can be used and therefore 
a new data loader needs to be written. No documentation exists for this. This documentation also needs to demonstrate how 
information in the data can be tied to externally specified geometry information about the instrument, i.e. an IDF+instrument 
parameter file in the instrument folder. 

Also demonstrate an example where geometry information is already embedded in the data and how both data and instrument info 
can be read (for example see the LoadMcStas loader). 

Related, no documentation exists which specifies exactly what information Mantid is read from ISIS and SNS Nexus files doing loading. 
Here, it will make sense that this documentation becomes part of the .rst file for the relevant loader. 

Contributing through Github
---------------------------
The documentation we have for explaining how to get started with Mantid as a new in-house team member has in general been 
found to be good/sufficient (http://www.mantidproject.org/Category:Development ). However, it has been found
that for a person not located within a existing Mantid developer team can finds it a steep learning code to 
understand how to start contribute to Mantid. So here not non-trivial exercise of adding better guidelines and standards for
this (perhaps learn from other open source frameworks like django).
