Making HKL different
====================

Motivation
----------

Currently the class `Kernel::V3D` is used to represent a large range of points and vectors in different spaces. Detector coordinates, unit cell vectors, Miller indices and many more are all represented by the same very low-level class `V3D`. While this is certainly very flexible in terms of the number of classes and/or interfaces developers need to keep track of, it comes with a number of disadvantages. The most important is probably that it's possible to perform nonsensical operations such as adding detector coordinates to a unit cell vector - since different types do not exist, they can not be enforced by the compiler, which means the burden of preventing errors falls to the developer. A similar case is where real and reciprocal space vectors have to be transformed by using different matrices. Without dedicated types the developer needs to make sure the correct matrix is used and in addition runtime checks have to be performed.

While it is a big task to make each and every use of `V3D` (and connected to that also `Kernel::Matrix`) type-safe, implementing a dedicated type for Miller indices HKL is a rather confined task. Potential replacements for `V3D` in this domain can exist in parallel at first and code can be ported step-by-step, simply reverting to the current "unsafe" implementation where necessary.

Requirements
------------

There should be a datatype different from `V3D` but with similar capabilities that is used to represent Miller index triplets.

While in theory, Miller indices are defined to be composed of three integer numbers, some flexibility is required for cases in early steps of data processing where exact integers may not be known or for commensurate superstructures where fractional indices can occur.

Though similar, those three cases cover different uses and should be covered by different types:

  1. `HKL` (integer, "proper Miller indices")
  2. `ProHKL` (double, "early stages of reduction")
  3. `FractionalHKL` (double, use for magnetic or other super-structures)

These types should be by default incompatible, i.e. it should not be possible to add a `ProHKL` onto a `FractionalHKL`-object unless either is explicitly converted to the other. The same is true for comparisons and so on, but as assumed above, it should be possible to perform certain explicit conversions between the types.

Furthermore there are some algorithms or operations that are agnostic to the type, so there should be a way to define algorithms that work for general objects that are "HKL-like".


Design
------

IsHKL-mixin
~~~~~~~~~~~

All of the above requirements can be solved by the so called "Curiously Recurring Template Pattern" (CRTP). For this particular purpose, the base class needs to be templated on the numeric type as well as on the derived type as it is normal for the CRTP:


```
template <typename NumericType, typename Derived>
class IsHKL {
public:
  const NumericType &h() const { ... }
  void setH(const NumericType &h) { ... }
  ...
  
  bool operator==(const Derived &rhs) {
    ...
  }
};

class ProHKL : IsHKL<double, ProHKL> {
  ...
};

class FractionalHKL : IsHKL<double, FractionalHKL> {
  ...
};

class HKL : IsHKL<int, HKL> {
  ...
};
```

This way, it is possible to compare for example two `ProHKL`-objects or two `HKL`-objects, but not a `ProHKL` and an `HKL`, as expressed in the requirements. It is however no problem to add custom operators to the derived classes should it be desired to allow a certain comparisons between those.

All conversions between different derived types must be marked `explicit` to prevent accidental implicit type conversion. This adds further safety to handling different types of indices within the same algorithm.

Writing generic algorithms
~~~~~~~~~~~~~~~~~~~~~~~~~~

When writing generic algorithms handling these HKLs it's important to handle types correctly. Functions dealing with `IsHKL` have to be templated with respect to both parameters, so in general:

```
template <typename NumericType, typename Derived>
bool isNonZero(const IsHKL<NumericType, Derived> &hkl) {
  return std::all_of(hkl.cbegin(), hkl.cend(),
		     [](const NumericType &index) { return index != NumericType{0}; });
}
```

If functions perform transformations and return a transformed HKL, they must return a `Derived`-object:

```
template <typename NumericType, typename Derived>
Derived higherOrderHKL(const IsHKL<NumericType, Derived> &hkl, const NumericType &order) {
  Derived higherOrder;
  std::transform(hkl.cbegin(), hkl.cend(), higherOrder.begin(),
		 [=](const NumericType &index) { return index * order; });
		 
  return higherOrder;
}
```

Inside these functions it is also always possible to use `static_cast` for turning the object into the derived type:

```
template <typename NumericType, typename Derived>
NumericType indexSumOfDifference(const IsHKL<NumericType, Derived> &lhs, const IsHKL<NumericType, Derived> &rhs) {
  Derived difference = static_cast<const Derived &>(lhs) - static_cast<const Derived &>(rhs);
  
  return std::accumulate(difference.cbegin(), difference.cend(), NumericType{0});
}
```

Suggested implementation
~~~~~~~~~~~~~~~~~~~~~~~~

There's a [PR](https://github.com/mantidproject/mantid/pull/15914) against the main repository where this design is implemented. It revealed one unfortunate name clash, `Mantid::Geometry::HKL` already exists as a sub-class of `MDFrame`. My suggestion for this is to use the opportunity and start migrating the crystallography related code into a new module called Crystallography, which then provides a new namespace `Mantid::Crystallography`. Initially I suggest that this new module sits between `Kernel` and `Geometry`. Once the existing crystallography-related code has been migrated, the dependency of the Geometry module on the Crystallography module can be removed.

In the pull request there is a performance test as well that compares the performance for some common operations that are performed on HKLs between the different cases `int` and `double`, but also with `V3D`.

Relative execution times (normed to `int`, lower is better):

| Test   | `int`  | `double`  | `V3D`*  |
|---|---|---|---|
| hkl1 == hkl2  | 1.0  | 1.6  | 2.3 |
| hkl1 < hkl2   | 1.0  | 1.1  | 0.8 |
| Matrix * hkl  | 1.0  | 1.5  | 4.8 |

* = `V3D` does not do fuzzy comparison of floating point values for `operator<`, but it does for `operator==`. `IsHKL` does fuzzy comparison for both.

Some of the difference is probably attributable to lack of inlining in `V3D`, but the main point is that the added type-safety doesn't result in runtime penalties.


Remaining issues
----------------

Some open questions remain:

  - Python export - not sure how well this transports through to Python
  - Moving to new Crystallography-module
  - Implement a "real world" example from the Geometry- or Crystal-module.

Once the Python-export issue is solved, all the point- and space group code could be refactored to use these new types. 