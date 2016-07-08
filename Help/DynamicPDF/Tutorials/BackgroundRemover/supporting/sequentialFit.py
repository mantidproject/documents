import numpy as np
from mantid.simpleapi import Fit, mtd, PDFFourierTransform,\
    Rebin, AppendSpectra, LoadNexus, ExtractSingleSpectrum,\
    CloneWorkspace
from pdb import set_trace as tr

#################################
##  Customize these variables  ##
#################################
slices_workspace_name = "slices_QE"
first_slice = 0  # first_slice doesn't have to be smaller than last_slice
last_slice = 115
out_root = "fit"  # root-name of output workspaces containing fit-related output
out_sqe = "sqe_no_background"  # name of output workspace containing slices without the background, S(Q,E)
out_gre = "gre"  # output workspace containing the Fourier transform of out_sqe using PDFFourierTransform, G(r,E)
gre_options = {"DeltaR": 0.01,  # Options for algorithm PDFFourierTransform
               "Rmax": 20.0}
# Here paste the QuadXGaus+LB model you copied from the model builder
model_string = """(composite=ProductFunction,NumDeriv=false;name=Quadratic,
A0=0.0771474,A1=-0.0184599,A2=0.00192572;name=Gaussian,Height=1,PeakCentre=4.06054,
Sigma=2.91412,ties=(Height=1));name=LinearBackground,A0=-0.0362006,A1=0.00913319"""

############################################
##  Unnecessary to change the code below  ##
############################################


def get_boundaries(workspace, index):
    """
    Return non-zero intensity range
    :param workspace: workspace containing the slices
    :param index: workspace index for the slice of interest
    :return: starting and ending Q values having non-zero intensity
    """
    y = workspace.dataY(index)  # intensities
    nonzero_indices = np.where(y>0)[0]
    q = workspace.dataX(index)  # Q-values
    return q[nonzero_indices[0]], q[nonzero_indices[-1]]


def templatize(model):
    """
    Substitute specific parameter values with appropriate keywords.
    NOTICE: Now only works for the built-in model QuadXGaus+LB
    :param model: model string with specific parameter values
    :return: templatized string
    """
    return """
  (composite=ProductFunction,NumDeriv=false;
    name=Quadratic,A0={{f0.f0.A0}},A1={{f0.f0.A1}},A2={{f0.f0.A2}};
    name=Gaussian,Height=1,PeakCentre={{f0.f1.PeakCentre}},Sigma={{f0.f1.Sigma}},ties=(Height=1)
  );
  name=LinearBackground,A0={{f1.A0}},A1={{f1.A1}}
"""


def update_model(model, table):
    """
    Update the model string with the argument parameters
    :param model: string describing the fit model
    :param table: table workspace containing latest optimized values
    :return: model string with updated parameter values
    """
    new_model = templatize(model)
    for index in range(table.rowCount()-1):
        row = table.row(index)
        new_model = new_model.replace('{{'+row["Name"]+'}}', str(row["Value"]))
    return new_model


def append_spectrum(single, composite):
    """
    Append a single spectrum to a matrix workspace.
    Caveat to solve: single and composite have different number of bins
    :param single: workspace containing the single new spectrum
    :param composite: workspace matrix containing the processed spectra
    """
    # Find binning triad for the single and composite workspaces
    qs = single.dataX(0)
    qsm, dqs, qsM = qs[0], (qs[-1]-qs[0])/(len(qs)-1), qs[-1]
    qc = composite.dataX(0)
    qcm, dqc, qcM = qc[0], (qc[-1]-qc[0])/(len(qc)-1), qc[-1]
    # Find the biggest range and finer binning
    qmin = qsm if qsm < qcm else qcm
    dq = dqs if dqs < dqc else dqc
    qmax = qsM if qsM < qcM else qcM
    # Rebin when necessary
    delete_single = False
    if [qsm, dqs, qsM] != [qmin, dq, qmax]:
        delete_single = True
        single = Rebin(single, [qmin, dq, qmax])
    if [qcm, dqc, qcM] != [qmin, dq, qmax]:
        composite = Rebin(composite, [qmin, dq, qmax], OutputWorkspace=composite.name())
    composite = AppendSpectra(composite, single, OutputWorkspace=composite.name())
    if delete_single:
        DeleteWorkspace(single)
    return composite

sqe = None
gre = None
workspaces_to_group = list()
slices_workspace = mtd[slices_workspace_name]
jump = 1 if first_slice < last_slice else -1
id_slice = first_slice
while id_slice != last_slice:
    start, end = get_boundaries(slices_workspace, id_slice)
    """
    Algorithm Fit creates the following workspaces
    out_root_Parameters: optimal values of fitting parameters
    out_root_Workspaces: slice, model-fit, residuals, and model-components
    out_root_CovariantMatrix: correlations among the workspaces
    """
    Fit(Function=model_string,
        InputWorkspace=slices_workspace_name,
        WorkspaceIndex=id_slice,
        StartX=start,
        EndX=end,
        Output="{0}{1}".format(out_root,id_slice),
        CreateOutput=True)
    for key in ("Workspace", "Parameters", "NormalisedCovarianceMatrix"):
        workspaces_to_group.append("{0}{1}_{2}".format(out_root, id_slice, key))
    # Update the model string. We take the current optimized model
    # as the initial guess for fitting of the next slice.
    parameters_workspace = mtd["{0}{1}_Parameters".format(out_root, id_slice)]
    model_string = update_model(model_string, parameters_workspace)
    # Calculate the PDF of the residuals, which is the slice without
    # the model background
    fits_workspace = mtd["{0}{1}_Workspace".format(out_root, id_slice)]
    residuals = ExtractSingleSpectrum(fits_workspace, 2)
    sqe = CloneWorkspace(residuals, OutputWorkspace=out_sqe)\
        if not sqe else append_spectrum(residuals, sqe)
    single_gre = PDFFourierTransform(InputWorkspace=residuals,
                                     InputSofQType="S(Q)-1",
                                     Qmin=start,
                                     Qmax=end,
                                     PDFType="G(r)",
                                     DeltaR=gre_options["DeltaR"],
                                     Rmax=gre_options["Rmax"])
    gre = CloneWorkspace(single_gre, OutputWorkspace=out_gre)\
        if not gre else append_spectrum(single_gre, gre)
    id_slice += jump

# Group all the fit workspaces
GroupWorkspaces(InputWorkspaces=",".join(workspaces_to_group), OutputWorkspace="{0}s".format(out_root))

# Clean up
DeleteWorkspace(residuals)
DeleteWorkspace(single_gre)