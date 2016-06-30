import numpy as np
from mantid.simpleapi import Fit, mtd, PDFFourierTransform

#################################
##  Customize these variables  ##
#################################
slices_workspace_name = "slices_QE"
first_slice = 49  # first_slice doesn't have to be smaller than last_slice
last_slice = 59
model_string = "Here paste the model-as-a-string"
out_root = "fit"  # root-name of workspaces containing fit-related output
out_sqe = "sqe"  # name of workspace containing slices without the background, S(Q,E)
pdf_options = {"DeltaR": 0.01,  # Options for algorithm PDFFourierTransform
               "Rmax": 20.0}
out_gre = "gre"  # Fourier transform of out_sqe using PDFFourierTransform, G(r,E)


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
    nonzero_indices = np.where(y>0)
    q = workspace.dataX(index)  # Q-values
    return q[nonzero_indices[0]], q[nonzero_indices[-1]]


def update_model(model, parameters):
    """
    Update the model string with the argument parameters
    :param model: string describing the fit model
    :param parameters: workspace containing latest optimized values
    :return: model string with updated initial values
    """
    # a. extract parameter names and values from "parameters"
    # b. Create function from "model"
    # c. Update function parameters from a.
    # d. cast function as string
    pass

def append_spectrum(single, composite):
    """
    Append a single spectrum to a matrix workspace.
    Caveat to solve: single and composite have different number of bins
    :param single: workspace containing the single spectrum
    :param composite: workspace name of the matrix workspace
    """
    pass

slices_workspace = mtd["slices_workspace_name"]
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
        StartX=start,
        EndX=end,
        Output="out_root{0}".format(id_slice),
        CreateOutput=1)
    # Update the model string. We take the current optimized model
    # as the initial guess for fitting of the next slice.
    parameters_workspace = mtd["out_root{0}_Parameters".format(id_slice)]
    model_string = update_model(model_string, parameters_workspace)
    # Calculate the PDF of the residuals, which is the slice without
    # the model background
    fits_workspace = mtd["out_root{0}_Workspace".format(id_slice)]
    residuals = ExtractSingleSpectrum(fits_workspace, 2)
    append_spectrum(residuals, out_sqe)
    single_pdf = PDFFourierTransform(InputWorkspace=residuals,
                                     InputSofQType="S(Q)-1",
                                     Qmin=start,
                                     Qmax=end,
                                     PDFType="G(r)",
                                     DeltaR=pdf_options["DeltaR"],
                                     Rmax=pdf_options["Rmax"])
    append_pdf(single_pdf, out_gre)
    id_slice += jump
