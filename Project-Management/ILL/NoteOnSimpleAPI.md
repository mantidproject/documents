
'''
  class AnyAlgo(PythonAlgorithm):
  ...
    ws = CreateSampleWorkspace(......, StoreInADS=False)
  ...
'''

instead of

'''
  class AnyAlgo(PythonAlgorithm):
  ...
    self.createChildAlgorithm(CreateSampleWorkspace)
    self.initialize()
    self.setProperty(...)
    ...
    self.execute()
    ws = self.getProperty(...)
  ...
'''
