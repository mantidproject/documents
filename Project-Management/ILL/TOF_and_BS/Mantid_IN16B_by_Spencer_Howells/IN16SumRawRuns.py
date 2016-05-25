#pylint: disable=no-init
from mantid.simpleapi import *
from mantid.kernel import Direction
from mantid.api import (DataProcessorAlgorithm, AlgorithmFactory, MatrixWorkspaceProperty)
from mantid import config, logger, mtd
import os.path

class IN16SumRawRuns(DataProcessorAlgorithm):

    _runs = []
    _output_ws = None


    def category(self):
        return 'Workflow\\MIDAS;PythonAlgorithms;Inelastic'


    def summary(self):
        return 'Sum a selection of raw files.'


    def PyInit(self):
        self.declareProperty(name='Runs', defaultValue='',
                             doc='List of runnumbers, comma seperated')

        self.declareProperty(MatrixWorkspaceProperty("OutputWorkspace", "",
                                                     direction=Direction.Output),
                             doc="Name for the output workspace created.")

    def PyExec(self):
        workdir = config['defaultsave.directory']
        runs = self.getProperty('Runs').value
        output_ws = self.getPropertyValue('OutputWorkspace')

        values = runs.split(',')
        numb_runs = len(values)
        logger.information('Number of runs : %i' % numb_runs)

        for idx in range(numb_runs):
            logger.information('File %i is %s ' % (idx + 1, values[idx]))
            path = os.path.join(workdir, values[idx] + '.nxs')
            LoadILLIndirect(FileName=path,
                            OutputWorkspace='__raw')
            if idx == 0:
                CloneWorkspace(InputWorkspace='__raw',
                               OutputWorkspace=output_ws)
            else:
                Plus(LHSWorkspace=output_ws,
                     RHSWorkspace='__raw',
                     OutputWorkspace=output_ws)
                DeleteWorkspace('__raw')
        logger.information('Output workspace : %s' % output_ws)

# Register algorithm with Mantid
AlgorithmFactory.subscribe(IN16SumRawRuns)
