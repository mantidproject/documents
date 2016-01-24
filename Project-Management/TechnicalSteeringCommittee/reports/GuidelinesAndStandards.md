Guidelines and standards
========================

Here list currently missing guidelines and standards, which purpose are to  
*	Save time for any developer, who may be new to Mantid and not located within a Mantid team environment, wants to for example
 * add a new instrument to Mantid
 * integrate non-Mantid software with Mantid in some way
 * simply just want to contribute to Mantid
*	Save time for experienced Mantid team members not having to explain the above

Data formats (loaders)
------------
As part of adding a new instrument to Mantid, it may not be the case that an existing data loader can be used, and therefore 
a new data loader needs to be written. 

* No guidelines exist for adding a new loader to Mantid
 * This includes no documentation exists which specifies what information Mantid reads from, for example, ISIS and SNS Nexus files during loading [14561](https://github.com/mantidproject/mantid/issues/14561)

Contributing through Github
---------------------------
The documentation we have for explaining how to get started with Mantid as a new in-house team member has in general been 
found to be good/sufficient (http://www.mantidproject.org/Category:Development ). However, it has been found
that for a person not located within a existing Mantid developer team can finds it a steep learning curve to 
understand how to start contribute to Mantid. So here the non-trivial exercise of adding better guidelines and standards for
this (perhaps learn from other open source frameworks like django).

Fitting
-------
We currently have
*	No documentation, which gives a good overview of the Mantid fitting framework, which includes a description of how this matches onto the directory structure in CurveFitting
 *	Including almost no documentation about the different minimizers we support ([15014](https://github.com/mantidproject/mantid/issues/15014))
* No guidelines for adding advanced fit functions, including fit functions whose parameters are functions of other fitting parameters and fit functions containing explicate dependence on units (like [IkedaCarpenterPV](http://docs.mantidproject.org/nightly/fitfunctions/IkedaCarpenterPV.html))
* No guidelines for how to add a new minimizer and a cost function
* No dedicated guidelines exist for how to best tests new fit functions, minimizers and cost functions, including where this is recommended tests for both for robustness and performance (15078)[https://github.com/mantidproject/mantid/issues/15078]

GUI development and integrate non-Mantid code projects with Mantid
---
Guidelines for how to add a new GUI to Mantid and integrat non-Mantid code projects with Mantid.

We currently have the following documentation on this:
* [GUI Design Guidelines](http://www.mantidproject.org/GUI_Design_Guidelines)
* [Integrate non mantid code projects with mantid](http://www.mantidproject.org/Integrate_non_Mantid_code_projects_with_Mantid)
* [Python GUI Control in Mantidplot](http://www.mantidproject.org/Python_GUI_Control_in_MantidPlot)
* [Create a customized input dialog](http://www.mantidproject.org/Writing_a_CustomDialog)

Perhaps majority of documentation there. Maybe links about could benefit from being grouped together.
