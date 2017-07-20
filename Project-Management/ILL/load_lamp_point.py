from mantid import config
from mantid.kernel import *
from mantid.api import *
from mantid.simpleapi import *

import numpy
import h5py


def load_workspace_2D(output_ws, X, Y, data, errors):
    if Y.shape[0] == Y.size:
        print('Y is a column')
        for i in range(data.shape[0]):
            output_ws.setX(i, X)
            output_ws.setY(i, data[i, :])
            if errors.size == data.size:
                output_ws.setE(i, errors[i, :])

        y_axis = NumericAxis.create(data.shape[0])
        for i in range(data.shape[0]):
            y_axis.setValue(i, Y[i])
        output_ws.replaceAxis(1, y_axis)
    else:
        print('Y is a matrix')
        for i in range(data.shape[0]):
            output_ws.setX(i, X)
            output_ws.setY(i, data[i, :])
            if errors.size == data.size:
                output_ws.setE(i, errors[i, :])

        y_axis = NumericAxis.create(data.shape[0])
        for i in range(data.shape[0]):
            y_axis.setValue(i, Y[i][0])
        output_ws.replaceAxis(1, y_axis)


def load_workspace_1D(output_ws, X, data, errors):
    output_ws.setX(0, X)
    output_ws.setY(0, data)
    if errors.size == data.size:
        output_ws.setE(0, errors)


class LoadLampPoint(DataProcessorAlgorithm):
    def category(self):
        return 'DataHandling\\Nexus'

    def PyInit(self):
        self.declareProperty(FileProperty(name="InputFile", defaultValue="", action=FileAction.Load, extensions=["hdf", "nxs"]))
        self.declareProperty(name="ConvertToHistogram", defaultValue=False,
                             doc="Set X-axis to have bin edges instead of bin centres - sometimes required for algorithms")
        self.declareProperty(WorkspaceProperty(name="OutputWorkspace", defaultValue="", direction=Direction.Output))

    def PyExec(self):
        input_file = self.getProperty("InputFile").value
        convert_to_histogram = self.getProperty("ConvertToHistogram").value

        title = ""
        y_label = ""

        with h5py.File(input_file, 'r') as hf:
            data = numpy.array(hf.get('entry1/data1/DATA'))
            attribute_long_name_DATA = str(hf.get('entry1/data1/DATA').attrs.get('long_name'))
            if attribute_long_name_DATA is not None:
                title = attribute_long_name_DATA[3:-2]
            X = numpy.array(hf.get('entry1/data1/X'))
            Y = numpy.array(hf.get('entry1/data1/Y'))
            attribute_long_name_Y = str(hf.get('entry1/data1/X').attrs.get('long_name'))
            if attribute_long_name_Y is not None:
                y_label = attribute_long_name_Y[3:-2]
            errors = numpy.array(hf.get('entry1/data1/errors'))
            monitors = numpy.array(hf.get('entry1/monitors/MONITOR1'))

        print('Shape of the array DATA: ', data.shape)
        print('X shape: ', X.shape, 'Y shape: ', Y.shape)
        print('errors shape: ', errors.shape, 'monitors shape: ', monitors.shape)

        # Need to convert the type, as can not convert from numpy.float32 to a C++ value
        X = numpy.array(X, dtype='float')
        Y = numpy.array(Y, dtype='float')
        data = numpy.array(data, dtype='float')
        errors = numpy.array(errors, dtype='float')

        self._output_ws = CreateWorkspace(DataX=numpy.zeros(data.shape[1]), DataY=numpy.zeros(data.shape[0] * data.shape[1]), NSpec=data.shape[0])
        self._output_ws = ConvertToPointData(self._output_ws)

        self._output_ws.setYUnitLabel(y_label)
        self._output_ws.setTitle(title)

        if data.shape[0] == data.size:
            load_workspace_1D(self._output_ws, X, data, errors)
        else:
            load_workspace_2D(self._output_ws, X, Y, data, errors)

        if convert_to_histogram:
            self._output_ws = ConvertToHistogram(self._output_ws)

        self.setProperty('OutputWorkspace', self._output_ws)


AlgorithmFactory.subscribe(LoadLampPoint)
