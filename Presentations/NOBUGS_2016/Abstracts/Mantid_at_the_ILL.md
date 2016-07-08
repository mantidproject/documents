## The ILL Joins the Mantid Project

**Type: Oral Contribution, Track: Distributed Development**

#### Antti Soininen<sup>1</sup>, Gagik Vardanyan<sup>1</sup>, Ian Bush<sup>1,2</sup>, Verena Reimund<sup>1</sup>

1. Institut Laue-Langevin, Grenoble, France
2. Tessella plc, Abingdon, Oxfordshire, UK

At the ILL LAMP (Large Array Manipulation Program) [1] has been the primary package responsible for data reduction for over 20 years. LAMP is based on IDL, so works across multiple platforms, and provides a graphical user interface and scripting capabilities for data treatment. It provides support for all of the instruments at ILL, having the ability to handle data produced at the ILL since its creation. However, with the imminent retirement of one of the developers a decision has been made to phase out LAMP and bring in Mantid [2] as the primary package for data reduction. LAMP will still be used for historic data which would be difficult to support comprehensively in Mantid, but only essential maintenance work will be done for LAMP in the future.

The Mantid Framework has many similarities to LAMP, it also works across multiple platforms, and provides both GUI and scripting for data manipulation. Mantid has been in use for some time at ISIS and the SNS, and the ESS will also use it for all data reduction. A number of advantages foreseen in adopting Mantid, both the software and the development distributed development approach are already well established, so much of the data reduction functionality LAMP provided already exists in Mantid. In addition, it will also provide a more consistent user experience for users undertaking experiments at different facilities. Within the Mantid Project, there are many example of collaborative sub-projects, which have allowed allowing several facilities to contribute to, and benefit from combined effort.

The current Mantid adoption project started in May 2016 at the ILL, and builds on previous work undertaken during a project to explore using Mantid in principle. The project involves a team of three new developers for three years, plus a developer for one year with existing Mantid experience, and the Computing for Science Group at the ILL. The aim to support most of the instruments at the ILL after the end of the initial 3 year period.

In this talk we will discuss the progress made thus far in using Mantid on Time-of-Flight spectroscopy (IN4, IN5 and IN6) and Backscattering (IN16B) instruments at the ILL. We will discuss some of the differences in approach between and LAMP and Mantid and the challenges this created for comparing results between them. We will also discuss the future plans for the project to address the other technique areas, and supporting instruments with moving detectors at the ILL.

[1] https://www.ill.eu/instruments-support/computing-for-science/cs-software/all-software/lamp/the-lamp-book/

[2] http://www.mantidproject.org/

##### Alternative (Gagik)

At the ILL LAMP (Large Array Manipulation Program) [1] has been the primary package responsible for data reduction for over 20 years. Despite handling the data produced at the ILL since its creation, it is less viable nowadays due to being based on technologies, like IDL, unfamiliar to modern users, and limited capabilities to accommodate growing needs by the scientific community. In order to facilitate ease of use and the standardisation of neutron data reduction software across many facilities worldwide, a decision has been made to phase out LAMP and bring in Mantid [2] as the main tool for the upcoming data treatment. Extensively used at the ISIS, SNS and recently ESS, it will soon become the standard at ILL.

The Mantid Framework is a cross-platform and easy-to-extend package providing both GUI and python scripting facilities for complex data manipulation. A number of advantages foreseen in adopting Mantid, both from the perspective of well established distributed development practices, as well as powerful data reduction facilities far beyond LAMP. In addition, it will foster user mobility by providing more consistent user experience for those undertaking experiments at different facilities. 

The current Mantid adoption project at ILL launched in May 2016, and is based on the effort undertaken during the previous project of exploration of using Mantid in principle. The 3-year long project involves a team of 3 new developers  plus a developer for one year with existing Mantid experience, under the Computing for Science Group at the ILL. The objective is to enable smooth transition from LAMP to Mantid by providing support for most of the instruments and reduction logic at the ILL in Mantid Framework.

In this talk we will present the progress made thus far in this area.  We will focus mostly on Time-of-Flight (IN4, IN5 and IN6) and Backscattering (IN16B) spectroscopy instruments at the ILL. We will discuss some of the differences in approaches between LAMP and Mantid and the challenges faced along the way. We will also share the future plans to address the other technique areas and to support instruments with moving detectors at the ILL.


-----------------------------
##### Original (Ian)

A new team from the ILL has joined the Mantid project, building on work already undertaken to support instruments at the ILL. We will discuss the progress made in these areas, Mantid adoption on instruments and the challenges of adding a new distributed development team to the Mantid project. We will also discuss some of the future challenges that will need to be addressed for adoption of Mantid at the ILL.

##### Original (Gagik)

A new team at the ILL has joined the Mantid project, with the objective to fully implement ILL instruments support into Mantid. We present the progress made in these area, with the focus on the domains of TOF and Backscattering data reduction. Some future challenges that will need to be addressed for commisioning of Mantid at the ILL are also discussed.
