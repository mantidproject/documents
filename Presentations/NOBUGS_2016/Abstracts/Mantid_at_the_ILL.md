## The ILL Joins the Mantid Project

#### Antti Soininen<sup>1</sup>, Gagik Vardanyan<sup>1</sup>, Ian Bush<sup>1,2</sup>, Verena Reimund<sup>1</sup>

1. Institut Laue-Langevin, Grenoble, France
2. Tessella plc, Abingdon, Oxfordshire, UK

At the ILL LAMP (Large Array Manipulation Program) [1] has been the main software responsible for data reduction for over 20 years. LAMP is based on IDL, so works across multiple platforms, and provides a graphical user interface and scripting capabilities for data treatment. It has good support for all of the instruments at ILL, having the ability to handle data produced at the ILL since its creation. However, with the imminent retirement of one of the developers a decision has been made to replace LAMP with Mantid [2] for the main data reduction software. LAMP will still be used for historic data which would be difficult to support comprehensively in Mantid, but only essential maintenance work will be done for LAMP in the future.

The Mantid Framework has many similarities to LAMP, it also works across multiple platforms, and provides both GUI and scripting for data manipulation. Mantid has been in use for some time at ISIS and the SNS, and the ESS will also use it as their main data reduction service. A number of advantages are seen in using Mantid, both the software and the development distributed development approach are already well established, so much of the data reduction functionality LAMP provided already exists in Mantid. It will also provide a more consistent user experience for users undertaking experiments at different facilities.

The current Mantid adoption project started in May 2016 at the ILL, and builds on previous work undertaken during a project to explore using Mantid in principle. The project involves a team of three new developers for three years, plus a developer for one year with existing Mantid experience, and the Computing for Science Group at the ILL. The aim to support most of the instruments at the ILL after the end of the initial 3 year period.

In this talk we will discuss the progress made so far in using Mantid on Time-of-Flight spectroscopy (IN4, IN5 and IN6) and Backscattering (IN16B) instruments at the ILL. We will talk about some of the differences in approach between and LAMP and Mantid and the challenges this created for comparing results between them. We will also discuss the future plans for the project to address the other technique areas, and supporting instruments with moving detectors at the ILL.

[1] https://www.ill.eu/instruments-support/computing-for-science/cs-software/all-software/lamp/the-lamp-book/

[2] http://www.mantidproject.org/



##### Original (Ian)

A new team from the ILL has joined the Mantid project, building on work already undertaken to support instruments at the ILL. We will discuss the progress made in these areas, Mantid adoption on instruments and the challenges of adding a new distributed development team to the Mantid project. We will also discuss some of the future challenges that will need to be addressed for adoption of Mantid at the ILL.

##### Original (Gagik)

A new team at the ILL has joined the Mantid project, with the objective to fully implement ILL instruments support into Mantid. We present the progress made in these area, with the focus on the domains of TOF and Backscattering data reduction. Some future challenges that will need to be addressed for commisioning of Mantid at the ILL are also discussed.
