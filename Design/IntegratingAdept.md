Integrating adept into Mantid
=============================

As described in a previously uploaded [document](https://github.com/mantidproject/documents/blob/master/Design/Autodiff.md), [adept](http://www.met.rdg.ac.uk/clouds/adept/) is a library for automatic differentiation, which can be an alternative to numeric derivatives in some cases. Ticket [#9782](http://trac.mantidproject.org/mantid/ticket/9782) was created for the integration of adept into Mantid. This document summarizes the results from this ticket and contains suggestions and questions related to finalization of the integration process.

1. Cross platform compatibility
-------------------------------
adept is distributed as source code, but the most recent version (1.0 as of November 2014) only works on Linux, furthermore the build script only generates a static library. The first goals were to find out whether it's possible to compile adept as a shared library and also on all platforms that Mantid supports. It turns out that both tasks are possible, but with some modifications to the library. Since we only need the library itself and none of the other things the original source archive contains, a fork was created and uploaded to [github](https://github.com/MichaelWedel/adept-fork).

In this fork, the following things were changed:

  - Build system was changed from a single Makefile to a CMake-based solution
  - Instead of a static library, a shared library is built
  - define-directives for a usable DLL were added/changed
  - A CMake find module for adept was added
  - Packaging scripts for deb and rpm packages were added
  
The shared library builds under Linux, Windows and Mac OS X.

2. Performance
--------------
Performance was compared for three different profile functions that are commonly used for modeling diffraction line profiles, Gaussian, Lorentzian and Pearson-VII. To this end, all three functions were implemented to use three different methods for calculating derivatives: Hand-coded, numerical and automatic.

Reference data for function values and all partial derivatives were calculated using Matlab's symbolic toolbox with subsequent conversion to double precision numbers on a domain of 200 points. Additionally, function values with added noise were produced in this way for testing fitting behavior.

A test algorithm (`CurveFitting::AutoDiffTestAlg`) was implemented that performs these steps:

  - Load reference data from a NeXuS-file (attached to ticket)
  - Create function with selected differentiation method according to algorithm parameter
  - Perform fit of function parameters on noisy data
  - Call IFunction::function 10000 times to time execution
  - Call IFunction::functionDeriv 10000 times

## 2.1. Execution times
Relative execution times for function calculation (hand-coded : numerical : automatic):

  - Gaussian: 1.0 : 1.0 : 1.35
  - Lorentzian: 1.0 : 1.0 : 3.36
  - Pearson-VII: 1.0 : 1.0 : 1.09

And Jacobian:

  - Gaussian: 1.0 : 2.80 : 1.98
  - Lorentzian: 1.0 : 1.93 : 5.25
  - Pearson-VII: 1.0 : 2.23 : 1.07
  
Hand-coded derivatives are fastest in all cases. Whether numerical or automatic differentiation is faster depends on the function. For numerical derivatives, IFunction::function needs to be called `nParam + 1` times, while for automatic derivatives there is always 1 call to IFunction::function, followed by the cost for the forward Jacobian calculation.

Automatic derivatives are faster than numerical derivatives only if the following relation holds:

```
    t_fnum * (nParam + 1) > t_fauto + t_Jacobian
```

Both `t_fauto` and `t_Jacobian` depend on the number and type of statements in the function as all statements are recorded and have different contributions to the Jacobian in the end.

## 2.2. Accuracy of derivatives
The test algorithm also compares the values of the partial derivatives at each point of the domain with the reference data.

Here, the derivatives obtained from automatic differentiation show the advantage of giving exactly the same results as hand-coded derivatives, while numerical derivatives can deviate due to the well known problems with rounding and cutoff errors.

## 2.3. Conclusion
The relative performance of automatic and numerical derivatives seems to depend greatly on the nature of the chosen function. For cases where derivatives need to be as precise as possible or equal to hand-coded derivatives, automatic differentiation offers a viable alternative, combining precision of hand-coded derivatives, ease of implementation like numerical derivatives as well as comparable execution times.


3. Open questions
-----------------

There are some open questions left that need to be addressed in order to finish the integration of automatic derivatives into Mantid:

  - The library needs to be shipped with Mantid, similar to other dependencies, such as paraview. What is the best way to take care of that? Should there be a repository which is similar to mantidproject/paraview-build? Is there a process which builds Linux packages automatically?
  - The license of adept is GPLv3. Is this compatible with Mantid or are there any licensing concerns about shipping the library together with the program?
  - For finishing [#9782](http://trac.mantidproject.org/mantid/ticket/9782), adept needs to be installed on the build servers. What is the procedure for this?
  - The test algorithm and test implementations of the different functions need to be removed. Is there a good way of keeping it somewhere?
  
Questions that may be addressed in the future:

  - The way adept uses the recording stack for statements (an "active instance" is stored in a static variable of adept::stack), it is not possible to build this thread safe on Windows. On Linux, the static variable is declared "thread local", so each thread can have its own active stack. As far as I found out, in a DLL, the __declspec-directives for exporting symbols and thread local behavior are mutually exclusive. The author of adept mentioned in an e-mail that they are working on solving this problem, so this limitation may disappear in a future version.
  
  