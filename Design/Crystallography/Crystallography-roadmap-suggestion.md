Mantid crystallography roadmap suggestion
=========================================

Motivation
----------

Certain aspects of crystallographic computation are already modelled within the Mantid framework, but so far the implementation is not very coherent or complete. As a consequence, many existing low level components that reside in the Geometry-namespace are not used by higher level components, such as algorithms in the Crystal-submodule. Another factor for the lack of use is that many things have been added over the last 12 months and are thus relatively new.

Using the low-level concepts now available in Geometry can make some of the algorithms in Crystal more concise and easier to read, for example SortHKL, where parts of the code deal with finding equivalent reflections using the methods available at the time it was written. This can now be done with less code using the extended interface of Geometry::PointGroup. Another example is PredictPeaks, which could be extended to support different methods to determine reflection conditions besides the lattice centering that is available now. Using the structure factor calculation tools it could also predict intensities (this has already been requested by Pascal Manuel, ticket #13908).

Besides improving existing algorithms, new ones can be added. The first example for a new algorithm could be a space group determination routine using the ExtSym-method that has initially been designed for powder diffraction applications. Exporting more and more of the C++-implemented concepts to the Python interface will make these components accessible for end-users as well.

Overall, improving and extending the crystallographic tools in the Mantid framework may in turn improve many algorithms and lead to a better user experience with more integrated workflows that don't have to rely on external tools at early stages of the data processing.

This document is intended as a basis for discussion, anybody who has an interest in the topic should make modifications as required. Maybe some "synchronization" with requirements from the SSC is necessary so there are no collisions and tasks get the right priorities.

Short term goals
----------------

For short term planning there are two aspects to consider. The first aspect is to complete and polish the crystallographic computations that have been added so far. This concerns mostly space groups:

  - Up to now, only standard settings from ITA are implemented. Especially in the monoclinic and orthorhombic system, many space groups have many different possible settings. These should be implemented by applying transformations to the existing space groups. A separate transformation type may be sensible for this.
  - Proper support for trigonal space groups with the possibility to use both settings for trigonal space groups. So far, only the hexagonal setting is supported. This problem is related to the first one and could be handled accordingly using a transformation.
  - Improve space group symbol handling. It should be possible to use the symbols with or without spaces for example, the same is true for point group symbols.
  - In principle, the ReflectionCondition class can be implemented using SymmetryOperation as well. For this to work properly, space groups should maybe store the translation group separately so that it can be retrieved easily later on.
  - Integrate crystallographic objects with PropertyManager, so that they can be used directly in algorithms, potentially along with validators.
  - Harmonize method naming, possibly according to the Python-bindings, where such a harmonization has already been done.

The second aspect is about using the existing (possibly in some aspects polished) code to develop simple examples that demonstrate the use (and hopefully the usefulness) of the existing low level crystallography code. So far there are two fairly concrete tasks for which tickets have already been created:

  - Modify PredictPeaks to not only calculate reflection positions but also estimated intensities, indicate intensity to the user in instrument view and later on also in slice viewer.
  - Implement simplified ExtSym-algorithm (published by Anders Markvardsen) for single crystal data to determine space group. This requires the first two issues of the above list to be completed.

These points from both aspects can all be handled as fairly well separated tasks (although with some dependencies between them), it's realistic to finish those or at least most of them before the 2016 developer workshop. Overall these changes aim to make the current code more usable and more useful, as well as to provide examples for what is possible using the available tools.


Medium term goals
-----------------

In addition to the short term goals, there are some issues that could be solved within the existing framework but may require redesign of certain components, some of them even more low level than what’s in Geometry:

  - Add "Reflection"-class. Conceptually this class is somewhere between V3D and Peak in terms of complexity and
  scope. Reflection would essentially include the Miller indices HKL and probably a d-value and a structure factor. Peak would then hold a Reflection internally, probably a pointer. That way, several peaks could point to the same reflection, the reflection could probably also point to its "reflection family". Such a structure would make gathering statistics on reflections and unique reflections very simple.
  - Evaluate feasibility and usage of HKLFilter. If it turns out to be well usable, add the concept of an HKLTransformation. These transformations would provide mappings of the form V3D -> x, where x could be double or again V3D.
  - Create a transforming iterator for use with HKLGenerator. That way, transformations of reflections could be performed on the fly while creating them.
  - Look at other algorithms in Crystal-module. Some of them can be formulated in a much more concise way using HKLGenerator, PointGroup and so on with added possibilities to improve performance (SortHKL example from above). Other algorithms could profit from extended functionality.
  - Consider introducing a semantic difference between vectors and points. Currently everything is represented by V3D, including HKL which is actually an integer vector. With different classes for vector and point types some mistakes may be avoided and some code may be easier to understand. Of course, the underlying implementation should still be generic, the Eigen-library provides good examples for this.

Besides technical goals, there are also scientific considerations to make:

  - Gather requirements from single crystal/powder beam lines to find out if algorithms can be added to improve the workflows.
  - Find out if and how areas other than diffraction may benefit from the crystallographic code.

These goals require some design effort and discussion. The 2016 developer workshop provides a good opportunity for such discussions, but some design documents should be prepared in advance where necessary.

Long term goals
---------------

This section is a bit broader than the previous two.

Some of the considerations are more long-term and concern for example requirements of new ESS instruments (possibly also existing ones?). One specific example is provided by NMX (macromolecular crystallography beam line) where experiments lead to data sets with potentially millions of peaks. Are the current implementations of Peaks/PeaksWorkspace capable of handling these amounts of data with enough performance?

Another concern may be integration of other crystallographic libraries. What functionality from other libraries such as cctbx could be useful for Mantid? Is it feasible to integrate them on a C++-level or is the possibility of using the python libraries enough? Could it be an advantage to keep, maintain and further improve the code that has been added to the Mantid framework?

Summary
-------

The "roadmap" presented above covers three time scales. The short term goals are very concrete tasks that can be implemented before the 2016 developer workshop. The medium term goals are somewhat concrete as well, but require some design effort that may be feasible to discuss in the context of the developer workshop so that specific tasks can be derived at that time. The long term goals are subject to continuous discussions.