# Update on neutron imaging functionality in Mantid

Interest in neutron imaging in general and energy resolved neutron
imaging in particular has been growing in recent years. Several
imaging instruments are currently in different stages of planning,
construction, commissioning and operation at pulsed neutron sources
around the world, such as IMAT at ISIS (UK), ODIN at ESS (Nordic
countries), RADEN at J-PARC (Japan), and VENUS at SNS (USA).

IMAT (Imaging and Materials Science & Engineering) is undergoing
commissioning in 2016 and provides neutron radiography (2D), neutron
tomography (3D), energy resolved (fourth dimension) and
energy-dispersive neutron imaging. IMAT offers unique time-of-flight
diffraction techniques by capitalising on latest image reconstruction
procedures and event mode data collection schemes. These features
impose several software requirements for data reduction and analysis
that differ substantially from other neutron techniques.

The [Mantid software project](http://www.mantidproject.org) provides
an extensible framework that supports high-performance computing for
data reduction, manipulation, analysis and visualisation of scientific
data. It is primarily used for neutron and muon data at several
facilities worldwide. Mantid includes several so-called custom
interfaces specialized for different scientific areas.

We give an update on recent developments in the Mantid software to
provide better support for neutron imaging data and to support the
commissioning of IMAT at ISIS. This involves new data structures, data
processing components or algorithms, and user interfaces to satisfy
the higher demands of energy-depending neutron imaging in terms of
data volume and complexity of analysis.

A custom graphical user interface for imaging data and tomographic
reconstruction is available in recent releases of Mantid. It
integrates capabilities for pre- and post-processing, reconstruction,
and 2D and 3D visualisation. This functionality can be used for
instruments specifically designed for imaging experiments as well as
other instruments using imaging detectors.

Diverse tools for tomographic data reconstruction and analysis are
being developed by different research groups and synchrotron and
pulsed-source facilities. The imaging graphical interface of Mantid
offers a common, harmonised interface to use an array of tools and
methods that are currently being trialed, including for example third
party tools for tomographic reconstruction such as
[TomoPy](https://github.com/tomopy/tomopy), the [Astra
Toolbox](https://github.com/astra-toolbox/astra-toolbox),
[Savu](https://github.com/DiamondLightSource/Savu/), and
[MuhRec](https://www.psi.ch/niag/muhrec).
