from mantid import config
from mantid.kernel import *
from mantid.api import *
from mantid.simpleapi import *

import numpy
import h5py


def convert_Lamp_X_bins_to_Mantid(array):
    # Assume regular spacing for Lamp bins
    delta_X = array[1] - array[0]

    # Move each bin to be a bins start
    array = array - delta_X

    # Return an array with a final bin added
    return numpy.append(array, array[-1] + delta_X)


def load_workspace_2D(output_ws, X, Y, data, errors):
    for i in range(Y.size):
        output_ws.setX(i, X)
        output_ws.setY(i, data[i, :])
        if errors.size == data.size:
            output_ws.setE(i, errors[i, :])


def load_workspace_1D(output_ws, X, Y, data, errors):
    output_ws.setX(0, X)
    output_ws.setY(0, data)
    if errors.size == data.size:
        output_ws.setE(0, errors)


class LoadLamp(PythonAlgorithm):

    def category(self):
        return 'DataHandling\\Nexus'

    def PyInit(self):
        self.declareProperty(FileProperty(name="InputFile", defaultValue="", action=FileAction.Load, extensions = ["nxs", "hdf"]))
        self.declareProperty(WorkspaceProperty(name="OutputWorkspace", defaultValue="", direction=Direction.Output))

    def PyExec(self):
        input_file = self.getProperty("InputFile").value
        
        with h5py.File(input_file, 'r') as hf:
            data = numpy.array(hf.get('entry1/data1/DATA'))
            X = numpy.array(hf.get('entry1/data1/X'))
            Y = numpy.array(hf.get('entry1/data1/Y'))
            errors = numpy.array(hf.get('entry1/data1/errors'))
            monitors = numpy.array(hf.get('entry1/monitors/MONITOR1'))

        print 'Shape of the array DATA: ', data.shape
        print 'X size: ', X.size, 'Y size: ', Y.size
        print 'errors size: ', errors.size, 'monitors size: ', monitors.size

        output_ws = WorkspaceFactory.create("Workspace2D", NVectors=Y.size, XLength=X.size+1, YLength=X.size)

        # Need to convert the type, as can not convert from numpy.float32 to a C++ value        
        X = numpy.array(X, dtype='float')
        Y = numpy.array(Y, dtype='float')
        data = numpy.array(data, dtype='float')
        errors = numpy.array(errors, dtype='float')
        monitors = numpy.array(monitors, dtype='float')
        print 'Monitors:', monitors.shape

        X = convert_Lamp_X_bins_to_Mantid(X)

        if (Y.size   == 1) :
            load_workspace_1D(output_ws, X, Y, data, errors)
        elif (Y.size > 1):
            load_workspace_2D(output_ws, X, Y, data, errors)

        self.setProperty('OutputWorkspace', output_ws)


AlgorithmFactory.subscribe(LoadLamp)
