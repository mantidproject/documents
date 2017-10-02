
~~~~
  class AnyAlgorithm(PythonAlgorithm):
  ...
    ws = AnyOtherAlgorithm(......, StoreInADS=False)
  ...
~~~~

instead of

~~~~
  class AnyAlgorithm(PythonAlgorithm):
  ...
    self.createChildAlgorithm(AnyOtherAlgorithm)
    self.initialize()
    self.setProperty(...)
    ...
    self.execute()
    ws = self.getProperty(...)
  ...
~~~~
