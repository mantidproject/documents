from mantid.kernel import *
from mantid.api import *
 
class LoadInEnergy(PythonAlgorithm):
  
  def PyInit(self):
      self.declareProperty(FileProperty("Filename", "", FileAction.Load))
      self.declareProperty(WorkspaceProperty("OutputWorkspace", "", Direction.Output))
      
  def PyExec(self):
      filename = self.getProperty("Filename").value
      from mantid.simpleapi import Load
 
      # lifted from script
      _tmp = Load(Filename=filename)
      _tmp = _tmp.convertUnits(_tmp,Target="Energy")
 
      self.setProperty("OutputWorkspace",_tmp)
      _tmp.delete() # Remove temporary reference from MantidPlot view
      
# Tell mantid about it
AlgorithmFactory.subscribe(LoadInEnergy)