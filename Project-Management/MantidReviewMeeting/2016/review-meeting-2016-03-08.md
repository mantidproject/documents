Agenda
=========

* Mantid Roadmap
 * https://docs.google.com/spreadsheets/d/1vjZ-vQpwa4FehvVHEPo8IXFbI8T1JMzfAWQ0xOsUrqM/pubhtml (read only, ask me for an editable link)
 * As a project and a team we will be assessed on how we deliver against the Roadmap
 * Associated tickets have the Roadmap label and should be the first things you work on after a maintenance period
 * If asked to do urgent work by instrument scientists on other tasks then talk to Me/Pete/Jon as we need to record work that deviates from the plan, and assess the impact.

* Workspace Indices, Spectrum Numbers and Detector ID's (Nick)
 * user documentation: http://www.mantidproject.org/MBC_The_Workspace_Matrix
 * There is NO such thing as a Specta index or spectrum index in mantid (although there is ain a nexus file)
 * Mapping functions in MatrixWorkspace https://github.com/mantidproject/mantid/blob/master/Framework/API/inc/MantidAPI/MatrixWorkspace.h#l128

* Error bar plotting changes (Nick)
 * The default for plotting line plots has been changed to include plotting error bars on every data point. https://raw.githubusercontent.com/mantidproject/mantid/2d6075f8eaa7a016b7b7e959298207928df5d5e5/docs/source/images/R37AllErrorBars.png
 * This in general makes more sense than the previous approach of missing some points based on the data density.
 * However it can make dense data plots with errors look more obscured, so if you preferred the old approach you can change it back by unselecting the option Draw All Errors in the View->Prefences menu. https://raw.githubusercontent.com/mantidproject/mantid/2d6075f8eaa7a016b7b7e959298207928df5d5e5/docs/source/images/R37PlotAllErrorsOption.png
  


* Elliptical peak shape cuts in the SliceViewer (Anton)

* Add items you would like to present


Questions to discuss
===========

* Add questions or items you want to discuss here
