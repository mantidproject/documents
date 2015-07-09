
Introduction
============

This document describes the design of a new type of workspaces
suitable to store and process stacks of images. While that is in
principle the motivation for this design, equivalent data structures
may be useful in diferent contexts, so additional aspects may be
introduced as this document evolves.

The basic need is to have an efficient and simple representation of
stacks of images (with 3 or more dimensions) as for example image
processing tools like ImageJ (http://imagej.nih.gov/ij/) or
tomographic reconstruction tools like tomopy
(https://github.com/tomopy/tomopy/) use.

Objectives
==========

This design is specifically motivated by the new instrument IMAT which
is expected to produce large collections of images. A new type of
workspace should be defined that:

* Holds stacks of images coming from neutron imaging experiments.

* Can be used as a convenient and efficient data structure to
  interoperate with third party tools, visualize stacks of images, and
  apply image processing algorithms.

This will require the introduction of a new type of multidmensional
(MD) workspace, which should draw from or share as much as possible
with IMDHistoWorkspace (for example, taking advantage of the
n-dimensional iterators).

The immediate uses that should be enabled by introducing this new type
of workspace:

* Visualize stacks of images for simple, GUI-driven pre-processing
  steps (selection of subsets of images, clipping, specific types of
  normalization, etc.). This is normally required before using third
  party tomographic reconstruction tools.

* Load stacks of images and/or volumes into the VSI/ParaView

* Easy prototyping and integration of algorithms to fulfill tasks that
  will be needed to pre-/post-process stacks of images and data
  volumes produced by tomographic reconstruction. This includes for
  example simple algebraic operations on the stacks, applied on a
  per-image basis.

As a side effect, a particular case of this 'stack of images'
workspace should be a good representation for images such as those
produced by the IMAT instrument or calibration images from different
instruments.

Requirements
============

Here is a (potentially growing) list of requirements that should be
kept in mind for the design. Their implemenation could be iterative.

* Efficient, raw storage of data
* Avoid "overheads" of workspace types like Workspace2D: no errors, no
  doubles, etc. But ideally these should still be supported
  optionally.
* It should be possible to represent multiple dimensions, not just
  flat stacks of 2D images.  Typical dimensions can include X and Y
  (2D image), angle, energy level, time, and potentially more
  (experiment conditions, etc.).
* Python interface for scripting, with numpy array support. 
* Support for types like 8 and 16 bits integers, etc.
* File-backed storage / lazy loading
* Contiguous memory blocks are convenient but, equally, deques and
  other sparse structures could be useful.
* Terminology can be an issue when considering disparate applications
  and contexts.
* Compression option.
* Useable in different contexts: pre/processing of individual images
  and stacks of them, as well as visualization.
* Easy interoperability. For tomography users will resort to a variety
  of tools depending on their objectives and background. Loaders and
  savers will be needed, and these should be efficient.

Current hierarchy of MD workspaces at a glimpse
===============================================

```
Kernel::DataItem
  ^
  |
API::Workspace   API::MDGeometry
  ^                   ^
  |            -------|
  |            |
  |            |
  |            |
API::IMDWorkspace  [Note: it has methods getMask(), getError(), etc. that SOI does not need or want]
  ^
  |
API::IMDHistoWorkspace
  ^
  |
DataObjects::MDHistoWorkspace   [Note: provides DataObjects::MDHistoWorkspaceIterator, see e.g. createIterator()]
```

The class diagram of API::MDGeometry is available from:
http://doxygen.mantidproject.org/nightly/dc/d73/classMantid_1_1API_1_1MDGeometry.html

The class diagram of API::IMDHistoWorkspace is available from:
http://doxygen.mantidproject.org/nightly/d4/da9/classMantid_1_1API_1_1IMDHistoWorkspace.html

For the MatrixWorkspace class (the non-MD alternative hierarchy) the diagram is at:
http://doxygen.mantidproject.org/nightly/d8/d57/classMantid_1_1API_1_1MatrixWorkspace.html

Other relevant interfaces and classes are:
* Geometry::IMDDimension
* API::ExperimentInfo

Design alternatives
===================

There are several general features of workspaces (or some types of
workspaces) that StackOfImagesWorkspace should have. These include:
basic information such as name, comment, memory, but also instrument
and experiment information, and history.

Individual images are definitely regular grids. And stacks of them,
even if along multiple dimensions (for example dimension 3: multiple
projection angles, dimension 4: muliple energy levels, dimension 5:
multiple re-runs over time) are also treated without MD-ish operations
such as (re-)binning, event/histograms, etc. In any case a dimension
can be collapsed by simple operations such as for example a sum (or
average) image for all energy levels.

Functionality that SOI needs or wishes to have and where to get it from:

- Instrument and experiment information. Two alternatives:
  API::ExperimentInfo and API::MultipleExperimentInfos.

- Workspace/algorithm history: included in API::Workspace.

examples: MDHistoWorkspace::compact()

(Obvious) points that are highly certain and are a solid starting point:

- StackOfImagesWorkspace should inherit from Workspace. This also
  implies that it derives from DataItem which should be enough to
  guarantee that SOI workspaces can be in the Analysis Data Service
  and that Mantid algorithms can be run on them.

- No point to use MatrixWorkspace interface and functionality as SOI
  do not have spectra, (X, Y, Error). Also, do not get confused by the
  MantidImage type and related methods in API::MatrixWorkspace. We are
  not using that image type here.

- In a similar way as MatrixWorkspace has dataX() and dataY() which
  return a MantidVec reference, and readX() and readY() which return
  const MantidVec references, SOI should have data() and roData()
  methods.

- StackOfImagesWorkspace should also inherit from ExperimentInfo or
  MultipleExperimentsInfos, and the second seems a better option for
  complicated stacks of images.

- Geometry::IMDDimension: should be usable as it is.

- API::MDGeometry (which uses IMDDimension): the IMDDimensions related
functionality is relevant, but this class also has (Q) transformations
and origin coordinates related stuff that does not seem to make sense
for SOI. It may make sense to define a MDGeometryBase class (where I'd
like to find a more specific name for *Base*) which would have roughly
the first few methods of MDGeometry, excluding aspects like "Q", and
would become its base/parent class.

Approach 1: try to get as much as possible from traditional (I)MD classes
-------------------------------------------------------------------------

This assumes that in the current hierarchy of MD classes all the
functionality, methods and members are placed exactly where they are
needed, never higher than strictly needed.

If we want to integrate this new workspace type in the IMD/MD classes
hierarchy, many issues arise when trying to find a position and proper
interaction between *StackOfImagesWorkspace* (SOI) and other (MD)
workspaces. A basic version of StackOfImages would relate to other
classes and look like this:

Kernel::DataItem
  ^
  |
Workspace     MDGeometryBase
  ^            ^
  |            |
  |            |
  |            |
  |            |
IMDWorkspaceStripped    [Note: (without getMask(), getError(), etc., without normalisation)]
  ^
  |
  |
  |-------------------------------   MDGeometry
  ^                              |    ^
  |                              |    |
  |                          IMDWorkspace
  |                                 ^
  |                                 |
  |  MultipleExperimentsInfos       |
  |           ^                     |
  |           |                     |
IMDHistoWorkspaceStripped           |
  ^                                 |
  |                                 |
  |-----------------------------    |
  |                            ^    |
  |                            |    |
IMDWorkspaceStripped         IMDHistoWorkspace
  ^                               ^
  |                               |
  |                          MDHistoWorkspace
  |
  |
  |
  |-------------------------------------
  |                                    |
IStackOfImagesWorkspace             ?CompactMDHistoWorkspace or similar?
  ^
  |
StakcOfImagesWorkspace

Note: IMDHistoWorkspaceStripped is a regular grid workspace (regular
on a dimension-by-dimension basis).

Note: it could well happen that what is now called
"IMDWorkspaceStripped" in the diagram would rather be something like
"ICompactMDHistoWorkspace".

This obviously gets complicated. And to complicate it further, there
is much functionality in the API::IMDIterator iterators that would not
apply to stacks of images. So a stripped version of them would be
needed as well.

On the bright side, the left pipeline path of the diagram can be
created with extremely minimal functionality taken from the more
traditional MD classes. Then the "stripped" or "base" functionality
that is found to be applicable and useful would be moved to the left
side incrementally.

Note that IStackOfImages could actually be something that is not
necessarily images, but just multidimensional regular-grid
data. StakcOfImagesWorkspace adds imaging specific data and
functionality. For example, parameters required for image
pre-/post-processing or tomographic reconstruction, such as center of
rotation, filter parameters, etc. would be present only under
IStackOfImagesWorkspace/StackOfImagesWorkspace.

In the diagram left path, there cannot be any functionality tied to a
particular pixel type (double in traditional workspaces). The question
is if at the bottom, StakcOfImagesWorkspace should be a template.

Pros & cons of this approach:
- The obvious advantage we are after is better integration and code
  re-use between different workspace types
- Several new base classes need to be introduced. Risk of messing
  things up in the future.
- Flexible and hopefully safe and sensible outcome if done
  incrementally.


Approach 2: Minimal class hierarchy
-----------------------------------

The opposite end to approach 1 is to simply derive from Workspace and
MultipleExperimentsInfos (or ExperimentInfo in its simplest
version). The stripped MDGeometry class would still be worth
considering.

```
Kernel::DataItem
  ^
  |
Workspace     MDGeometryBase     MultipleExperimentsInfos
  ^            ^                      ^
  |            |                      |
  |            |      -----------------
  |            |      |
  |            |      |
IStackOfImagesWorkspace
  ^
  |
StakcOfImagesWorkspace
```

Pros & cons:
- simple
- too limited


Additional notes on the practical use of StackOfImagesWorkspace
===============================================================

It should be possible to write Python algorithms that manipulate the
numpy multidimensional arrays, and combine them with flexibility, as
it will be very convenient for users to be able to manipulate some
images or the stack as a whole with simple filters or masking,
algebraic, etc. operations.
