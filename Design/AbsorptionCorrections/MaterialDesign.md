Materials (re)design
====================

Motivation
----------

There are serveral tickets concerning `NeutronAtom`
([#11542](https://github.com/mantidproject/mantid/issues/11542),
[#9267](https://github.com/mantidproject/mantid/issues/9267),
[#7565](https://github.com/mantidproject/mantid/issues/7565),
[#5670](https://github.com/mantidproject/mantid/issues/5670)),there is
too much derived information is presented/calculated in
[SetSampleMaterial](http://docs.mantidproject.org/nightly/algorithms/SetSampleMaterial-v1.html),
the scattering length information has some incorrect information, and
the absorption information does not contain the correct wavelength
dependency. In the process of fixing these various issues, it is a
good time to re-visit the design of the various classes to see if
there is a better way to organize things.

Status
------

The `Atom` class is a static constant class with public
attributes. One of these is `Atom::neutron` which is a `NeutronAtom`
object. The `NeutronAtom` class has members for the (tabulated) values
of scattering information. While this is serviceable, the more natural
interface is for people to use the `Material` class itself for

The (slightly) bigger picture
-----------------------------

A [`Workspace`](http://docs.mantidproject.org/v3.7.1/api/python/mantid/api/Workspace.html) 
has a [`ExperimentInfo`](http://docs.mantidproject.org/v3.7.1/api/python/mantid/api/ExperimentInfo.html). 
`ExperimentInfo` has a [`Sample`](http://docs.mantidproject.org/v3.7.1/api/python/mantid/api/Sample.html).

The [`Sample`](http://docs.mantidproject.org/v3.7.1/api/python/mantid/api/Sample.html) will have the following attributes:
 * methods for the Geometry
 * methods for the `CrystalStructure` (currently `getCrystalStructure()`)
 * methods for the `Material` (currently `getMaterial()`)
 * methods for a "friendly name" (currently `getName()`)

The [`Material`](http://docs.mantidproject.org/v3.7.1/api/python/mantid/kernel/Material.html) will have the attributes
 * the scattering length information is taken from an out-of date source. It sould be using from [link](http://www.ati.ac.at/~neutropt/scattering/)
 * methods for the chemical formula (currently `chemicalForumla()` which returns a `List` of [`Atom`](http://docs.mantidproject.org/v3.7.1/api/python/mantid/kernel/Atom.html) and a `List` of composition numbers). The chemical formula should also provide functionality to get the relative fraction of each atom.
 * methods for the number density (currently `numberDensity`)
 * methods for the mass density (currently missing)
 * methods for the packing fraction (currently missing)
 * methods for the effective number density (currently missing) which will be calculated from the product of the number density and the packing fraction.
 * methods for the effective/composite cross sections (present) and scattering lengths (missing, including scattering length calculated from the `b=sqrt(total xs) / (4 pi)`). The current neutronic information has the real and (generally zer) imaginary parts, but not the magnitude.
 * methods for `<b>^2`, `<b^2>` and the normalized Laue term
 * improved methods for getting the absorption cross-section as a function of wavelength with information from [link](https://www-nds.iaea.org/ngatlas2/) and [link](http://www.nndc.bnl.gov/sigma/index.jsp)

Replacing `SetSampleMaterial`
-----------------------------

`SetSampleMaterial` currently calculates many values and returns them as output properties. This is inconvenient
as it ties users to this specific algorithm. Instead, `Material` will have the following attributes:

