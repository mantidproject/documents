# Working with fit functions in python

Although fitting functions have some of the functionality exposed to python the use of it is very limited and functions are constructed via strings. Values of the optimised parameters get extracted from `TableWorkspace`s output from the Fit algorithm. Both function construction and extraction of the results are cumbersome and error prone. This document describes a design of a python fitting API aiming to overcome these problems. The main idea of the solution proposed here is to create and manipulate a C++ [`IFunction`](https://github.com/mantidproject/mantid/blob/master/Framework/API/inc/MantidAPI/IFunction.h) object from python directly via a thin wrapper python class `FitFunctionWrapper`.

## Function construction

For each concrete function type (Gaussian, Lorentzian, etc) there should exist a corresponding python function with the same name automatically generated in a way similar to the algorithm functions. A function object is then constructed by calling such a function (constructor) and is an instance of `FitFunctionWrapper`. For example
```
  g = Gaussian()
```
A call without passing in any initialisation arguments should create a function with default parameters and attributes.
Initial values of parameters and attributes can be given via keyword arguments, for example
```
  p = Polynomial(attributes={'n': 3}, parameters={'A0': 1, 'A1': 2, 'A3': 3, 'A4': 4})
```
Parameter and attribute names can also be used as the keys:
```
  g = Gaussian(Height=1, Sigma=0.1)
  
  p = Polynomial(n=3, A0=1, A1=2, A3=3, A4=4)
```
The implementation must check each keyword argument if it's a parameter or an attribute by calling `IFunction::hasAttribute(name)`. All passed attributes must be set before setting parameters. There is need to be a provision for setting attributes in a particular order in case it is essential for a fitting function. This can be done for example by passing a list of name/value pairs (tuples or lists) to the `attributes` keyword argument.

### Construction of composite functions

Composite functions can be created in a similar way, by callig a constructor. It should be able to accept the same types of arguments as a simple function but also it must have the `functions` keyword argument that takes a list of member functions. For example:
```
  c = CompositeFunction(functions=[Gaussian(PeakCentre=1), Gaussian(PeakCentre=2)])
```
Another way of setting member functions is via positional arguments of the condtructor:
```
  c = CompositeFunction(Gaussian(PeakCentre=1), Gaussian(PeakCentre=2))
```
`FitFunctionWrapper` class will override the `__add__()` method to allow construction of composite functions from a sum of member functions:
```
  c = LinearBackground() + Gaussian(PeakCentre=1) + Gaussian(PeakCentre=2)
```
`ProductFunction` can be constructed from a product of member functions:
```
  p = ExpDecay() * UserFunction(Formula='sin(w*x)', w=1)
```

### Multi-domain functions

A [`MultiDomainFunction`](https://github.com/mantidproject/mantid/blob/master/Framework/API/inc/MantidAPI/MultiDomainFunction.h) needs a custom constructor which sets domain indices to its members.

## Updating functions

### Getting and setting parameters and attributes

`FitFunctionWrapper` will implement `__getitem__(self, name)` and `__setitem__(self, name, value)` methods to access parameters and attributes in a dictionary-like style (`name` is a string):
```
  sigma = gaussian['Sigma']
  
  comp_func['f1.A0'] = 0.5
```

Parameters of members of composite functions can be accessed via their wrapper objects. For example:
```
  bk = LinearBackground()
  peak = Lorentzian()
  spectrum = bk + peak
  ...
  bk['A0'] = 1
  peak['FWHM'] = 0.123
  assert spectrum['f0.A0'] == 1
  assert spectrum['f1.FWHM'] == 0.123
```
*Question: what to do if a function becomes a member of two or more composite functions?*
  1. *Ignore and let the user be responsible for it*
  2. *Set a flag on `FtFunctionWrapper` and prevent subsequent attempts to add it*

### Managing members of composite functions

`FitFunctionWrapper` will implement `__getitem__(self, i)` and `__setitem__(self, i, value)` methods to access members of a composite function in a list-like style (`i` is an `int`):
```
  spectrum = LinearBackground() + Gaussian(PeakCentre=1) + Gaussian(PeakCentre=2)
  peak1 = spectrum[1]
  peak1['Sigma'] = 0.123
  spectrum[2] = Lorentzian(PeakCentre=2)
```

`FitFunctionWrapper` will override `__iadd__(self, func)` and `__delitem__(self, i)` (`i` is an `int`, `func` is a `FitFunctionWrapper`) to implement adding and deleting members via `+=` and `del` operators:
```
  spectrum += Lorentzian(PeakCentre=3)
  del spectrum[0]
```

Implement `__len__(self)` to return the number of member functions.
```
  n_peaks = len(spectrum)
```

### Setting ties

Ties are set with the `tie` method. Both keyword arguments and dictionaries of name/value pairs can be used as arguments.
```
  func.tie(A0=2.0)
  func.tie({'f1.A2': '2*f0.A1', 'f2.A2': '3*f0.A1 + 1'})
```

Tying to a constant can also be done with the `fix` method.
```
  func.fix('A0')             # Fix to the current value
  func.fix(A0=2.0, A1=1.0)   # Fix to new values
  func.fix({'f1.A2': 1.0, 'f2.A2': 2.0})
```

Ties are removed with the `removeTie` or `free` methods.
```
  func.free('f1.Sigma', 'f3.Sigma')
  func.removeTie('f1.Sigma', 'f3.Sigma')
```

Composite functions should be able to set ties on all members with a single call:
```
  c.tieAll('Sigma')
```
The above call should tie all `Sigma` parameters in the member functions. It is equivalent to calling
```
  c.tie({'f1.Sigma': 'f0.Sigma', 'f2.Sigma': 'f0.Sigma', 'f3.Sigma': 'f0.Sigma', ...})
```
Similarly a call to `fixAll` fixes all parameters with the given name to their current value or to a new value if provided.
```
  spectrum.fixAll('FWHM')
  spectrum.fixAll(FWHM=0.01)
  spectrum.fixAll({'f1.FWHM': 0.01})
```
Calling `fixAll()`/`freeAll()` without arguments fixes/frees all parameters of a function.

### Setting constraints

Constraints are set with `constraints` method passing constraints as strings:
```
  g.constraints('-1 < PeakCentre < 1', 'Sigma > 0')
```

For composite functions constraints can be set both through the composite function and its members:
```
  c = LinearBackground() + Gaussian(PeakCentre=1) + Gaussian(PeakCentre=2)
  c.constraints('f1.Sigma > 0')
  c[2].constraints('0 < Sigma < 1')
```

Composite functions should be able to set constraints on all members with a single call:
```
  c.constrainAll('Height > 1', 'Sigma > 0')
```
This should constrain the named parameters in all members that have them. Members that don't have these parameters should be skipped.

## Fitting

Python function `Fit` should accept instances of `FitFunctionWrapper` as its `Function` argument. `Fit` does't modify the input function but the returned value has the output function with the fitted parameters. Instead of a tuple `Fit` will return an instance of class `FitOutput` that contains all outputs from the algorithm and gives access to them both via the index operator and python read-only properties:
```
  res = Fit(func, ws)
  output_func = res.function
  chi2 = res.chiSquared
  ...
```

## Function evaluation

`FitFunctionWrapper` class will implement `__call__(...)` method to evaluate the function. The method will be able to accept a variety of input types:
 1. Workspace
 2. Numpy array
 3. List of numbers
 4. Single number
 
The output type is the same as that of the input.

## Plotting

Python function `plotFunction` will plot one or more fitting functions in MantidPlot. It will have the arguments:
 1. first positional argument - the function(s) to plot
 2. `workspace` - optional workspace on which x-values to evaluate the function
 3. `workspaceIndex` - optional index of a spectrum to get the x-values from
 4. `startX` - optional if `workspace` is given, mandatory otherwise. The start of the plot region.
 5. `endX` - optional if `workspace` is given, mandatory otherwise. The end of the plot region.

