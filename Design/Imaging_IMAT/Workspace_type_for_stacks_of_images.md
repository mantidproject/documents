
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


Design overview
===============

Position and interaction between *StackOfImagesWorkspace* and other
(MD) workspaces. Interface *IStackOfImagesWorkspace*.


Additional notes on the practical use of StackOfImagesWorkspace
===============================================================

It should be possible to write Python algorithms that manipulate the
numpy multidimensional arrays, and combine them with flexibility, as
it will be very convenient for users to be able to manipulate some
images or the stack as a whole with simple filters or masking,
algebraic, etc. operations.
