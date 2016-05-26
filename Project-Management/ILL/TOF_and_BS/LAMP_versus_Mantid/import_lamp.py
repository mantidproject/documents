from mantid.api import *
import numpy

in_directory = "/home/cs/soininen/Data/lamp-export/IN4/152/exp_7-01-418/"

in_file_name = "079680_dat.txt"

data_raw = numpy.loadtxt(in_directory + in_file_name)

# Extract non-data rows and columns.
det_angles = data_raw[1:, 0]
indices = data_raw[0, 1:]
data_raw = data_raw[1:, 1:]

# Borrow x values from another workspace.
x_input_workspace_name = "079680"
x_input_ws = mtd[x_input_workspace_name]

# data_raw has two extra spectra at the end compared to x_input_ws for reasons unknown.
# Also, disregard the monitor spectra in x_input_ws.
ws = CreateWorkspace(x_input_ws.extractX()[1:, :], data_raw[:-2, :],NSpec = len(det_angles) - 2)

