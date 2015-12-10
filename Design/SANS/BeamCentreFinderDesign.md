# Design Document for Beam Centre Finder

### Current issue
Currently the Beam Centre Finder (*BCF*) is heavily tied up with the ISIS instruments and the ReductionSingleton().
ANSTO are looking currently for similar functionality but since their reduction workflow is not based on the
ReductionSingleton() and they don't make use of the instrument class they cannot use the BCF directly. 
This document lines out the required changes to make the BCF useable in a more general context which could 
also be beneficial when moving away from the current Reduction-Step approach.

### Proposed solution
In general terms we want to hide any solution-specific details in the BCF. Currently there is already a layer of 
abstration which hides the instrument specific details, e.g. LARMOR uses an instrument rotation instead of a translation.
A common generic interface should allow for the current implementation on the ISIS side as well as other 
implementations to make use of the Beam Centre Finder logic.

### Components which require a workover
There are several parts which need to be considered

* Bare calls to the ReductionSingleton, eg ReductionSingleton().inst.cen_find_step
* The CentrePositioner which is responsible to provide new positions after each iteration. 
  This abstracts away differences in the way instruments handle displacements(translation or rotation) 
  and also contains takes into left/rigth or up/down or both are desired for BCF operation. Note that the 
  ReductionSingleton() is injected into the CentrePositioner.
* The BeamCenterLogger needs to report on the search operation. It displays coordinates mainly. Note that 
  since we are dealing with m in the logic and mm in the output this is being considered here. Similarly, it 
  handles degree for rotations. It also takes the reducer as an input. Note that the ReductionSingleton() is 
  injected into the BeamCenterLogger.
* CentreFinder is where the reduction takes place and where the residuals are calculated which are the quanitity
  we want to minimize. The CentreFinder itself contains bare references to the ReductionSingleton() itself.

### Things which can be reused with little effort
* The CentrePositioner and the underlying factories need to be extended to detect when we want to use ANSTO.
  Then we should switch to a XY-instance for the PositionProvider. This means we have to change the input slightly
  to take something more general than a reducer and base our factory decision on this more general input. Once it
  has decided for an ISIS instruement, we can make use of the current implementation.
* The Beam Centre Logger should be injected and completly replaced by an Ansto implementation. We log into the ISIS
  SANS GUI currently.

### Things which need to be redesigned

An abstract base class which can provide a more general interface could look like this
```python
class SANSBeamCentreFinderReduction(abc):
   ...

   @abstractmethod
   def initialize(xstart, ystart)
   '''
   @returns beam coords, steps 
   '''

   @abstractmethod
   def updateInternalCoordinates(coord1, coord2)
   '''
   An update step before to be called before we seek the centre
   '''

   @abstractmethod
   def applyLimits(rlow, rupp)
   '''
   Applies the limits and needs to be done after a Seek step.
   '''


   @abstractmethod
   def getSeekCentreReductionWrapper(rlow, rupp)
   '''
   @returns the wrapper for the appropriate reduction workflow, 
            which itself is an abc
   '''
```

``` python
class SANSSeekCentreReduction(abc):
   ...

   @abstractmethod
   def move(sign_policy, coord1, coord2)
   '''
   Moves the instrument in the workspace. ISIS will leave this as is
   ANSTO needs to think what the right way of moving is
   '''

   @abstractmethod
   def move(sign_policy, coord1, coord2)
   '''
   Moves the instrument in the workspace. ISIS will leave this as is
   ANSTO needs to think what the right way of moving is.
   '''


   @abstractmethod
   def getReducedSlices(workspace, ??can_workspace)
   '''
   This takes in a the workspace performs a reduction and provides four slices for UP/DOWN LEF/RIGHT
   @returns 4 1D, sliced workspaces
   '''
   
   @abstractmethod
   def getReducedSlices(workspace, ??can_workspace)
   '''
   This takes in a the workspace performs a reduction and provides four slices for UP/DOWN LEF/RIGHT
   @returns 4 1D, sliced workspaces
   '''


   @abstractmethod
   def ceanUpSlice(workspace)
   '''
   Removes the EndNans from teh workspace
   '''



```


### Things to clarify and potential difficulties
*  
