class: center, middle

# Data Processor Algorithms

What does it give me for free?

---

## Quick review of Algorithm

```python
def PyInit(self):
    # bunch of inconsistently named properties
    # mostly strings that are parsed in the PyExec

def PyExec(self):
    # as long of a function as you can imagine
```

---

## Did you know?

Grouping properties in the GUI

```python
def PyInit(self):
    self.declareProperty(MatrixWorkspaceProperty('InputWorkspace', '',
                                                 Direction.Input),\
                         doc="")
    self.declareProperty(FileProperty(name='InputFile',defaultValue='',
                                      action=FileAction.OptionalLoad,
				      extensions = ['_event.nxs']),
                         doc='')
    grp1 = 'Fancy Label'
    self.setPropertyGroup('InputWorkspace', grp1)
    self.setPropertyGroup('InputFile', grp1)
```

---

## Did you know?

Cross checking properties

```python
def validateInputs(self):
    issues = dict()
    if (not self.getProperty('InputWorkspace').isDefault()) \
        and (not self.getProperty('InputFile').isDefault()):

	issues['InputWorkspace'] = 'cannot set with "InputFile"'
	issues['InputFile'] = 'cannot set with "InputWorkspace"'

    return issues
```

...which runs before `PyExec`

---

## What is a [DataProcessorAlgorithm](http://docs.mantidproject.org/v3.5.1/api/python/mantid/api/DataProcessorAlgorithm.html)?
