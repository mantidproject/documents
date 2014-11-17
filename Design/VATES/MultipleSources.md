# Handling of Multiple Workspaces in the VSI

### Motivation
The current handling of multiple workspaces can cause several unhandled exceptions.

### Current Issues

##### Several sources with different sets of views
When a workspace is added to the VSI, it creates a new view. 
In addition, several view buttons are enabled or disabled. The view which was added last, determiens the state of  the view buttons. This can lead to a situation where views become available to workspace data which are normally disabled for this type of data.

The following examples might help to illustrate several issues which can occur.

###### Example 1
First we add an MD-Histo workspace in the standard view. This view enables the multi-slice and three-slice button and disables the splatterplot button as well as the standard button.
Then we add an MD-Event workspace (again in standard view). This view enables all buttons, except for the standard button. When we press the splatterplot button, an unhandled exception occurs. Note that this would not have been the case, if we had set the MD-Histo source to invisible.

###### Example 2
As previously, we add an MD-Histo workspace in the standard view. After this, we load an MD-Event workspace into the splatterplot mode. We then select the MD-Histo source which again causes an unhandled exception. Hence loading directly into an incompatible view is not handled.

##### Example 3
As previously, we add an MD-Histo workspace in the standard view. After this, we load an MD-Event workspace into the standard view. We disable the visisibilty of the MD-Histo workspace and switch into splatter mode. Once we make the MD-Histo workspace visible again, an exception occurs.


###Design

#### Approach 1: Restricting views
By keeping track of the visible sources, we can only make those views available which are common to all visible sources.
When the visisbility of a source is changed, ParaView intercepts this via the protected slot 
`handleIndexclicked(const QModelIndex &index_)`. Here we could add additional logic which alters the state of the available views depeding on the nature of the source which was made visible/invisible. If we make a source visible which is not compatible with the current view, then we revert to the view which is "best" for the majority of the sources or the standard view. If we make a source invisible and this "frees" a previously blocked view, then we make this view available.

This approach requires us to replace the pipelineBrowserWidget with a child class that provides a `customHandleIndexclicked(const QModelIndex &index_)` slot that is connected to the `clicked` signal of the pipelineBrowserWidget. The additional logic checks if the visibilty of the source is compatible with the current view and acts accordingly.


#### Approach 2: Automatic disabling the visibilty of sources  
Instead of only making those views available which are common to all visible sources, we can provide all possible views for the set of visible sources. When we switch to a view which is not compatible with a particular visible source, we make this source invisible. When we switch back to the original view, the source is made visible again. If the user decides to enable the visibilty of a source which is not compatible with the current view, we revert to the view which is "best" for the marjority of the visible sources or the standard view.

Similarly as above, we need to replace the pipelineBrowserWidget with a child class that provides a `customHandleIndexClicked(const QModelIndex &index_)` slot.  In addition we need to add logic to the listener of the `clicked` signal of the buttons. This logic will alter the visibilty of the sources which are not compatible with the new view.


######Determining the "best" view
There are two ways to determine the most adequate initial view for a given workspace. 
First, the user has the option of defining a preferred view in the `Mantid.user.properties` file. He can populate the field `vsi.initialview` with either `STANDARD`, `MULTISLICE`, `THREESLICE` or `SPLATTERPLOT`; e.g.: `vsi.initalview = THREESLICE`.

If this view is not compatible with the type of workspace, then the standard view is selected.

In case, there isn't any user-specific setting for the preferred view, we determine the instrument with which the workspace data was measured. If there are several instruments involved, we pick the first instrument from the list. We retrieve the set of techniques for this instrument and select a technique based on a defined hierarchy:

1. `Single Crystal Diffraction` --> `SPLATTERPLOT`
2. `Neutron Diffraction` --> `SPLATTERPLOT`
3. The first technique which contains the string `Spectroscopy`  --> `MULTISLICE`
4. Others --> `STANDARD`

We determine the view which is associated with our selection and make sure that it is compatible with the workspace type. If this is not the case the standard view is selected.

###Feedback