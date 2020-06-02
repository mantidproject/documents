Agenda
======

Pinned Topics
-------------
* Review any outstanding external [pull request](https://github.com/mantidproject/mantid/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+-label%3A%22State%3A+In+Progress%22) or [issues](https://github.com/mantidproject/mantid/issues)?
* Any updates to [tracking design table](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/reports/TSC-TrackingDesignProposals.md)?
* Find volunteer for presentation at next mantid review meeting

New Items
---------

ACTION ALL, please come to the meeting with an understanding of how masking is used at your facility.

* Masking and Reversible detector masking
  * We have Masking implemented in two ways at the moment
  * "Traditional" masking - Mask flag is set and data is cleared
    * MaskDetectors, MaskDetectorsInShape, InstrumentView "Apply To Data"
    * most algorithms and tools expect this and do not check the mask flag
  * reversible masking - Only the mask flag is flipped and the data left in place
    * most algorithms will not handle this properly
    * Algorithms that do this: MaskDetectorsIf, ClearMaskedSpectrum, MaskInstrument
  * This has already caused confusion in the development team, and must be worse for users
    * We should agree a single way forward
  
* Reducing the number of open issues
  * Number of issues has crept up from ~800 to ~2000 over the last 3 years
  * Mantid Plot tagged issues accounts for ~500, leaving us with 1500
  * Asking devs to close older issues isn't working fully
    * Typically bug still exists so they can't close, but equally they won't ever get round to fixing
    * Some are duplicates that are fixed, but finding these is a challenge with the other 1499 issues
   * Other large open source projects have automated policies for dealing with this:
     * Some will close all issues after n months whilst moving all features to a separate long-term list
     * Some will automatically close inactive issues (no comments) after n months
     * Some close anything the aren't planning on doing this in x months or cannot afford dev time to do it within y months
     * Something else?
   * Discussion:
     * Is this worth comitting resources to resolving?
     * If so, how should we do this and when?

Minutes
-------

  
