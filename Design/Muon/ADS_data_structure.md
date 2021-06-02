# Sample Logs

We want to use the sample logs of the workspaces to hold information about how these workspaces were produced. This means we don't need to carry around information about the groups and pairs, and we can always reliably and quickly discern this information from the logs.

In the current GUI, the only way to get this information is to reverse-engineer the workspace name. This is a bad idea, but can easily be fixed. Even worse, there is some information we simply cannot obtain this way (for example, which detector id's were combined to give a particular group? Was a time offset applied?). This means the workspace and its name alone cannot be used to figure out what was done to calculate it.

### Proposed sample log structure for every muon workspace

We use a unique string (e.g. "analysis") prepended to the name of each log to distinguish them from the rest of the logs. There is a split between "pre-process" parameters and "group" or "pair" parameters; roughly following the earlier proposal for the sub-algorithms of `MuonProcess`;

```python
analysis_periods = 2
analysis_rebin_args = 5
analysis_crop_x_min = 0.1
analysis_crop_x_max = 10.0
analysis_time_offset = 0.1

analysis_period_combination = "1+2"

# for groups
analysis_group_name = "fwd"
analysis_group_detectors = "1-5"

# for pairs
analysis_pair_name = "long"
analysis_group1 = "1-5"
analysis_group2 = "6-10"
analysis_group1_name = "fwd"
analysis_group1_names = "bwd"
analysis_alpha = 1.0
```

This allows us to do the following things (which we cannot do otherwise);

- Produce the workspace's name from its own logs (this is a hugely useful feature)
- We can check if a workspace is a group/pair by looking for `group_name` or `pair_name`.
- We can actually completely reproduce the analysis that created a workspace from these parameters (plus others from the log such as run and instrument).
- We ensure that saved/loaded workspaces still make sense outside of the context of the Muon GUI, since all the logs are not interface-specific concepts, and could be understood by any muon scientist.

# Current ADS Data Structure : All the non-fitting stuff

For future reference, here is a summary of how the current data is structured in the ADS.

Setting for example "EMU" as the instrument : 

- Each run has its own folder, named by a combination of `instrument` + `run`.
- The GUI handles only one file at a time, the raw data is held in `MuonAnalysis` which is either a `MatrixWorkspace` (if single period) or `GroupWorkspace` if multi-period. Then the workspaces within the group are named with trailing integers beginning at 1.
- Each time a group or pair is calculated, the results appear in the relevant run folder. There are four workspaces, the "Raw" and "unNorm" versions are without rebinning and without normalization respectively.
- The groups and pairs are placed together, despite being conceptually different objects.
- `MuonAnalysisTFNormalizations` is a global table which stores information from each of the runs.
- `MuonAnalysisGrouped` is the same as `MuonAnalysis` but grouped across all detectors (i.e. just the sum of all the spectra), this is always a group workspace, the workspaces in it are the periods of the data.

The "folder" structure is shown below (where a folder represents a `GroupWorkspace`)

```
MuonAnalysis

# OR

MuonAnalysis/
    MuonAnalysis_1
    MuonAnalysis_2
    ...

EMU0001234/
    EMU0001234; Pair long; 1; #1
    EMU0001234; Pair long; 1; #1_Raw
    EMU0001234; Pair long; 1; #1_unNorm
    EMU0001234; Pair long; 1; #1_Raw_UnNorm

    ... # a set of four workspaces (as above) for each group, group asymmetry or pair
    ... # + a repeat of these four each time the analysis is re-run, with the final number being incremented.

EMU0001235/
    EMU0001235; Pair long; 1+2; #1
    EMU0001235; Pair long; 1+2; #1_Raw
    EMU0001235; Pair long; 1+2; #1_unNorm
    EMU0001235; Pair long; 1+2; #1_Raw_UnNorm

    EMU0001235; Group fwd; 1; #1
    EMU0001235; Group fwd; 1; #1_Raw
    EMU0001235; Group fwd; 1; #1_unNorm
    EMU0001235; Group fwd; 1; #1_Raw_UnNorm

    ...

MuonAnalysisTFNormalizations

MuonAnalysisGrouped/
    MuonAnalysis_Grouped_1
```

## Issues with the current structure

Below are some issues I think are making this structure either hard to understand or hard to use from a user's perspective;

- Generally speaking, there tends to be a huge proliferation of workspaces within each folder, many of which the user simply does not need to see or interact with (e.g. the `unNorm` which were only added a few months ago).

- Different combinations of periods are held within the run folder. For example I can redo the same analysis with periods 1 and 2 added together, or periods 1 and 2 subtracted. These are fundamentally different analyses and should be kept separate.

- Grouping and pairing data are held within the same run folder, despite these being conceptually different objects.

- The `MuonAnalysis` workspace enforces that we can only deal with one file at a time; there is no reason to impose this and in fact it would be better to be able to deal with several files simultaneously.

- The `MuonAnalysis` being different kinds of objects depending on whether the data is multi-period or not is unneccessary and confusing; why not simply have a group in all cases, with just one workspace for single period data?

# Proposed Modifications

I propose to keep the data structure and naming *essentially* the same, with a few minor modifications which act to make the structure more readable, cleaner, and gather data together which is likely to be accessed at once, and to hide data that the user does not need to interact with.

Modifications to the current structure are : 

- Another layer of folders within each run folder; one for groups, pairs and group-asymmetries.

- A raw data folder in each run folder, to prevent re-loading. This does away with the odd `MuonAnalysis` workspace or workspace group. Single period data is then represented by just one workspace in the raw folder, this suggests thinking about single period data as a limiting case of multi-period data which makes much cleaner analyses.

- Place the intermediate data which is of no interest to the user in its own folder called "cached_data".

- Each set of period combinations has its own folder; this way we don't mix different periods combinations in the same folder. There is never a scenario where this is a good idea as the names are so similar that on a quick glance they look identical and it is so easy to accidentally select the wrong one.

- The grouped version of MuonAnalysis (the old "MuonAnalysisGrouped") are placed alongside the raw data, with modified names.


```python
EMU0001234/

    # Holds the old MuonAnalysis and MuonAnalysisGrouped
    EMU0001234_raw_data/
        EMU0001234_period_1  # first period
        EMU0001234_period_2  # second period
        ...
        EMU0001234_period_n  # nth and last period
        EMU0001234_grouped_period_1 # first period, grouped across all detectors
        ...
        EMU0001234_grouped_period_n # last period, grouped across all detectors

    # All the unNorm files go in here
    EMU0001234_cached_data/
        EMU0001235; Group fwd; 1; #1_unNorm
        EMU0001235; Group fwd; 1; #1_Raw_UnNorm

    # both group counts and group asym
    EMU0001234_groups/

        # normal grouped counts, with non-rebinned data visible
        EMU0001234; Group; fwd; Counts; #1
        EMU0001235; Group; fwd; Counts; #1_noRebin
        EMU0001234; Group; bwd; Counts; #1
        EMU0001235; Group; bwd; Counts; #1_noRebin

        # also group asymmetries, with non-rebinned data visible
        EMU0001234; Group; fwd; Asym; #1
        EMU0001234; Group; fwd; Asym; #1_noRebin
        
    # the results of pair asymmetry calculations
    EMU0001234_pairs/

        EMU0001234; Pair long1; Asym; #1
        EMU0001234; Pair long2; Asym; #1
        

# multiple period combinations are held completely separately
EMU0001235; Periods 1+2/

    EMU0001235_raw_data/
        EMU0001235_period_1  # first period
        EMU0001235_period_2  # second period
        ...

    EMU0001235_groups/...

    ...

# As before, this stays outside of the rest of the structure
MuonAnalysisTFNormalizations
```

# Current ADS Data Structure : All the fitting stuff

Part of the current interface fitting design is a set of exclusive options on the "type" of fit to gather workspaces for; the options are "Individual", "Sequential", "Simultaneous" and "Multiple".

The current structure of fitting related data in the ADS is as follows;

```python
# Individual fit mode, saves to same place as original data.
# If only one run is selected this is how both co-add and simultaneous modes save
EMU0001234/
    EMU0001234; Pair long; 1; #1_Workspace
    EMU0001234; Pair long; 1; #1_Parameters
    EMU0001234; Pair long; 1; #1_CovarianceMatrix

    EMU0001234; Group long; 1; #1_Workspace
    EMU0001234; Group long; 1; #1_Parameters
    EMU0001234; Group long; 1; #1_CovarianceMatrix

# Result of a fit in co-add mode in multiple-fitting
EMU0001230-4/
    EMU0001230-4; Pair long; 1; #1_Workspace
    EMU0001230-4; Pair long; 1; #1_Parameters
    EMU0001230-4; Pair long; 1; #1_CovarianceMatrix

# A sequential fit from the fit menu in single fitting
# The user supplies a lable, "Label1" in this case
MuonSeqFit_Label1/
    MuonSeqFit_Label1_EMU0001234/
        MuonSeqFit_Label1_EMU0001234_Workspace
        MuonSeqFit_Label1_EMU0001234_Parameters
        MuonSeqFit_Label1_EMU0001234_NormalizedCovarianceMatrix

    MuonSeqFit_Label1_EMU0001235/
        MuonSeqFit_Label1_EMU0001235_Workspace
        MuonSeqFit_Label1_EMU0001235_Parameters
        MuonSeqFit_Label1_EMU0001235_NormalizedCovarianceMatrix

    MuonSeqFit_Label1_EMU0001236/
        ...

    ...

# Simultaneous mode in multiple-fitting
MuonSimulFit_1234-1240/
    MuonSimulFit_1234_1240_NormalizedCovarianceMatrix
    MuonSimulFit_1234_1234_EMU0001234_long_Parameters
    MuonSimulFit_1234_1235_EMU0001234_long_Parameters
    MuonSimulFit_1234_1236_EMU0001234_long_Parameters
    ...
    MuonSimulFit_1234_1234_EMU0001234_long_Workspace
    MuonSimulFit_1234_1235_EMU0001234_long_Workspace
    MuonSimulFit_1234_1236_EMU0001234_long_Workspace
```

## Issues with this current structure

- The individual fitting results are saved to the same folder as the data that is fit. This adds to the verbosity of such folders and removes a distinction which is preserved for the other kinds of fitting, if nothing else this is inconsistent.

- No string in name to indicate that the workspace is a fit results, and no indication that it is "individual fit" mode.

- In theory, in the individual fitting mode a group and pir could share the same name and the fitted result would overwrite itself. The resulting workspace names would be completely ambiguous as to which was being stored.

- The structure of the GUI and structure of the saved data are different, making it very confusing to understand the data from the GUI.

- From a sequential fit, there is no way to identify the group or pair

- From a simultaneous fit there is no way to determine a pair or group

# Proposed modifications

For the fitted data the following structure may be sensible. Modifications to the current structure are:

- Having individual fits in their own group, rather than in amongst the data that is fitted to. Currently the only way to tell if a workspace is the result of a fit is that is has "_Workspace" on the end of its name. Somebody using the ADS for the first time would struggle to understand this, and it is much clearer to have the individual fits residing in their own "folder". This also brings the results structure of individual fits more in line with that on sequential fits.

- The introduction of one extra layer to the nested workspaces, that separates Sequential/Simultaneous/Individual fits. This then mimics the structure of the GUI and makes it easier to understand.

```python
MuonIndividualFits/

    # Single period
    EMU0001234/
        Fit_EMU0001234 Workspace; Pair; long; Asym; Period 1; #1
        Fit_EMU0001234 Parameters; Pair; long; Asym; Period 1; #1
        Fit_EMU0001234 Covariance; Pair; long; Asym; Period 1; #1

    # Multi-period combinations
    EMU0001234 Periods 1+2/
        Fit_EMU0001234 Workspace; Pair; long; Asym; Period 1+2; #1
        Fit_EMU0001234 Parameters; Pair; long; Asym; Period 1+2; #1
        Fit_EMU0001234 Covariance; Pair; long; Asym; Period 1+2; #1

    EMU0001235/
        Fit_EMU0001235 Workspace; Pair long; Asym; Period 1; #1
        Fit_EMU0001235 Parameters; Pair long; Asym; Period 1; #1
        Fit_EMU0001235 Covariance; Pair long; Asym; Period 1; #1

    ... # All possible instruments/runs

MuonSequentialFits/

    # unique labels for each sequential fit
    SequenialFit_Label1/

        # Each run from the sequential fit
        Seq_EMU0001234/
            Seq_EMU0001234 Workspace; Pair; long; Asym; Period 1; #1_Label1
            Seq_EMU0001234 Parameters; Pair; long; Asym; Period 1; #1_Label1
            Seq_EMU0001234 Covariance; Pair; long; Asym; Period 1; #1_Label1
            ...

        Seq_EMU0001235/ 
            Seq_EMU0001235 Workspace; Pair; long; Asym; Period 1; #1_Label1
            ...

    SequentialFit_Label2/

        ...

MuonSimultaneousFits/

    # unique labels for each simultaneous fit
    Sim_Label1/
        Sim_Label1; Pair long; Asym; Period 1; #1_Label1
        Sim_Label1; Pair long; Asym; Period 1; #1_Label1
        Sim_Label1; Pair long; Asym; Period 1; #1_Label1

    Sim_Label2/
        Sim_Label1; Pair long; Asym; Period 1; #1_Label1
        ...
    
```