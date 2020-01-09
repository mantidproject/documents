Merging the multidimensional hierarchical workspaces based on Morton indexes.
-----------------------------------------------------------------------------

The main idea is to base this algorithm on `MDEventTreeBuilder` using similarly as it used in `Indexed mode section` of
`ConvertToMd <https://docs.mantidproject.org/nightly/algorithms/ConvertToMD-v1.html>`_  and minimize copying and
memory allocations. The general ideas are described in
`design proposal <https://github.com/mantidproject/documents/blob/master/Design/MDWorkspace/MDSpaceDesign.md>`_ .
The main difficulty is the "incompatibility" of the workspaces created with the indexed and non indexed mode as well as
the indexed workspaces with the different boundaries of the global "box": to merge the arbitrary (B)
workspace to the indexed (A) one it is needed to collect all the events from B, sort them
according to the Morton index and maybe extend A. So the only beneficial in terms of performance
case would be then the both (or more) workspaces are indexed with the same bounding box. In this case
only leaves could be merged by adding the events to leaves boxes and distributing them using
`MDEventTreeBuilder` methods. May be for simplicity it is worth to fall back non-indexed algorithm
in all cases except the last described.

The several ideas for the parallelization of the algorithm:

1. Find the workspace with the biggest number of events and merge the others one by one into it
   making parallelization by leaves.
2. If the amount of workspaces to merge is notable then it is worth to split all set into independent
   subsets and merge independently to decrease the number of outputs, afterwards fall back into
   the first scenario.
3. If the input workspaces are inhomogeneous in terms of global bounding box and indexing, then
   the argument set could be split into homogeneous chunks and processed (the issue here is how to
   merge the final inhomogeneous parts, this should be discovered).

The skeleton for the implementation with the comments could be found at
`branch <https://github.com/mantidproject/mantid/blob/igudich/merge_md_indexed/Framework/MDAlgorithms/src/MergeMD.cpp>`_.

