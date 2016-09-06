## Test Scenarios for Workspace Dock Widget
* **Load button in Workspace Dock**
 1. Load button used to launch load dialog, user selects valid data file and hits Run. Workspace loaded into ADS and the workspace name is added to the workspace dock. ![Load1-1](ScenariosScreenshots/Load1-1.png) ![Load1-2](ScenariosScreenshots/Load1-2.png)
 2. Load button used to launch load dialog, user selects multiple files from the file open dialog and clicks the Run button. A group workspace is created called MultipleFiles which contains the selected workspaces.
 3. Load button used to launch load dialog, user cancels load (Close). No interaction with ADS or workspace dock.
 4. Load button used to launch load dialog, workspace is not set by user. User selects Run. User presented with a dialog which states that one or more invalid properties (filename) have been set.
 5. User runs Load algorithm outside of workspace dock with valid data file. Workspace loaded into ADS and the workspace name is added to the workspace dock.
* **Group Button**
 1. User selects multiple workspaces within the workspace dock and clicks the Group button.  A group workspace called NewGroup is created which contains the selected workspaces. The workspaces are no longer displayed independently of the group.
 2. User selects a workspace group within the workspace dock and clicks the UnGroup button. The workspace group is removed and the individual constituent workspaces are listed in the workspace dock.
 3. User selects a group workspace and a free workspace within the workspace dock and clicks the Group button. A group workspace called NewGroup is created which contains all of the workspaces in the previous group and the free workspace. There are no subgroups. Just one new group. 
* **Sort Button**
 1. User clicks the Sort button, then selects ascending from drop-down menu with name selected. The workspaces in the dock are sorted by name ascending.
 2. User clicks the Sort button, then selects descending from drop-down menu with name selected. The workspaces in the dock are sorted by name descending.
 3. User clicks the Sort button, then selects ascending from drop-down menu with last modified selected. The workspaces in the dock are sorted by last modified ascending.
 4. User clicks the Sort button, then selects descending from drop-down menu with last modified selected. The workspaces in the dock are sorted by last modified descending.
* **Delete Button in Workspace Dock**
 1. User selects works valid workspace in workspace dock and clicks the delete button. The user is presented with a Yes/No confirmation dialog. User selects Yes. Workspace is removed from workspace dock.
 2. User selects works valid workspace in workspace dock and clicks the delete button. The user is presented with a Yes/No confirmation dialog. User selects No. Selected workspace is not deleted from the dock.
 3. User selects multiple workspaces in workspace dock and clicks the delete button. The user is presented with a Yes/No confirmation dialog. User selects Yes. All selected workspaces are removed from the workspace dock.
 4. User selects multiple workspaces in workspace dock and clicks the delete button. The user is presented with a Yes/No confirmation dialog. User selects No. All selected workspaces remain in the workspace dock. 
 5. User selects a workspace which is a member of a workspace group and clicks the delete button. The user is presented with a Yes/No confirmation dialog. User selects Yes. The selected workspace is deleted from the group. The group remains but with one less workspace.
 6. User selects the workspace in a workspace group which only contains one workspace and clicks the delete button. The user is presented with a Yes/No confirmation dialog. User selects Yes. The selected workspace and the parent group are removed from the workspace dock.
 7. User selects a workspace from the workspace tree and an additional workspace which exists within a workspace group and clicks the Delete button. The user is presented with a Yes/No confirmation dialog. User selects Yes. The selected workspace names are removed from the workspace dock.
* **Other Actions**
 1. User right clicks workspace/group in workspace dock and selects Rename. A rename dialog is launched which prompts for the new workspace name. User enters a valid workspace name. The workspace name is updated in the ADS and the workspace dock.
 2. User right clicks workspace/group in workspace dock and selects Rename. A Yes/No confirmation dialog is launched. The user selects Yes. The workspace is removed from the workspace dock and ADS.