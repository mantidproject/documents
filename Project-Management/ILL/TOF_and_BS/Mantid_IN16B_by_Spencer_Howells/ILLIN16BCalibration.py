#pylint: disable=no-init
from mantid.kernel import *
from mantid.api import (WorkspaceProperty, FileProperty, FileAction, TextAxis,
                        DataProcessorAlgorithm, AlgorithmFactory, mtd)
from mantid.simpleapi import *
import numpy as np

class ILLIN16BCalibration(DataProcessorAlgorithm):

    _input_file = None
    _calib_ws = None
    _origin_ws = None
    _map_file = None
    _peak_range = None
    _intensity_scale = None
    _mirror_mode = None


    def category(self):
        return 'Workflow\\Inelastic;PythonAlgorithms;Inelastic'


    def summary(self):
        return 'Creates a calibration workspace in energy trnasfer for IN16B.'


    def PyInit(self):
        self.declareProperty(FileProperty(name='Run', defaultValue='',
                                          action=FileAction.Load),
                             doc='Comma separated list of input files')

        self.declareProperty(name='MirrorMode', defaultValue=False,
                             doc='Data uses mirror mode')

        self.declareProperty(FileProperty(name='MapFile', defaultValue='',
                                          action=FileAction.OptionalLoad,
                                          extensions=['xml']),
                             doc='Comma separated list of input files')

        self.declareProperty(FloatArrayProperty(name='PeakRange', values=[0.0, 100.0],
                                                validator=FloatArrayMandatoryValidator()),
                             doc='Peak range in energy transfer')

        self.declareProperty(name='ScaleFactor', defaultValue=1.0,
                             doc='Intensity scaling factor')

        self.declareProperty(WorkspaceProperty('OutputWorkspace', '',
                                               direction=Direction.Output),
                             doc='Output workspace for calibration data')


    def PyExec(self):
        self._setup()

        temp_raw = '__raw'
        temp_left = '__red_left'
        temp_right = '__red_right'
        temp_red = '__red'

        # Do an energy transfer reduction
        IndirectILLReduction(Run=self._input_file,
                             CalibrationWorkspace='',
                             Analyser='silicon',
                             Reflection='111',
                             MirrorMode=self._mirror_mode,
                             RawWorkspace=temp_raw,
                             LeftWorkspace=temp_left,
                             RightWorkspace=temp_right,
                             ReducedWorkspace=temp_red,
                             MapFile=self._map_file)

        self._setup_mirror(temp_raw)

        # Integrate within peak range
        number_histograms = mtd[temp_red].getNumberHistograms()
        Integration(InputWorkspace=temp_red,
                    OutputWorkspace=self._calib_ws + '_sum',
                    RangeLower=float(self._peak_range[0]),
                    RangeUpper=float(self._peak_range[1]))

        ws_mask, num_zero_spectra = FindDetectorsOutsideLimits(InputWorkspace=self._calib_ws + '_sum',
                                                               OutputWorkspace='__temp_ws_mask')
        DeleteWorkspace(ws_mask)

        if self._mirror_mode:
            Integration(InputWorkspace=temp_left,
                        OutputWorkspace=self._calib_ws + '_left',
                        RangeLower=float(self._peak_range[0]),
                        RangeUpper=float(self._peak_range[1]))
            Integration(InputWorkspace=temp_right,
                        OutputWorkspace=self._calib_ws + '_right',
                        RangeLower=float(self._peak_range[0]),
                        RangeUpper=float(self._peak_range[1]))
            workspaces = [self._calib_ws + '_sum', self._calib_ws + '_left', self._calib_ws + '_right']
        else:
            CloneWorkspace(InputWorkspace=self._calib_ws + '_sum',
                           OutputWorkspace=self._calib_ws + '_red')
            workspaces = [self._calib_ws + '_sum', self._calib_ws + '_red']

        for ws in workspaces:
        # Process automatic scaling
            temp_sum = '__sum'
            SumSpectra(InputWorkspace=ws,
                       OutputWorkspace=temp_sum)
            total = mtd[temp_sum].readY(0)[0]
            DeleteWorkspace(temp_sum)

            if self._intensity_scale is None:
                self._intensity_scale = 1 / (total / (number_histograms - num_zero_spectra))

        # Apply scaling factor
            Scale(InputWorkspace=ws,
                  OutputWorkspace=ws,
                  Factor=self._intensity_scale,
                  Operation='Multiply')

        GroupWorkspaces(InputWorkspaces=workspaces,
                        OutputWorkspace=self._calib_ws)
        self.setProperty('OutputWorkspace', self._calib_ws)

        # if mirror mode, calculate means
        if self._mirror_mode:
            left_mean = 'left_mean'
            self._calc_mean(temp_left, left_mean)
            right_mean = 'right_mean'
            self._calc_mean(temp_right, right_mean)
            RenameWorkspace(InputWorkspace=left_mean,
                            OutputWorkspace=self._origin_ws)

            ConjoinWorkspaces(InputWorkspace1=self._origin_ws,
                              InputWorkspace2=right_mean,
                              CheckOverlapping=False)
            y_axis = TextAxis.create(number_histograms)
            mtd[self._origin_ws].replaceAxis(1, y_axis)
            y_axis.setLabel(0, 'left')
            y_axis.setLabel(1, 'right')
            mtd[self._origin_ws].setYUnitLabel('Peak centre (meV)')
            DeleteWorkspace(temp_left)
            DeleteWorkspace(temp_right)
        else:
            red_mean = 'red_mean'
            self._calc_mean(temp_red, red_mean)
            RenameWorkspace(InputWorkspace=red_mean,
                            OutputWorkspace=self._origin_ws)
            y_axis = TextAxis.create(number_histograms)
            mtd[self._origin_ws].replaceAxis(1, y_axis)
            y_axis.setLabel(0, 'red')

        # Clean up unused workspaces
        DeleteWorkspace(temp_raw)
        DeleteWorkspace(temp_red)

		
    def _setup(self):
        """
        Gets properties.
        """

        self._input_file = self.getProperty('Run').value
        self._calib_ws = self.getPropertyValue('OutputWorkspace')
        self._origin_ws = self._calib_ws[:-5] + 'origin'

        self._map_file = self.getPropertyValue('MapFile')
        self._peak_range = self.getProperty('PeakRange').value
        self._mirror_mode = self.getProperty('MirrorMode').value

        self._intensity_scale = self.getProperty('ScaleFactor').value
        if self._intensity_scale == 1.0:
            self._intensity_scale = None

    def _setup_mirror(self, ws):
        run = mtd[ws].getRun()
        if run.hasProperty('Doppler.mirror_sense'):
            mirror_sense = run.getLogData('Doppler.mirror_sense').value
            if mirror_sense == 16:
                self._mirror_mode = False
                logger.information('Doppler mirror_sense is %s' % self._mirror_mode)
            elif mirror_sense == 14:
                self._mirror_mode = True
                logger.information('Doppler mirror_sense is %s' % self._mirror_mode)
            else:
                logger.information('Doppler mirror_sense is Unknown')


    def validateInputs(self):
        """
        Validates input ranges.
        """
        issues = dict()

        issues['PeakRange'] = self._validate_range('PeakRange')

        return issues


    def _validate_range(self, property_name):
        """
        Validates a range property.

        @param property_name Name of the property to validate
        @returns String detailing error, None if no error
        """

        prop_range = self.getProperty(property_name).value
        if len(prop_range) == 2:
            if prop_range[0] > prop_range[1]:
                return 'Invalid range'
        else:
            return 'Incorrect number of values (should be 2)'

        return None

    def _calc_mean(self, ws_in, ws_out):
        moment_0 = '__moment_0'
        moment_1 = '__moment_1'
        ConvertToPointData(InputWorkspace=ws_in, OutputWorkspace='__temp_ws')
        x_data = np.asarray(mtd['__temp_ws'].readX(0))
        x_workspace = CreateWorkspace(OutputWorkspace="__temp_x",
                                      DataX=x_data, DataY=x_data, UnitX="DeltaE")
        Multiply('__temp_ws', x_workspace, OutputWorkspace=moment_1)
        Integration(ws_in, OutputWorkspace=moment_0)
        ConvertToHistogram(InputWorkspace=moment_1, OutputWorkspace=moment_1)
        Integration(moment_1, OutputWorkspace=moment_1)
        Divide(moment_1, moment_0, OutputWorkspace=moment_1)
        Transpose(InputWorkspace=moment_1, OutputWorkspace=ws_out)
        DeleteWorkspace('__temp_ws')
        DeleteWorkspace('__temp_x')
        DeleteWorkspace(moment_0)
        DeleteWorkspace(moment_1)
        return


# Register algorithm with Mantid
AlgorithmFactory.subscribe(ILLIN16BCalibration)
