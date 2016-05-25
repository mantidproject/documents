#pylint: disable=no-init,invalid-name
from mantid.simpleapi import *
from mantid.kernel import StringListValidator, Direction
from mantid.api import DataProcessorAlgorithm, PropertyMode, AlgorithmFactory, WorkspaceGroupProperty, \
                       FileProperty, FileAction, MatrixWorkspaceProperty
from mantid import config, logger, mtd

import numpy as np
import os.path

#pylint: disable=too-many-instance-attributes
class IndirectILLReduction(DataProcessorAlgorithm):

    _raw_workspace = None
    _red_workspace = None
    _red_left_workspace = None
    _red_right_workspace = None
    _map_file = None
    _use_mirror_mode = None
    _shift_origin = False
    _save = None
    _plot = None
    _instrument_name = None
    _run_number = None
    _analyser = None
    _reflection = None
    _run_name = None
    _calibration_workspace = None
    _origin_workspace = None

    def category(self):
        return "Workflow\\MIDAS;Inelastic;PythonAlgorithms"


    def summary(self):
        return 'Performs an energy transfer reduction for ILL indirect inelastic data.'


    def PyInit(self):
        # Input options
        self.declareProperty(FileProperty('Run', '',
                                          action=FileAction.Load,
                                          extensions=["nxs"]),
                             doc='File path of run.')

        self.declareProperty(WorkspaceGroupProperty("CalibrationWorkspace", "",
                                                     optional=PropertyMode.Optional,
                                                     direction=Direction.Input),
                             doc="Workspace containing calibration intensities.")

        self.declareProperty(name='Analyser', defaultValue='silicon',
                             validator=StringListValidator(['silicon']),
                             doc='Analyser crystal.')

        self.declareProperty(name='Reflection', defaultValue='111',
                             validator=StringListValidator(['111']),
                             doc='Analyser reflection.')

        self.declareProperty(FileProperty('MapFile', '',
                                          action=FileAction.OptionalLoad,
                                          extensions=["xml"]),
                             doc='Filename of the map file to use. If left blank the default will be used.')

        self.declareProperty(name='MirrorMode', defaultValue=False,
                             doc='Whether to use mirror mode.')

        # Output workspace properties
        self.declareProperty(MatrixWorkspaceProperty("RawWorkspace", "",
                                                     direction=Direction.Output),
                             doc="Name for the output raw workspace created.")

        self.declareProperty(MatrixWorkspaceProperty("ReducedWorkspace", "",
                                                     direction=Direction.Output),
                             doc="Name for the output reduced workspace created. If mirror mode is used this will be the sum of both "
                             "the left and right hand workspaces.")

        self.declareProperty(MatrixWorkspaceProperty("LeftWorkspace", "",
                                                     optional=PropertyMode.Optional,
                                                     direction=Direction.Output),
                             doc="Name for the left workspace if mirror mode is used.")

        self.declareProperty(MatrixWorkspaceProperty("RightWorkspace", "",
                                                     optional=PropertyMode.Optional,
                                                     direction=Direction.Output),
                             doc="Name for the right workspace if mirror mode is used.")

        # Output options
        self.declareProperty(name='Save', defaultValue=False,
                             doc='Switch Save result to nxs file Off/On.')
        self.declareProperty(name='Plot', defaultValue=False,
                             doc='Whether to plot the output workspace.')


    def PyExec(self):
        self._setup()
        logger.information('Nxs file : %s' % self._run_path)
        LoadILLIndirect(FileName=self._run_path,
                        OutputWorkspace=self._raw_workspace)
        self._setup_mirror()
        if self._calibration_workspace != '':
            LoadNexus(Filename=self._origin_workspace + '.nxs',
                      OutputWorkspace=self._origin_workspace)                  

        instrument = mtd[self._raw_workspace].getInstrument()
        self._instrument_name = instrument.getName()
        self._run_number = mtd[self._raw_workspace].getRunNumber()
        self._analyser = self.getPropertyValue('Analyser')
        self._reflection = self.getPropertyValue('Reflection')
        self._run_name = self._instrument_name + '_' + str(self._run_number)

        output_workspaces = self._reduction()

        self.setPropertyValue('RawWorkspace', self._raw_workspace)
        self.setPropertyValue('ReducedWorkspace', self._red_workspace)

        if self._use_mirror_mode:
            self.setPropertyValue('LeftWorkspace', self._red_left_workspace)
            self.setPropertyValue('RightWorkspace', self._red_right_workspace)

        if self._save:
            workdir = config['defaultsave.directory']
            for ws in output_workspaces:
                file_path = os.path.join(workdir, ws + '.nxs')
                SaveNexusProcessed(InputWorkspace=ws, Filename=file_path)
                logger.information('Output file : ' + file_path)

        if self._plot:
            from IndirectImport import import_mantidplot
            mtd_plot = import_mantidplot()
            graph = mtd_plot.newGraph()

            for ws in output_workspaces:
                mtd_plot.plotSpectrum(ws, 0, window=graph)

            layer = graph.activeLayer()
            layer.setAxisTitle(mtd_plot.Layer.Bottom, 'Energy Transfer (meV)')
            layer.setAxisTitle(mtd_plot.Layer.Left, '')
            layer.setTitle('')

    def _setup(self):
        self._run_path = self.getPropertyValue('Run')
        self._calibration_workspace = self.getPropertyValue('CalibrationWorkspace')
        self._origin_workspace = self._calibration_workspace[:-5] + 'origin'
        self._raw_workspace = self.getPropertyValue('RawWorkspace')
        self._red_workspace = self.getPropertyValue('ReducedWorkspace')
        self._red_left_workspace = self._red_workspace + '_left'
        self._red_right_workspace = self._red_workspace + '_right'
        self._map_file = self.getProperty('MapFile').value

        self.setPropertyValue('RawWorkspace', self._raw_workspace)
        self.setPropertyValue('ReducedWorkspace', self._red_workspace)

        self._use_mirror_mode = self.getProperty('MirrorMode').value
        if self._calibration_workspace == '':
            self._shift_origin = False
        else:
            self._shift_origin = True
        logger.information('Shift option is %s' % self._shift_origin)

        self._save = self.getProperty('Save').value
        self._plot = self.getProperty('Plot').value
		
    def _setup_mirror(self):
        run = mtd[self._raw_workspace].getRun()
        if run.hasProperty('Doppler.mirror_sense'):
            mirror_sense = run.getLogData('Doppler.mirror_sense').value
            if mirror_sense == 16:
                self._use_mirror_mode = False
                logger.information('Doppler mirror_sense is %s' % self._use_mirror_mode)
            elif mirror_sense == 14:
                self._use_mirror_mode = True
                logger.information('Doppler mirror_sense is %s' % self._use_mirror_mode)
            else:
                logger.information('Doppler mirror_sense is Unknown')

        AddSampleLog(Workspace=self._raw_workspace, LogName="mirror_sense",
                     LogType="String", LogText=str(self._use_mirror_mode))

    def _reduction(self):
        """
        Run energy conversion for IN16B
        """
        logger.information('Input workspace : %s' % self._raw_workspace)

        idf_directory = config['instrumentDefinition.directory']
        ipf_name = self._instrument_name + '_' + self._analyser + '_' + self._reflection + '_Parameters.xml'
        ipf_path = os.path.join(idf_directory, ipf_name)

        LoadParameterFile(Workspace=self._raw_workspace, Filename=ipf_path)
        AddSampleLog(Workspace=self._raw_workspace,
                     LogName="facility",
                     LogType="String",
                     LogText="ILL")

        if self._map_file == '':
            # path name for default map file
            instrument = mtd[self._raw_workspace].getInstrument()
            if instrument.hasParameter('Workflow.GroupingFile'):
                grouping_filename = instrument.getStringParameter('Workflow.GroupingFile')[0]
                self._map_file = os.path.join(config['groupingFiles.directory'], grouping_filename)
            else:
                raise ValueError("Failed to find default map file. Contact development team.")

            logger.information('Map file : %s' % self._map_file)

        grouped_ws = self._run_name + '_group'
        GroupDetectors(InputWorkspace=self._raw_workspace,
                       OutputWorkspace=grouped_ws,
                       MapFile=self._map_file,
                       IgnoreGroupNumber=True,
                       Behaviour='Average')

        monitor_ws = self._run_name + '_mon'
        ExtractSingleSpectrum(InputWorkspace=self._raw_workspace,
                              OutputWorkspace=monitor_ws,
                              WorkspaceIndex=0)

        if self._use_mirror_mode:
            output_workspaces = self._run_mirror_mode(monitor_ws, grouped_ws)
        else:
            output_workspaces = self._run_non_mirror_mode(monitor_ws, grouped_ws)

        return output_workspaces


    def _run_non_mirror_mode(self, monitor_ws, grouped_ws):
        """
        Runs energy reduction with mirror mode.

        @param monitor_ws :: name of the monitor workspace
        @param grouped_ws :: name of workspace with the detectors grouped
        """
        logger.information('Mirror sense is OFF')
        self._calculate_energy(monitor_ws, grouped_ws, self._red_workspace)
        if self._calibration_workspace != '':
            Divide(LHSWorkspace=self._red_workspace,
                   RHSWorkspace=self._calibration_workspace + '_red',
                   OutputWorkspace=self._red_workspace)
        return [self._red_workspace]

    def _run_mirror_mode(self, monitor_ws, grouped_ws):
        """
        Runs energy reduction with mirror mode.

        @param monitor_ws :: name of the monitor workspace
        @param grouped_ws :: name of workspace with the detectors grouped
        """
        logger.information('Mirror sense is ON')

        x = mtd[grouped_ws].readX(0)  # energy array
        mid_point = int((len(x) - 1) / 2)

        #left half
        left_ws = self._run_name + '_left'
        left_mon_ws = left_ws + '_mon'
        left_temp_ws = '__left_temp_ws'
        CropWorkspace(InputWorkspace=grouped_ws,
                      OutputWorkspace=left_ws,
                      XMax=x[mid_point - 1])
        CropWorkspace(InputWorkspace=monitor_ws,
                      OutputWorkspace=left_mon_ws,
                      XMax=x[mid_point - 1])

        self._calculate_energy(left_mon_ws, left_ws, left_temp_ws)
        if self._calibration_workspace != '':
            Divide(LHSWorkspace=left_temp_ws,
                   RHSWorkspace=self._calibration_workspace + '_left',
                   OutputWorkspace=left_temp_ws)

        #right half
        right_ws = self._run_name + '_right'
        right_mon_ws = right_ws + '_mon'
        right_temp_ws = '__right_temp_ws'
        CropWorkspace(InputWorkspace=grouped_ws,
                      OutputWorkspace=right_ws,
                      Xmin=x[mid_point])
        CropWorkspace(InputWorkspace=monitor_ws,
                      OutputWorkspace=right_mon_ws,
                      Xmin=x[mid_point])

        self._calculate_energy(right_mon_ws, right_ws, right_temp_ws)
        if self._calibration_workspace != '':
            Divide(LHSWorkspace=right_temp_ws,
                   RHSWorkspace=self._calibration_workspace + '_right',
                   OutputWorkspace=right_temp_ws)
        number_histograms = mtd[left_temp_ws].getNumberHistograms()

        if self._shift_origin:
            index = self._indexOf(mtd[self._origin_workspace].getAxis(1), "left")
            left_mean = mtd[self._origin_workspace].readY(index)
            index = self._indexOf(mtd[self._origin_workspace].getAxis(1), "right")
            right_mean = mtd[self._origin_workspace].readY(index)

            left_spectrum = '__left_spectrum'
            right_spectrum = '__right_spectrum'
            CloneWorkspace(InputWorkspace=left_temp_ws,
                           OutputWorkspace=self._red_left_workspace)
            CloneWorkspace(InputWorkspace=right_temp_ws,
                                    OutputWorkspace=self._red_right_workspace)

            for idx in range(number_histograms):
                ExtractSingleSpectrum(InputWorkspace=self._red_left_workspace,
                                      OutputWorkspace=left_spectrum,
                                      WorkspaceIndex=idx)
                x_shifted = mtd[left_spectrum].readX(0) - left_mean[idx]
                mtd[self._red_left_workspace].setX(idx, x_shifted)

                ExtractSingleSpectrum(InputWorkspace=self._red_right_workspace,
                                      OutputWorkspace=right_spectrum,
                                      WorkspaceIndex=idx)
                x_shifted = mtd[right_spectrum].readX(0) - right_mean[idx]
                mtd[self._red_right_workspace].setX(idx, x_shifted)

            RebinToWorkspace(WorkspaceToRebin=self._red_left_workspace,
                             WorkspaceToMatch=left_temp_ws,
                             OutputWorkspace=self._red_left_workspace)
            RebinToWorkspace(WorkspaceToRebin=self._red_right_workspace,
                             WorkspaceToMatch=left_temp_ws,
                             OutputWorkspace=self._red_right_workspace)


        else:
            RenameWorkspace(InputWorkspace=left_temp_ws,
                            OutputWorkspace=self._red_left_workspace)
            RenameWorkspace(InputWorkspace=right_temp_ws,
                            OutputWorkspace=self._red_right_workspace)

        #sum both workspaces together
        Plus(LHSWorkspace=self._red_left_workspace,
             RHSWorkspace=self._red_right_workspace,
             OutputWorkspace=self._red_workspace)
        Scale(InputWorkspace=self._red_workspace,
              OutputWorkspace=self._red_workspace,
              Factor=0.5, Operation='Multiply')

        DeleteWorkspace(monitor_ws)
#        DeleteWorkspace(grouped_ws)
        DeleteWorkspace(left_mon_ws)
        DeleteWorkspace(right_mon_ws)
#        DeleteWorkspace(left_temp_ws)
#        DeleteWorkspace(right_temp_ws)
        if self._shift_origin:
            DeleteWorkspace(left_spectrum)
            DeleteWorkspace(right_spectrum)

        return [self._red_left_workspace, self._red_right_workspace, self._red_workspace]


    def _calculate_energy(self, monitor_ws, grouped_ws, red_ws):
        """
        Convert the input run to energy transfer

        @param monitor_ws :: name of the monitor workspace to divide by
        @param grouped_ws :: name of workspace with the detectors grouped
        @param red_ws :: name to call the reduced workspace
        """
        x_range = self._monitor_range(monitor_ws)
        Scale(InputWorkspace=monitor_ws,
              OutputWorkspace=monitor_ws,
              Factor=0.001,
              Operation='Multiply')

        CropWorkspace(InputWorkspace=monitor_ws,
                      OutputWorkspace=monitor_ws,
                      Xmin=x_range[0],
                      XMax=x_range[1])
        ScaleX(InputWorkspace=monitor_ws,
               OutputWorkspace=monitor_ws,
               Factor=-x_range[0],
               Operation='Add')

        CropWorkspace(InputWorkspace=grouped_ws,
                      OutputWorkspace=grouped_ws,
                      Xmin=x_range[0],
                      XMax=x_range[1])
        ScaleX(InputWorkspace=grouped_ws,
               OutputWorkspace=grouped_ws,
               Factor=-x_range[0],
               Operation='Add')

        Divide(LHSWorkspace=grouped_ws,
               RHSWorkspace=monitor_ws,
               OutputWorkspace=grouped_ws)
        formula = self._energy_range(grouped_ws)
        ConvertAxisByFormula(InputWorkspace=grouped_ws,
                             OutputWorkspace=red_ws,
                             Axis='X',
                             Formula=formula)

        red_ws_p = mtd[red_ws]
        red_ws_p.getAxis(0).setUnit('DeltaE')

        xnew = red_ws_p.readX(0)  # energy array
        logger.information('Energy range : %f to %f' % (xnew[0], xnew[-1]))


    def _monitor_range(self, monitor_ws):
        """
        Get sensible values for the min and max cropping range

        @param monitor_ws :: name of the monitor workspace
        @return tuple containing the min and max x values in the range
        """
        x = mtd[monitor_ws].readX(0)  # energy array
        y = mtd[monitor_ws].readY(0)  # energy array
        imin = np.argmax(np.array(y[0:20]))
        nch = len(y)
        im = np.argmax(np.array(y[nch - 21:nch - 1]))
        imax = nch - 21 + im

        logger.information('Cropping range %f to %f' % (x[imin], x[imax]))

        return x[imin], x[imax]


    def _energy_range(self, ws):
        """
        Calculate the energy range for the workspace

        @param ws :: name of the workspace
        @return formula for convert axis by formula to convert to energy transfer
        """
        x = mtd[ws].readX(0)
        npt = len(x)
        imid = float(npt / 2 + 1)
        gRun = mtd[ws].getRun()
        wave = gRun.getLogData('wavelength').value
        logger.information('Wavelength : %s' % wave)
        if gRun.hasProperty('Doppler.maximum_delta_energy'):
            energy = gRun.getLogData('Doppler.maximum_delta_energy').value*1e-3  #max energy in meV
            logger.information('Doppler max energy : %s' % energy)
        elif gRun.hasProperty('Doppler.doppler_speed'):
            speed = gRun.getLogData('Doppler.doppler_speed').value
            amp = gRun.getLogData('Doppler.doppler_amplitude').value
            logger.information('Doppler speed : %s' % speed)
            logger.information('Doppler amplitude : %s' % amp)
            energy = 1.2992581918414711e-4 * speed * amp * 2.0 / wave  # max energy
        elif gRun.hasProperty('Doppler.doppler_freq'):
            speed = gRun.getLogData('Doppler.doppler_freq').value
            amp = gRun.getLogData('Doppler.doppler_amplitude').value
            logger.information('Doppler freq : %s' % freq)
            logger.information('Doppler amplitude : %s' % amp)
            energy = 1.2992581918414711e-4 * freq * amp * 2.0 / wave  # max energy

        dele = 2.0 * energy / npt
        formula = '(x-%f)*%f' % (imid, dele)

        return formula

    def _indexOf(self, text_axis, label):
        nvals = text_axis.length()
        for idx in range(nvals):
            if label == text_axis.label(idx):
                return idx
    # If we reach here we didn't find it
        raise LookupError("Label '%s' not found on text axis" % label)


# Register algorithm with Mantid
AlgorithmFactory.subscribe(IndirectILLReduction)
