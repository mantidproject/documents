## Meeting notes - 2018/04/27 - Mantid Debrief

Participants:  B. Fak, S. Rols, J. Ollivier, Q. Berrod, T. Seydel, M. Appel, G. Cuello, A. Cabrera, T. Hansen, S. Savvin, P. Mutti, V. Reimund, A. Soininen, G. Vardanyan, M. A. Gonzalez

### Points discussed: 

* Isolated issues login to the new machines: There have been just a few cases and the IT service found that they were related to some old login scripts (.bashrc and similar). 

* Network problems: Serious issues in in4lnx, difficulting enormously working with Mantid. Problems also found in in5lnx and in6lnx. Recently IT has found that there is a problem with the management of the network card by the Linux kernel of the new machines when working at 1 Gb/s. An upgrade of the kernel system seems to correct the problem, so the same upgrade will be applied to all the machines during the reactor shutdown. At the same time, Mantid will be updated to the last stable release (3.12.1) and the last available nightly build will be installed alongside.

* It is not yet clear if all the problems encountered at IN4 are related to the network card problem, but hopefully this upgrade will provide a more stable environment.

* Mantid use: Only IN4 and IN5 have used Mantid routinely during this reactor cycle. At IN6, the LLB team has been "familiarising" with the instrument and using Lamp (but need to check with Marek and Mohamed, not present, if they have used it). At IN16B, most of the time has been used for the commisioning of BATS. At D2B, Gagik has been present during a 1-day experiment and he has used Mantid with Gabriel. None of the reflectometry responsibles were in the meeting, so we still need to check if Mantid has been used or tested at all in D17 and Figaro.

* User experience at IN4: About 25% of the users refuse to use Mantid, another quarter used it and were comfortable with Mantid and quite happy with their experience and about half of the users had "mixed feelings" about Mantid.

* Problems, suggestions: Bjorn has a list of points that should be addressed. He will transmit it to Antti. 

* The question of accessing the right directories to read the data and write the results was mentioned. This is not a blocking point, as any user can set the working directory where Mantid output will be written and any number of data directories with the "Manage User Directories". We need to decide if it is enough to educate the users to pay attention to this when the First Time Setup appears, or if something more evident (similar to the Nomad experiment selection at the start of each experiment) needs to be done. 

* Bjorn mentioned that current TOF reduction scripts are too "scaring" for some users. We still need to keep them for debugging and to perform non standard reductions, but a simplified version for non-expert users is needed. Ideally, also simple user interfaces should be developed. 

* Having a history associated with each plot (similar to the workspace history) would be appreciated.

* Increasing Mantid use: Agreed that shifting from current tools to Mantid demands an additional effort, which in some cases can be significant. Proposed to perform a few experiments together (instrument scientist + user + someone from CS) during next cycle to help with this. It would be also good to compile some representative cases of experiments done during the first cycle and redo the analysis together using Mantid.

* Other issues: The RAM memory of the present in5lnx machine is not enough to deal correctly with single crystal experiments, where a single measurement can consist of 100-200 data acquisitions (e.g. 100 x 10^5 pixels x 1024 channels). This is not strictly an ILL-Mantid problem, but needs to be taken into account. A similar situation will affect Panther and IN6-Sharp in the future. Computers with at least 256 Gb of memory (maybe even up to 1 Tb as in SNS) could be needed.

* A related problem could be how to plot big quantities of data. Matplotlib is not adapted for such task and this point needs to be addressed in Mantid 4 (which is the current plan?). QtiPlot is reasonably fast, but it is not well documented and its user community is decreasing. Are there any other good options?

