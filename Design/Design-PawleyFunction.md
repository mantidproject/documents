# Introducing a Pawley fit function

## Motivation

There are serveral possible ways to extract lattice parameters from powder diffraction data. One of them is the Pawley-method, where analytical peak profiles are generated at the positions that result from the unit cell parameters and the Miller indices hkl of each peak. This means that unit cell parameters are fitted using the whole powder diffraction diagram. Other peak profile parameters are not interpreted. This document describes how Pawley-fitting can be integrated into the existing Mantid function fitting framework.

## Requirements

There are some requirements that the Pawley-function has to meet:
  * Possibility to assign an arbitrary number of HKLs, for each of which a profile function will be generated
  * Use IPeakFunction for calculating peak profiles - this way many profiles are available and new ones can be added independently.
  * Must expose unit cell parameters a, b, c, alpha, beta, gamma, taking into account restrictions arising from the crystal system.
  * Must expose all profile parameters of the member peak-function except the location. Location should be hidden because changing this parameter for a single peak does not have any meaning, since the position is calculated.
  * Must set the location of the peak functions according to the assigned unit cell and HKLs.
  * Specifically for POLDI it would be useful if the whole function could be shifted by an offset (this is what the chopper slits at POLDI do). This could be implemented either as a parameter or maybe better as an attribute, since it probably should not be optimized (even though it could be useful for calibration of zero-shift).
  * The unit of the workspace should be taken into account so that the function is not limited to d, but can also be used in Q or 2theta. That means that after calculating d from HKL and the unit cell, the value has to be converted to the unit of the spectrum.


## Implementation possibilities

### 1. Inheriting from CompositeFunction

One possibility is to have PawleyFunction inherit from CompositeFunction. In that case, the function has to declare the unit cell parameters and also modify the way member function parameters are exposed. This is mainly for hiding the location parameter. One drawback of this approach is that it violates Liskov's substitution principle.

### 2. Implementing IFunction1D and having a CompositeFunction-member

This approach is very similar to the first one, except that composition makes it clear that the PawleyFunction is not actually a CompositeFunction and hence does not offer all of its functionality. The function would implement IFunction1D and ParamFunction. Upon construction it should be possible to tell the function which crystal system is used to constrain the available lattice parameters. Furthermore, the name of the profile function (must be an IPeakFunction) should be given. The last required information is a list of HKLs, which will be used to generate the appropriate number of member function that are then put into the internal CompositeFunction. After this, the parameters of the CompositeFunction (which are all profile parameters) are exposed as parameters of the PawleyFunction.

In order to exclude the location parameter, IPeakFunction has to be extended slightly so that it is possible to obtain the names of the location, fwhm and height parameters. Since there may not be a 1:1-mapping for all IPeakFunction-implementations the default implementation of this part of the interface should throw a NotImplemented-exception.


## Possible generalization

Instead of supplying the crystal system, one could supply a space group, which determines the crystal system as well (at least once tickets #10305 and probably #11006 are done). In that way LeBail-fit could possibly also profit from this function by imposing relative intensity constraints based on reflection multiplicity, which depends on the point group. Also, using the point group, the list of HKLs could be "sanitized" in the sense that there would be only symmetry independent reflections left.


## Open questions

An unsolved problem is how the list of HKLs should be supplied to the function. There could be the option to load HKLs from a workspace (PeaksWorkspace, Table?). Probably it would also be beneficial to have starting parameters for the peak profiles, so those would have to be supplied as well. As already discussed, PeaksWorkspace does not work very well for powder diffraction peaks (please correct this if you disagree). Advice on this issue is very welcome.


## Actions

A ticket has been created ([#11043](http://trac.mantidproject.org/mantid/ticket/11043)) and I will make an example implementation for option 2, leaving the HKL-setting open for now. Therefore it will be possible to use the function in conjunction with the Fit-algorithm programatically, but probably not through the GUI.

# Update March 20, 2015

## Implementation

The function has been implemented in ticket [#11043](http://trac.mantidproject.org/mantid/ticket/11043). The approach differs a little bit from the description above, a UML diagram is attached to the ticket in PDF format (http://trac.mantidproject.org/mantid/attachment/ticket/11043/PawleyFunctionDiagram.pdf).

### PawleyParameterFunction

The first element of the Pawley fit is PawleyParameterFunction. It is not really a function of its own, it is just there to handle the cell parameters based on the crystal system, which can be set as an attribute (CrystalSystem). If "Cubic" is selected, the function has only "a" as parameter, adding more and more until "Triclinic" provides all 6 parameters. Furthermore, the function has another attribute "ProfileFunction", which is used to store the name of the profile function that should be used for calculating the peaks later on. It creates the peak function and extracts the name of the parameter that is associated to the center parameter - this is required later for fixing those parameters.

The class implements ParamFunction and has empty implementations of function and functionDeriv.

Each time the crystal system is set, the number of parameters changes.

### PawleyFunction

PawleyFunction implements FunctionParameterDecorator and it decorates a CompositeFunction that is composed of two functions. The first one is PawleyParameterFunction, while the second is again a CompositeFunction which is there to store the IPeakFunction-objects. Because PawleyFunction is derived from FunctionParameterDecorator, all parameters of the decorated function are exposed. Because it's a CompositeFunction, the parameters of the contained functions are exposed - in this case the cell parameters and the parameters of the peaks stored in the "inner" CompositeFunction.

Peaks can be added in a very general way, there is a method addPeak that takes a V3D for HKL, fwhm and height. When this method is called, an IPeakFunction of the type stored in PawleyParameterFunction is created, the parameters fwhm and height are set as starting values and the center-parameter is fixed, after which the object is put into the inner CompositeFunction. In addition, the V3D is stored. The exposed parameters of PawleyFunction are then updated. This process is repeated for as many peaks as there are.

For calculating the function value, the PawleyFunction gets a UnitCell-object from PawleyParameterFunction, which is generated from the function parameters. Then it iterates through all IPeakFunctions that are stored in the inner composite, uses the UnitCell-object and the HKL to calculate d and tries to convert it to the unit of the supplied MatrixWorkspace, if there is any (otherwise, d is kept). This value is then assigned to the center parameter of the IPeakFunction that is associated to the HKL.

At this point, the function value is nothing more than the function value of the inner CompositeFunction.

### PawleyFit

Because the function requires some setup (see "Open questions" above), especially for the reflections that are used, an algorithm has been added (similar to LeBailFit). Documentation including a usage example has been written, it explains how to provide peak information and so on.

## Limitations

I tried to include support for different units, but I've limited it to units that can be converted from d using quick conversion and limited my tests to d and Q. Maybe someone with more experience in that area could extend that part later on.

Another thing I'm not 100% satisfied with is that initial cell parameters have to be provided and they have to be quite close to the actual ones in order to result in a reasonable refinement. I've thought about this problem and I think I would like to introduce a new domain that uses HKLs instead of double values and a function that calculates d for a given HKL. It would use the data provided in the peak table and perform a preliminary fit of the lattice parameters using only the reflection positions. That should give better starting parameters and it would not require the user to specify a cell (the information is in the peak tableworkspace anyway in the form of HKL/d-pairs).

## Further actions

For POLDI (which this was intended for originally) another wrapper has to be added for making it compatible with the MultiDomainFunction interface and the different weighting scheme used at POLDI. This will be handled in another ticket.