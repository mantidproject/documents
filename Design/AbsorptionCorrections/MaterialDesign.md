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
`ExperimentInfo` has a [`Sample`](http://docs.mantidproject.org/v3.7.1/api/python/mantid/api/Sample.html)
which has `Geometry`, `CrystalStructure`, and 
[`Material`](http://docs.mantidproject.org/v3.7.1/api/python/mantid/kernel/Material.html).

Replacing `SetSampleMaterial`
-----------------------------

`SetSampleMaterial` currently calculates many values and returns them as output properties. This is inconvenient
as it ties users to this specific algorithm. Instead, `Material` will have the following attributes:

