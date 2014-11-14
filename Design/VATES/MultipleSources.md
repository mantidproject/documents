# Handling of Multiple Workspaces in Vates

### Motivation
The current handling of multiple workspaces can cause several unhandled exceptions.

### Current Issues
When a workspace is added to the VSI, it creates a new view.
In addition, several view buttons are enabled or disabled.
The view which was added last, determines the state of the view buttons.
This can lead to a situation where views become available to workspace data which are normally disabled for this type of data.

The following examples might help to illustrate several issues which can occur.

###### Example 1
First we add an MD-Histo workspace in the standard view. This view enables the multi-slice and three-slice button and disables the splatterplot button as well as the standard button.
Then we add an MD-Event workspace (again in standard view). This view enables all buttons, except for the standard button. We now select the MD-Histo source in the pipeline browser and notice that the splatterplot button is still enabled. When we press the splatterplot button, an unhandled exception occurs.

###### Example 2
As previously, we add an MD-Histo workspace in the standard view. After this, we load an MD-Event workspace into the splatterplot mode. We then select the MD-Histo source which again causes an unhandled exception.


###Design
We attach an event listener to the `sourceChanged` event. Once this is triggered, we determine whether the view is compatible with the new source. If this is the case we reset the buttons according to the new source type (this solves Example 1). If this is not the case, we create a new view which is determined by the "best" initial view for this type of workspace and the instrument type associated with the workspace (this solves Example 2).

For the first example: selecting the MD-Histo workspace causes only the multi-slice and three-slice buttons to be enabled.
For the second example: selecting the MD-Histo workspace causes the view to revert back to the standard view. 

######Determining the "best" view
There are two ways to determine the most adequate initial view for a given workspace. 
First, the user has the option of defining a preferred view in the `Mantid.user.properties` file. He can populate the field `vates.intialview` with either `STANDARD`, `MULTISLICE`, `THREESLICE` or `SPLATTERPLOT`; e.g.: `vates.initalview = THREESLICE`.

If this view is not compatible with the type of workspace, then the standard view is selected.

In case, there isn't any user-specific setting for the preferred view, we determine the instrument with which the workspace data was measured. If there are several instruments involved, we pick the first instrument from the list. We retrieve the set of techniques for this instrument and select a technique based on a defined hierarchy:

1. `Single Crystal Diffraction` --> `SPLATTERPLOT`
2. `Neutron Diffraction` --> `SPLATTERPLOT`
3. The first technique which contains the string `Spectroscopy`  --> `MULTISLICE`
4. Others --> `STANDARD`

We determine the view which is associated with our selection and make sure that it is compatible with the workspace type. If this is not the case the standard view is selected.

###Feedback