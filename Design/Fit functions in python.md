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
