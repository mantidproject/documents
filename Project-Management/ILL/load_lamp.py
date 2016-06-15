from mantid import config
from mantid.kernel import *
from mantid.api import *
from mantid.simpleapi import *

import numpy
import h5py


def convert_Lamp_X_bins_to_Mantid(array, x_axis_equal_bins):
    
    if x_axis_equal_bins:
        # Assume regular spacing for Lamp bins
        delta_X = array[1] - array[0]

        # Move each bin to be a bins start
        array = array - delta_X/2.0

        # Return an array with a final bin added
        new_X_bins = numpy.append(array, array[-1] + delta_X/2.0)

    else:
        new_X_bins = numpy.zeros(array.size + 1)
        
        new_X_bins[0] = array[0]
        new_X_bins[-1] = array[-1]
        
        for i in range(1, array.size):
            new_X_bins[i] = (array[i-1] + array[i])/2.0
            
        print  new_X_bins.size, array.size

    return new_X_bins


def load_workspace_2D(output_ws, X, Y, data, errors, x_axis_equal_bins, y_axis_edges):
    for i in range(Y.size):
        output_ws.setX(i, X)
        output_ws.setY(i, data[i, :])
        if errors.size == data.size:
            output_ws.setE(i, errors[i, :])

    # Now set the y axis correctly
    if y_axis_edges:
        y_values = convert_Lamp_X_bins_to_Mantid(Y, x_axis_equal_bins)
        print y_values.size
    else:
        y_values = Y        
        print y_values.size

    print y_values.size
    y_axis = NumericAxis.create(y_values.size)
    for i in range(Y.size):
        y_axis.setValue(i, y_values[i])   
    output_ws.replaceAxis(1, y_axis)     


def load_workspace_1D(output_ws, X, Y, data, errors):
    output_ws.setX(0, X)
    output_ws.setY(0, data)
    if errors.size == data.size:
        output_ws.setE(0, errors)


class LoadLamp(PythonAlgorithm):

    def category(self):
        return 'DataHandling\\Nexus'

    def PyInit(self):
        self.declareProperty(FileProperty(name="InputFile", defaultValue="", action=FileAction.Load, extensions = ["hdf", "nxs"]))
        self.declareProperty(WorkspaceProperty(name="OutputWorkspace", defaultValue="", direction=Direction.Output))
        self.declareProperty(name="XAxisBinEdges", defaultValue=True, doc="Set X-axis to have bin edges instead of bin centres")
        self.declareProperty(name="XAxisEqualBins", defaultValue=True, doc="Set if X axis has constant bin widths")
        self.declareProperty(name="YAxisBinEdges", defaultValue=False, doc="Set Y-axis to have bin edges instead of bin centres")

    def PyExec(self):
        input_file = self.getProperty("InputFile").value
        x_axis_edges = self.getProperty("XAxisBinEdges").value
        x_axis_equal_bins = self.getProperty("XAxisEqualBins").value
        y_axis_edges = self.getProperty("YAxisBinEdges").value
        
        with h5py.File(input_file, 'r') as hf:
            data = numpy.array(hf.get('entry1/data1/DATA'))
            X = numpy.array(hf.get('entry1/data1/X'))
            Y = numpy.array(hf.get('entry1/data1/Y'))
            errors = numpy.array(hf.get('entry1/data1/errors'))
            monitors = numpy.array(hf.get('entry1/monitors/MONITOR1'))

        print 'Shape of the array DATA: ', data.shape
        print 'X size: ', X.size, 'Y size: ', Y.size
        print 'errors size: ', errors.size, 'monitors size: ', monitors.size

        # Need to convert the type, as can not convert from numpy.float32 to a C++ value        
        X = numpy.array(X, dtype='float')
        Y = numpy.array(Y, dtype='float')
        data = numpy.array(data, dtype='float')
        errors = numpy.array(errors, dtype='float')
        monitors = numpy.array(monitors, dtype='float')
        print 'Monitors:', monitors.shape

        if x_axis_edges:
            X = convert_Lamp_X_bins_to_Mantid(X, x_axis_equal_bins)
        else:
            X = numpy.append(X, X[-1])

        output_ws = WorkspaceFactory.create("Workspace2D", NVectors=Y.size, XLength=X.size, YLength=X.size-1)

        if (Y.size == 1) :
            load_workspace_1D(output_ws, X, Y, data, errors)
        elif (Y.size > 1):
            load_workspace_2D(output_ws, X, Y, data, errors, x_axis_equal_bins, y_axis_edges)

        self.setProperty('OutputWorkspace', output_ws)


AlgorithmFactory.subscribe(LoadLamp)
