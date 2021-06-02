import mantid.simpleapi as mantid


def create_named_workspace(name):
    ws1 = CreateWorkspace([1, 2, 3, 4, 5], [10, 10, 10, 10, 10], [1, 1, 1, 1, 1])
    RenameWorkspace(ws1, name)
    return ws1


def create_named_group_with_named_workspaces(group_name, workspace_name_list):
    for name in workspace_name_list:
        create_named_workspace(name)

    group = GroupWorkspaces(workspace_name_list)
    RenameWorkspace(group, group_name)
    return group


def group_workspace_groups(name, workspaces):
    tmp = mantid.CreateSampleWorkspace()
    overall = mantid.GroupWorkspaces(tmp, OutputWorkspace=str(name))
    for workspace in workspaces:
        overall.add(workspace)
    mantid.AnalysisDataService.remove("tmp")


# ----------------------------------------------------------------------------------------------------------------------
# INDIVIDUAL FITS
# ----------------------------------------------------------------------------------------------------------------------

create_named_group_with_named_workspaces("Individual Fit: EMU0001234",
                                         ["Fit EMU0001234 Parameters; Pair Asym; long; Period; 1; #1",
                                          "Fit EMU0001234 Workspace; Pair Asym; long; Period; 1; #1",
                                          "Fit EMU0001234 Covariance; Pair Asym; long; Period; 1; #1"])

create_named_group_with_named_workspaces("Individual Fit: EMU0001234; Period 2",
                                         ["Fit EMU0001234 Parameters; Pair Asym; long; Period; 2; #1",
                                          "Fit EMU0001234 Workspace; Pair Asym; long; Period; 2; #1",
                                          "Fit EMU0001234 Covariance; Pair Asym; long; Period; 2; #1"])

create_named_group_with_named_workspaces("Individual Fit: EMU0001235",
                                         ["Fit EMU0001235 Parameters; Pair Asym; long; Period; 1; #1",
                                          "Fit EMU0001235 Workspace; Pair Asym; long; Period; 1; #1",
                                          "Fit EMU0001235 Covariance; Pair Asym; long; Period; 1; #1"])

group_workspace_groups("Muon Individual Fits", ["Individual Fit: EMU0001234", "Individual Fit: EMU0001234; Period 2",
                                                "Individual Fit: EMU0001235"])

# ----------------------------------------------------------------------------------------------------------------------
# SIMULTANEOUS FITS
# ----------------------------------------------------------------------------------------------------------------------

create_named_group_with_named_workspaces("Simultaneous Fit: UserLabel1",
                                         ["SimFit Parameters; Pair Asym; long; Period; 1; #1 UserLabel1",
                                          "SimFit Workspace; Pair Asym; long; Period; 1; #1 UserLabel1",
                                          "SimFit Covariance; Pair Asym; long; Period; 1; #1 UserLabel1"])

create_named_group_with_named_workspaces("Simultaneous Fit: UserLabel2",
                                         ["SimFit Parameters; Pair Asym; long; Period; 1; #1 UserLabel2",
                                          "SimFit Workspace; Pair Asym; long; Period; 1; #1 UserLabel2",
                                          "SimFit Covariance; Pair Asym; long; Period; 1; #1 UserLabel2"])

group_workspace_groups("Muon Simultaneous Fits", ["Simultaneous Fit: UserLabel1", "Simultaneous Fit: UserLabel2"])

# ----------------------------------------------------------------------------------------------------------------------
# SEQUENTIAL FITS
# ----------------------------------------------------------------------------------------------------------------------

create_named_group_with_named_workspaces("SeqFit EMU0001234 UserLabel1",
                                         ["SeqFit Parameters; Pair Asym; long; Period; 1; #1 UserLabel1",
                                          "SeqFit Workspace; Pair Asym; long; Period; 1; #1 UserLabel1",
                                          "SeqFit Covariance; Pair Asym; long; Period; 1; #1 UserLabel1"])

create_named_group_with_named_workspaces("SeqFit EMU0001235 UserLabel1",
                                         ["SeqFit Parameters; Pair Asym; long; Period; 1; #1 UserLabel1",
                                          "SeqFit Workspace; Pair Asym; long; Period; 1; #1 UserLabel1",
                                          "SeqFit Covariance; Pair Asym; long; Period; 1; #1 UserLabel1"])

group_workspace_groups("Sequential Fit: UserLabel1", ["SeqFit EMU0001234 UserLabel1", "SeqFit EMU0001235 UserLabel1"])

create_named_group_with_named_workspaces("SeqFit EMU0001234 UserLabel2",
                                         ["SeqFit Parameters; Pair Asym; long; Period; 1; #1 UserLabel2",
                                          "SeqFit Workspace; Pair Asym; long; Period; 1; #1 UserLabel2",
                                          "SeqFit Covariance; Pair Asym; long; Period; 1; #1 UserLabel2"])

create_named_group_with_named_workspaces("SeqFit EMU0001235 UserLabel2",
                                         ["SeqFit Parameters; Pair Asym; long; Period; 1; #1 UserLabel2",
                                          "SeqFit Workspace; Pair Asym; long; Period; 1; #1 UserLabel2",
                                          "SeqFit Covariance; Pair Asym; long; Period; 1; #1 UserLabel2"])

group_workspace_groups("Sequential Fit: UserLabel2", ["SeqFit EMU0001234 UserLabel2", "SeqFit EMU0001235 UserLabel2"])

group_workspace_groups("Muon Sequential Fits", ["Sequential Fit: UserLabel1", "Sequential Fit: UserLabel2"])
