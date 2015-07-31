Symmetrization
==============

A symmety operation is a process trough wich data in a certain zone can be moved to a different zone in such a way that the physical meaning
is not changed. For example, in a cubic system, a measurement along H direction is equivalent to a measurement in the K direction,
or a measurement in the L direction. It is sometimes easier to measure a part of the data in one region, and part of the data in a different
region. This can happen simultaneously in the case of instruments with multiple detectors. For visualization and analysis purposes,
and to get better statistics, it is useful to move all the data into one region, as long as it is allowed by physics of the system. 

Symmetrization in Mantid should be applied only to MDEvent workspaces. In particular cases, only for certain symmetry operations, 
and only with certain binning choices, symmetry can be applied to the histogram representation directly. For example, sor equal bins along 
H, K, L directions, if the dimension of the workspace in those directiops are equal, symmetric with respect to origin, one can directly
symmetrize the histogram representation by 90 or 180 degrees rotations, inversions with respect to origin, reflections across H=0, K=0, L=0 planes. 
This procedure however breaks down for 60 degrees rotations, or if the bin sizes or domains along different axes are not identical.  

If we have N MDEvents, one possible approach would be to generate additional sets of N MDEvents for each symmetry operation. This
has the advantage that once added to the original workspace, BinMD(SliceMD) would immediately yield the symmetrized data, along any slice/cut.
The big disadvantage is memory usage, which is proportional to the number of symmetry operations.

A second approach is to apply the symmetry operations only on the events that fall outside a certain region. For example, consider a square 
in the HK plane, with corners at (-1,-1),(-1,1),(1,1),(1,-1). We can reduce this to a triangle (0,0),(0,1),(1,1), and obtain the rest of the 
square by certain symmetry operations. The advantage is that it is not using more memory than the original workspace. Disadvantage is that BinMD
wold sometimes produce workspaces that are difficult to visualize, and it requires knowledge about where your desired measurement is showing up
in the symmetrized space. For example, in the case of the square described before, if I want to plot a cut from (-1,1) to (1,-1), I would
need to go instead from (0,0) ton (1,1). If the cuts are along some low symmetry directions, this can become more complicated for the users.

The best solution is to leave the original workspace as is, and just store symmetry operations on it. Then apply the symmetry operations when 
we create the histogram representation. There are only a few algorithms that need to implement this feature: BinMD, SliceMD, and MDNorm...
Advantage: should be very easy for the user to understand how to use it, and will not use more memory. Disadvantage: the algorithms need to be
applied as many times as symmetry operations. We can hide this from the user, but it still take more time than the algorithm for
non symmetrized data.

I propose that we store the symmetry operations as affine matrices, based on the dimensionality of the input workspace. 
This would allow to implement rotations, inversions, reflections, screw axes, translations, and so on, in a very intuitive fashion. For the 
point groups, one can already find the symmetry operations. For example, P6 group (one of the hexagonal ones), the symmetry operations are
(x,y,z),(-y,x,y,z),(-x+y,-x,z),(-x,-y,z),(x-y,x,z), and (y, -x+y z). In principle we can write these as 3x3 matrices. If we want to allow 
for translations, we add one more dimension, so they become 4x4. But Mantid supports additional dimensions, that we might want to symmetrize
or not, such as energy transfer, applied, electric field, temperature, and so on. It also allows us to store the dimensions in an arbitrary fashion.
That's why the symmetry operation stored as a matrices should be workspace dependent. For example, reflection with respect to H axis will
be written differently for the case of diffraction in the H, K, L basis, versus inelastic in the HH, -HH, L basis.

Implementation
==============

1. Allow storing a vector of matrices on an MDEvent workspace. Need to check how different algorithms would affect the stored matrices. For example,
if workspace w1 has one set of matrices, and workspace w2 has a different set, what should be w1=w2?
2. Add option to apply symmetry operations for BinMD/SliceMD/MDNorm..., and check if any other algorithm needs to do this.
3. In the case of BinMD and SliceMD we need to recalculate the basis, extents, and steps for each symmetry operation. A detail that we
must consider: what to do if SymmetryCalculatedMinimum>SymmetryCalculatedMaximum for a certain dimension. In this case we calculate the binning from 
SymmetryCalculatedMaximum to SymmetryCalculatedMinimum and then reverse the array in the MD histo
4. MDNorm algorithms will need to calculate the norm for each symmetry orientation. This can be done by recalculating the ends of
detector trajectories according to each symmetry operation. Need to better keep track of detector trajectory limits through
different MD algorithms (like slicing). To do that, we need in ConvertToMD to add two numbers for every detector containing the limits
in momentum (or energy transfer for inelastic). These values must be added into the experiment info, if we want to merge multiple runs into 
the same MD workspace.
5. Hide the need for multiple calls for each symmetry operation, and allow the algorithms to call themselves recursively
6. Write simple (python) algorithms that allow users to automatically generate/store/show/delete symmetrization matrices

To think about
==============
1. What to do with intermediate workspaces? This is the case if I want to take a cut out of a slice. I think we just need to be able to go
back to the original workspace
2. How to show things in SliceViewer? The MDEvent workspace shown initially in SV will not exhibit symmetry, but data is symmetrized as soon 
as you rebin it. 
