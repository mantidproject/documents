### Data Reduction at the ILL: A Comparison Between Mantid and Lamp

**Type: Poster, Track: Distributed Development**

#### Antti Soininen<sup>1</sup>, Gagik Vardanyan<sup>1</sup>, Ian Bush<sup>1,2</sup>, Verena Reimund<sup>1</sup>

1. Institut Laue-Langevin, Grenoble, France
2. Tessella plc, Abingdon, Oxfordshire, UK

The ILL have begun a project to phase out the use of their existing data reduction software, LAMP [1], and begin to use the Mantid Framework [2]. Some of the first work being undertaken in the Mantid adoption project is to compare the reduction output between LAMP and Mantid. In some cases, such as loading of the raw data, a perfect agreement would be expected between LAMP and Mantid. In other cases it might be expected that there will be differences in the data, but where this is the case the reasons for such differences should be understood.

LAMP has been in use for over 20 years at the ILL, and there are a number of differences in the workflows instrument scientists use when compared with the other facilities that use Mantid. This has led to a number of changes and additions in the Mantid software from the ILL. We will show some of these that were required to make the comparisons, and how we have kept such algorithm changes as general as possible, so they can be used by other facilities.

Initial work on adoption has been for Time-of-Flight spectroscopy (IN4, IN5 and IN6) and Backscattering (IN16B) at the ILL. In this presentation we will present some details of the work comparing the output of LAMP and Mantid for some of these instruments. We will show some of the different approaches in use between LAMP and Mantid for various reduction routines, for example in the S(Q, &omega;) conversion. We will also provide some discussion of the efficiency of the different approaches for the more computationally expensive algorithms.

[1] https://www.ill.eu/instruments-support/computing-for-science/cs-software/all-software/lamp/the-lamp-book/

[2] http://www.mantidproject.org/

##### Alternative (Gagik)

The ILL have begun a project to replace their existing data reduction software, LAMP [1], with the Mantid Framework [2]. Some of the first work being undertaken in the Mantid adoption is to compare the reduction output between LAMP and Mantid. In some cases, such as loading of the raw data, an identical output could be expected. In more complicated scenarios some differences are expected, but the reasons for that should be understood.

LAMP has been in use for over 20 years at the ILL, and there are a number of alterations in the reduction workflows compared with the other facilities using Mantid. This has led to a set of adjustments and additions in the Mantid software in order to make direct comparisons possible.

Initial effort on Mantid integration at ILL has been for Time-of-Flight (IN4, IN5 and IN6) and Backscattering (IN16B) spectroscopies. We present detailed comparisons between the output of LAMP and Mantid for some of these instruments. We discuss some of the different approaches used in LAMP and Mantid for various reduction routines, for example in the S(Q, &omega;) conversion. We also summarise the efficiency of the different approaches for some of the more computationally expensive algorithms.


-----------------------------

##### Original (Ian)

At the ILL Mantid is being introduced for neutron data reduction, with a view to eventually replace the existing Lamp software. We present some work discussing the differences and similarities in approach between Lamp and Mantid, and a comparison of data reduction treatments for Time-of-Flight Spectroscopy and Backscattering data. We will also discuss some of the changes required in Mantid to allow like-for-like comparisons to be made.

##### Original (Gagik)

At the ILL Mantid is being introduced for neutron data reduction and analysis, with a view to eventually replace the existing Lamp software. We discuss some of the general differences and similarities between the methodologies adopted therein. More detailed comparison of data reduction treatments for Time-of-Flight Spectroscopy and Backscattering data is presented. Few adjustments required in Mantid to allow like-for-like comparisons with Lamp are also summarised.

