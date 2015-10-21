
# Introduction


This document describes the design of a new type of workspaces
suitable to store and process stacks of images. While that is in
principle the motivation for this design, equivalent data structures
may be useful in diferent contexts, so additional aspects may be
introduced as this document evolves.

The basic need is to have an efficient and simple representation of
stacks of images or n-dimensional images.



# Objectives

## High-level
1. Create an efficient type for storage of stacks of images 3+ dimensions
2. Create a compressed form of the IMDHistoWorkspace specifically for visualization where the majority of the IMDHistoWorkspace information can be ditched. Compression.

This design is specifically motivated by the new instrument IMAT which
is expected to produce large collections of images. A new type of
workspace should be defined that:

* Holds stacks of images coming from neutron imaging experiments.

* Can be used as a convenient and efficient data structure to
  interoperate with third party tools, visualize stacks of images, and
  apply image processing algorithms.

This will require the introduction of a new type of multidimensional
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

# Requirements

Here is a (potentially growing) list of requirements that should be
kept in mind for the design. Their implementation could be iterative.

* Efficient, raw storage of data
* Avoid "overheads" of workspace types like Workspace2D: no errors, no
  doubles, etc. But ideally these should still be supported
  optionally.
* It should be possible to represent multiple dimensions, not just
  flat stacks of 2D images.  Typical dimensions can include X and Y
  (2D image), projection angle in tomography, energy band/level, time,
  and potentially more (experiment conditions, etc.).
* Python interface for scripting, with numpy array support. 
* Support for types like 8 and 16 bits integers, etc. A 16 bits pixel
  size is very common.
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

Eventually the new workspace type should be effective as input/output
to/from algorithms that may have to process hundreds of thousands of
files. An example of this is to aggregate stacks of ~100000 energy
selective individual image files (or alternatively large, several
gigabytes or hundreds of gigabytes, nexus or NXTomo files) into stacks
of ~1000 images (or alternatively few gigabytes nexus files). Two
factors should be considered in the design:
* Potentially very large number of underlying files which we do not
  want to open, or even check their existence/readability unless
  strictly needed.
* Required: capability and neat interface to process one image at a
  time, sequentially, avoiding multiple copies in memory, etc.

# Current hierarchy of MD workspaces at a glimpse

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
API::IMDWorkspace  [Note: it has methods getMask(), getError(), etc. that MDImageWorkspace does not need or want]
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
* Geometry::IMDDimension:
  http://doxygen.mantidproject.org/nightly/dd/db2/classMantid_1_1Geometry_1_1IMDDimension.html
* API::ExperimentInfo:
  http://doxygen.mantidproject.org/nightly/d4/d42/classMantid_1_1API_1_1ExperimentInfo.html
* API::MultipleExperimentInfo:
  http://doxygen.mantidproject.org/nightly/d7/d1f/classMantid_1_1API_1_1MultipleExperimentInfos.html

# Design alternatives

There are several general features of workspaces (or some types of
workspaces) that the new type of workspace should have. These include:
basic information such as name, comment, memory, but also instrument
and experiment information, and history.

The name *MDImageWorkspace* is in principle chosen so that it is
sufficiently general, with the idea that it represents either multiple
images or a multidimensional structure of images.

Individual images are definitely regular grids. And stacks of them,
even if along multiple dimensions (for example dimension 3: multiple
projection angles, dimension 4: muliple energy levels, dimension 5:
multiple re-runs over time) are also treated without MD-ish operations
such as (re-)binning, event/histograms, etc. In any case a dimension
can be collapsed by simple operations such as for example a sum (or
average) image for all energy levels.

Functionality that MDImageWorkspace needs or wishes to have and where
to get it from:

- Instrument and experiment information. Two alternatives:
  API::ExperimentInfo and API::MultipleExperimentInfos.

- Workspace/algorithm history: included in API::Workspace.

(Obvious) points that are highly certain and are a solid starting point:

- MDImageWorkspace should inherit from Workspace. This also
  implies that it derives from DataItem which should be enough to
  guarantee that MDImageWorkspaces can be in the Analysis Data Service
  and that Mantid algorithms can be run on them.

- No point to use MatrixWorkspace interface and functionality as
  MDImageWorkspaces do not (need to) have traditional spectra, (X, Y,
  Error). Also, do not get confused by the MantidImage type and
  related methods in API::MatrixWorkspace. We are not using that image
  type here.

- In a similar way as MatrixWorkspace has dataX() and dataY() which
  return a MantidVec reference, and readX() and readY() which return
  const MantidVec references, MDImageWorkspace should have `data()`
  and `roData()` methods.

- MDImageWorkspace should also inherit from ExperimentInfo or
  MultipleExperimentInfos, and the second seems a better option for
  complicated stacks of images.

- Geometry::IMDDimension: should be usable as it is.

- API::MDGeometry (which uses IMDDimension): the IMDDimensions related
functionality is relevant, but this class also has (Q) transformations
and origin coordinates related stuff that does not seem to make sense
for MDImageWorkspace in general. It may make sense to define a
MDGeometryBase class (where I'd like to find a more specific name for
*Base*) which would have roughly the first few methods of MDGeometry,
excluding aspects like "Q", and would become its base/parent class.

## Approach 1: try to get as much as possible from traditional (I)MD classes

This is in principle the ideal and preferred solution.

This assumes that in the current hierarchy of MD classes all the
functionality, methods and members are placed exactly where they are
needed, never higher than strictly needed.

If we want to integrate this new workspace type in the existing IMD/MD
classes hierarchy, many issues arise when trying to find a position
and proper interaction between *MDImageWorkspace* and other (MD)
workspaces. A basic version of MDImageWorkspace would relate to other
classes and look like this:

```
Kernel::DataItem
  ^
  |
Workspace   MDGeometryBase
  ^           ^
  |           |
  |           |
  |           |
  |           |
IMDLeanWorkspace    [Note: (without getMask(), getError(), etc., without normalisation)]
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
IMDLeanHistoWorkspace               |
  ^                                 |
  |                                 |
  |-----------------------------    |
  |                            ^    |
  |                            |    |
MDLeanHistoWorkspace       IMDHistoWorkspace
  ^                               ^
  |                               |
  |                          MDHistoWorkspace
  |
  |
  |
  |
  |
IMDImageWorkspace
  ^
  |
MDImageWorkspace
```

Note: IMDLeanHistoWorkspace is a regular grid workspace (regular
on a dimension-by-dimension basis).

Note: *Lean* is used here to name the smaller and simpler versions of
workspace types (left pipeline), as in MDLeanEvent. But these
*MDLean...* classes are not nearly as tightly constrained as
MDLeanEvent.

Note: it could well happen that what is now called "IMDLeanWorkspace"
in the diagram would rather be something different like
"ICompactMDHistoWorkspace".

This obviously gets complicated. And to complicate it further, there
is much functionality in the API::IMDIterator iterators that would not
apply to stacks of images. So a *lean* version of them would be needed
as well.

On the bright side, the left pipeline path of the diagram can be
created with extremely minimal functionality taken from the more
traditional MD classes. Then the *lean* or base functionality that is
found to be applicable and useful would be moved to the left side
incrementally.

Note that IMDLeanHistoWorkspace could actually be something that is
not necessarily images, but just multidimensional regular-grid
data. MDImageWorkspace (or a different name/alias) adds imaging
specific data and functionality. For example, parameters required for
image pre-/post-processing or tomographic reconstruction, such as
center of rotation, filter parameters, etc. would be present only
under IMDImageWorkspace/MDImageWorkspace.

In the left path of the diagram there cannot be any functionality tied
to a particular pixel type (double in traditional workspaces). The
question is if at the bottom, MDImageWorkspace should be a
template. One alternative, if we want to avoid template workspace
types, is to have `data()`/`roData()` and similar methods for the
supported types, reinterpreted (2 and 4 bytes is good enough, and the
MDImageWorkspace always knows what is its actual pixel type). In any
case we need the capability to return numpy arrays of the appropriate
type in the python interface.

Pros & cons of this approach:
- The obvious advantage we are after is better integration and code
  re-use between different workspace types
- Several new base classes need to be introduced. Risk of messing
  things up in the future.
- Flexible and hopefully safe and sensible outcome if done
  incrementally.


## Approach 2: Minimal class hierarchy


The opposite end to approach 1 is to simply derive from Workspace and
MultipleExperimentsInfos (or ExperimentInfo in its simplest
version). The base or lean MDGeometry class would still be worth
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
IMDImageWorkspace------
  ^
  |
MDImageWorkspace
```

Pros & cons:
- simple
- too limited


# Additional notes on the practical use of MDImageWorkspace

It should be possible to write Python algorithms that manipulate the
numpy multidimensional arrays, and combine them with flexibility, as
it will be very convenient for users to be able to manipulate some
images or the stack as a whole with simple filters or masking,
algebraic, etc. operations.

# Implementation steps

I'd go for approach 1, and I'd propose to follow a sequence of small
incremental steps where every of the layers of the *lean* path shown
in the figure of approach 1 (from top to bottom) is implemented in a
(relatively) small individual issue/pull request. This would require a
minimum of 4/5 pull requests until we introduce all the base
interfaces/classes and MDImageWorkspace can be implemented. I'd be
very keen to start working on this soon now that we are at the
beginning of 3.6 development, so we have time to move code around and
deal with potential issues well before the code freeze for the next
release.

# Reviewer
* Owen Arnold

## Reviewer Notes ##
* Do we really want to store errors? What's the use case for this?
* I would suggest a typdef for the actual inttype to use. Do we have a need to have multiple forms of this workspace with different size types? If so you should see what has been done around the MDEventWorkspace.
* I would suggest storing the data in contiguous block. This will make a lot of operations easier, such as exporting to numpy.
* The workspace should inherit from MultipleExperimentInfos to support the IMDHistoWorkspace compression use cases.
* I much prefer option 1. Of the type hierachy.
