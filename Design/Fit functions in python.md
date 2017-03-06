# Working with fit functions in python

Although fitting functions have some of the functionality exposed to python the use of it is very limited and functions are constructed via strings. Values of the optimised parameters get extracted from `TableWorkspace`s output from the Fit algorithm. Both function construction and extraction of the results are cumbersome and error prone. This document describes a design of a python fitting API aiming to overcome these problems. The main idea of the solution proposed here is to create and manipulate a C++ [`IFunction`](https://github.com/mantidproject/mantid/blob/master/Framework/API/inc/MantidAPI/IFunction.h) object from python directly via a thin wrapper python classes. `FitFunctionWrapper` will be the base class functionality common for all fit functions. Composite functions (`CompositeFunction`, `ProductFunction`, `Convolution`, `MultiDomainFunction`) will have their own wrappers inheriting from `FitFunctionWrapper`. If a fit function exibits a special behaviour a custom wrapper can be defined.

## Function construction

For each concrete function type (Gaussian, Lorentzian, etc) there should exist a corresponding python function in `simpleapi.fitfunctions` namespace with the same name automatically generated in a way similar to the algorithm functions. A function object is then constructed by calling such a function (constructor) and is an instance of `FitFunctionWrapper`. For example
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
The implementation must check each keyword argument if it's a parameter or an attribute by calling `IFunction::hasAttribute(name)`. All passed attributes must be set before setting parameters.

### Construction of composite functions

Composite functions can be created in a similar way, by calling a constructor. It should be able to accept the same types of arguments as a simple function but also it must have the `functions` keyword argument that takes a list of member functions. For example:
```
  c = CompositeFunction(functions=[Gaussian(PeakCentre=1), Gaussian(PeakCentre=2)])
```
Another way of setting member functions is via positional arguments of the condtructor:
```
  c = CompositeFunction(Gaussian(PeakCentre=1), Gaussian(PeakCentre=2))
```
Wrapper classes will override the `__add__()` method to allow construction of composite functions from a sum of member functions:
```
  c = LinearBackground() + Gaussian(PeakCentre=1) + Gaussian(PeakCentre=2)
```
`ProductFunction` can be constructed from a product of member functions by defining the `__mul__` method:
```
  p = ExpDecay() * UserFunction(Formula='sin(w*x)', w=1)
```

In both ways of constructing composites the functions passed as arguments shouldn't be used (attached) directly, they should be copied.

### Multi-domain functions

A [`MultiDomainFunction`](https://github.com/mantidproject/mantid/blob/master/Framework/API/inc/MantidAPI/MultiDomainFunction.h) is a kind of a `CompositeFunction` that can do calculations on multiple domains (e.g. multiple spectra) that are numbered and can be identified by *domain indices*. Each member function is applied to one or more domains and can have one or more domain indices associated with it. Therefore `MultiDomainFunction` needs a custom constructor to sets domain indices to its members.

The only type of mapping that has been used in Mantid is one-to-one: one function - one domain. 'Global' fitting is achieved by tying some of the parameters together. Here it is proposed to restrict (to start with) the python interface to this use case only.

So a construction of a `MultiDomainFunction` should be like this:
```
  md_fun = MultiDomainFunction(Gaussian(PeakCentre=1, Sigma=0.1), Gaussian(PeakCentre=1, Sigma=0.2), ..., global=['Height'])
```
Each function passed to the constructor will be applied to its own domain making the number of domains equal to the number of member functions. All `Height` parameters will be tied and therefore global and all the others will be local to each domain.

To implement the constructor the methods of C++ class `MultiDomainFunction` need to be exported to python. In particular the `setDomainIndex` method. Here is a (very simplified) way to implement the constructor:
```
class MultiDomainFunctionWrapper(CompositeFunctionWrapper):

    def __init__(self, *args, **kwargs):
        # Store a reference to the C++ instance of the functon
        self.func = FunctionFactory.createFunction('MultiDomainFunction')
        
        # Populate it with member functions
        for arg in args:
            # Each arg must be a wrapper holding a ref to its function instance
            self.func.add(arg.func)
        
        # Tie the global parameters
        self.tieAll(*kwargs['global'])
        
        # Set domain indices: 1-to-1
        for i in range(len(args)):
            self.setDomainIndex(i, i)

```

## Updating functions

### Getting and setting parameters and attributes

`FitFunctionWrapper` will implement the `__getitem__(self, name)` and `__setitem__(self, name, value)` methods to access parameters and attributes in a dictionary-like style (`name` is a string):
```
  sigma = gaussian['Sigma']
  
  comp_func['f1.A0'] = 0.5
```

Implement `__getattr__()` and `__setattr__()` to access parameters of non-composite functions through instance attributes with the same name as the parameter.
```
  bk.A0 = 1
```

### Managing members of composite functions

Wrappers for composite functions will implement `__getitem__(self, i)` method to access members of a composite function in a list-like style (`i` is an `int`):
```
  spectrum = LinearBackground() + Gaussian(PeakCentre=1) + Gaussian(PeakCentre=2)
  peak1 = spectrum[1]
  peak1['Sigma'] = 0.123
  spectrum[2] = Lorentzian(PeakCentre=2)
```
Composite wrappers will also define the `fn` attributes (where `n` is a number) for example: `c.f0`, `c.f1`, ... The following three lines will have the same effect:
```
  c.f1.f0.A0 = 2
  c[1][0]['A0'] = 2
  c['f1.f0.A0'] = 2
```
They will also define attributes with names equal to the names of the member functions + a suffix. The suffix is an int numbering repeating names. For example, members of function
```
  spectrum = LinearBackground() + Gaussian(PeakCentre=1) + Gaussian(PeakCentre=2)
```
can be refered to like this:
```
  spectrum.LinearBackground
  spectrum.Gaussian0
  spectrum.Gaussian1
```

The wrappers will override `__iadd__(self, func)` and `__delitem__(self, i)` (`i` is an `int`, `func` is a `FitFunctionWrapper`) to implement adding and deleting members via `+=` and `del` operators:
```
  spectrum += Lorentzian(PeakCentre=3)
  del spectrum[0]
```

Implement `__len__(self)` to return the number of member functions.
```
  n_peaks = len(spectrum)
```

Implement `__iter__` method to allow iteration over the members:
```
  for func in comp: 
    print(func)
```

### Setting ties

Ties are set with the `tie` method. Both keyword arguments and dictionaries of name/value pairs can be used as arguments.
```
  func.tie(A0=2.0)
  func.tie({'f1.A2': '2*f0.A1', 'f2.A2': '3*f0.A1 + 1'})
```

Tying to a constant value that a parameter currently has can also be done with the `fix` method.
```
  func.fix('A0')
  func.fix('f1.A2', 'f2.A2')
```

Ties are removed with the `untie` or `unfix` methods.
```
  func.unfix('f1.Sigma', 'f3.Sigma')
  func.untie('f1.Sigma', 'f3.Sigma')
```

Composite functions should be able to set ties on all members with a single call:
```
  c.tieAll('Sigma')
```
The above call should tie all `Sigma` parameters in the member functions. It is equivalent to calling
```
  c.tie({'f1.Sigma': 'f0.Sigma', 'f2.Sigma': 'f0.Sigma', 'f3.Sigma': 'f0.Sigma', ...})
```
Similarly a call to `fixAll` fixes all parameters with the given name to their current value.
```
  spectrum.fixAll('FWHM')
  spectrum.fixAll('f1.FWHM': 0.01)
```
Calling `fixAll()`/`unfixAll()` without arguments fixes/frees all parameters of a function.

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

Python function `Fit` should accept instances of `FitFunctionWrapper` as its `Function` argument. `Fit` doesn't modify the input function but the returned value has the output function with the fitted parameters.

## Function evaluation

`FitFunctionWrapper` class will implement `__call__(...)` method to evaluate the function. The method will be able to accept a variety of input types for its first positional argument:
 1. Workspace
 2. Numpy array
 3. List of numbers
 4. Single number
 
The output type is the same as that of the input. For example:
```
  g = Gaussian(Sigma=0.1, Height=1)
  y1 = g(0.2)
  y2 = g(2*g.Sigma)
  y_list = g([-2, -1, 0, 1, 2])
  out_ws = g(ws)
```

If the `__call__` method has the signature `__call__(self, x, *params)` then the function wrappers could be used directly with `scipy.optimize` fitting as the following example demonstrates:
```
import scipy.optimize

class Linear:
    
    def __init__(self):
        self.fun = FunctionFactory.createFunction('LinearBackground')
        
    def __call__(self, x, *params):
        for i in range(len(params)):
            self.fun.setParameter(i, params[i])
        y = x[:]
        ws = CreateWorkspace(x, y)
        out = EvaluateFunction(str(self.fun), ws, OutputWorkspace='out')
        return out.readY(1)
        
        
fun = Linear()
x = [1, 2, 3]
y = [3, 2, 1]
sigma = [0.1, 0.2, 0.3]
popt, pcov = scipy.optimize.curve_fit(fun, x, y, p0=[0, 0], sigma=sigma)
print popt
print fun(x)
```
The actual implementation of `__call__` will take into account any ties that are set on the parmeters.

## Plotting

Python function `plotFunction` will plot one or more fitting functions in MantidPlot. It will have the arguments:
 1. first positional argument - the function(s) to plot
 2. `workspace` - optional workspace on which x-values to evaluate the function
 3. `workspaceIndex` - optional index of a spectrum to get the x-values from
 4. `startX` - optional if `workspace` is given, mandatory otherwise. The start of the plot region.
 5. `endX` - optional if `workspace` is given, mandatory otherwise. The end of the plot region.

