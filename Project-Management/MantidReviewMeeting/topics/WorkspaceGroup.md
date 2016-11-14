# WorkspaceGroup

## WorkspaceGroup in the Workspace Taxonomy

## Using WorkspaceGroups in Algorithms
* Algorithms which accept Workspaces properties which are not groups may in some cases still run with WorkspaceGroups. The result will be the algorithm being executed on each workspace in the group in turn.
* Algorithms which accept WorkspaceGroup do not behave like this. Any operations on the group will be handled internally as defined by the developer of the algorithm.
* Algorithms which accept WorkspaceGroup specifically will not work if a single workspace is passed.

## Interplay with ADS

