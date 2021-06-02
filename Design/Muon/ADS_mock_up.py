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


MuonAnalysisTFNormalizations = CreateWorkspace([1], [2], [3])

##################################################################################################

create_named_group_with_named_workspaces("EMU0001234 Raw Data", ["EMU0001234_period_1",
                                                                "EMU0001234_period_2",
                                                                "EMU0001234_grouped_period_1",
                                                                "EMU0001234_grouped_period_2"])

create_named_group_with_named_workspaces("EMU0001234 Cached Data", ["EMU0001234; Group; fwd; Period; 1; #1_unNorm",
                                                                   "EMU0001234; Group; fwd; Period; 1; #1_Raw_unNorm",
                                                                   "EMU0001234; Group; bwd; Period; 1; #1_unNorm",
                                                                   "EMU0001234; Group; bwd; Period; 1; #1_Raw_unNorm"])

create_named_group_with_named_workspaces("EMU0001234 Groups", ["EMU0001234; Group; fwd; Period; 1; #1",
                                                              "EMU0001234; Group; fwd; Period; 1; #1_Raw",
                                                              "EMU0001234; Group; bwd; Period; 1; #1",
                                                              "EMU0001234; Group; bwd; Period; 1; #1_Raw"])

create_named_group_with_named_workspaces("EMU0001234 Pairs", ["EMU0001234; Pair Asym; long; Period; 1; #1",
                                                             "EMU0001234; Pair Asym; long; Period; 1; #1_Raw"])

EMU0001234 = group_workspace_groups("EMU0001234", ["EMU0001234 Raw Data",
                                                   "EMU0001234 Cached Data",
                                                   "EMU0001234 Groups",
                                                   "EMU0001234 Pairs"])

############################### Second period #######################################################

create_named_group_with_named_workspaces("EMU0001234 Raw Data", ["EMU0001234_period_1",
                                                                "EMU0001234_period_2",
                                                                "EMU0001234_grouped_period_1",
                                                                "EMU0001234_grouped_period_2"])

create_named_group_with_named_workspaces("EMU0001234 Cached Data; Period 2",
                                         ["EMU0001234; Group; fwd; Period; 2; #1_unNorm",
                                         "EMU0001234; Group; fwd; Period; 2; #1_Raw_unNorm",
                                         "EMU0001234; Group; bwd; Period; 2; #1_unNorm",
                                         "EMU0001234; Group; bwd; Period; 2; #1_Raw_unNorm"])

create_named_group_with_named_workspaces("EMU0001234 Groups; Period 2", ["EMU0001234; Group; fwd; Period; 2; #1",
                                                                        "EMU0001234; Group; fwd; Period; 2; #1_Raw",
                                                                        "EMU0001234; Group; bwd; Period; 2; #1",
                                                                        "EMU0001234; Group; bwd; Period; 2; #1_Raw"])

create_named_group_with_named_workspaces("EMU0001234 Pairs; Period 2", ["EMU0001234; Pair Asym; long; Period; 2; #1",
                                                                       "EMU0001234; Pair Asym; long; Period; 2; #1_Raw"])

EMU0001234_2 = group_workspace_groups("EMU0001234; Period 2", ["EMU0001234 Raw Data",
                                                               "EMU0001234 Cached Data; Period 2",
                                                               "EMU0001234 Groups; Period 2",
                                                               "EMU0001234 Pairs; Period 2"])

############################### period combinations #######################################################

create_named_group_with_named_workspaces("EMU0001234 Raw Data", ["EMU0001234_period_1",
                                                                "EMU0001234_period_2",
                                                                "EMU0001234_grouped_period_1",
                                                                "EMU0001234_grouped_period_2"])

create_named_group_with_named_workspaces("EMU0001234 Cached Data; Period 1+2",
                                         ["EMU0001234; Group; fwd; Period; 1+2; #1_unNorm",
                                         "EMU0001234; Group; fwd; Period; 1+2; #1_Raw_unNorm",
                                         "EMU0001234; Group; bwd; Period; 1+2; #1_unNorm",
                                         "EMU0001234; Group; bwd; Period; 1+2; #1_Raw_unNorm"])

create_named_group_with_named_workspaces("EMU0001234 Groups; Period 1+2", ["EMU0001234; Group; fwd; Period; 1+2; #1",
                                                                          "EMU0001234; Group; fwd; Period; 1+2; #1_Raw",
                                                                          "EMU0001234; Group; bwd; Period; 1+2; #1",
                                                                          "EMU0001234; Group; bwd; Period; 1+2; #1_Raw"])

create_named_group_with_named_workspaces("EMU0001234 Pairs; Period 1+2", ["EMU0001234; Pair Asym; long; Period; 1+2; #1",
                                                                         "EMU0001234; Pair Asym; long; Period; 1+2; #1_Raw"])

EMU0001234_2 = group_workspace_groups("EMU0001234; Period 1+2", ["EMU0001234 Raw Data",
                                                                 "EMU0001234 Cached Data; Period 1+2",
                                                                 "EMU0001234 Groups; Period 1+2",
                                                                 "EMU0001234 Pairs; Period 1+2"])
