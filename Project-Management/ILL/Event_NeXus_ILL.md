# Event NeXus Design Ideas for the ILL

## Overview

The base class for holding event data (or list data) in a NeXus file is [`NXevent_data`](http://download.nexusformat.org/sphinx/classes/base_classes/NXevent_data.html). This class is currently used for storing the event data at ISIS and the SNS. In the Mantid framework this data is loaded via the [`LoadEventNexus`](http://docs.mantidproject.org/nightly/algorithms/LoadEventNexus-v1.html) algorithm, where the same algorithm is used for both SNS and ISIS data. Experimental MPI support has recently been added to this algorithm to support the ESS's future needs.

## Example Event NeXus Files

[Click to download a set of example event NeXus files.](https://www.dropbox.com/s/xod95lwrei4napw/Event%20NeXus%20Examples.zip?dl=1) This contains 2 SNS files for HYSPEC and CNCS, and 3 ISIS example files for OFFSPEC, LARMOR and SANS2D.

## File Structure

The event NeXus files are generally identical to the non-event NeXus files, with additional entries for the event data, but all other information recorded as for histogram only NeXus files. Hence they can be loaded either with LoadEventNeXus or the usual loader for the files. At the SNS event files are denoted by ending in `_event.nxs`.

The `NXevent_data` class needs to be created within the NeXus file, this can be created alongside the normal histogram data. For example the SNS `/entry/bankN` is used for the `NXdata` class and `/entry/bankN_events` is used, where N is the bank number. ISIS have a single `NXevent_data` class in their NeXus files, which is always written to `/raw_data_1/detector_1_events`, while SNS write one `NXevent_data` class per bank.

If an `NXevent_data` class is present then the loader in Mantid will default to `LoadEventNeXus`, but this is configurable to whether the event loader or standard loader takes priority.

## Minimal Requirements for `NXevent_data`

The following needs to be contained in the `NXevent_data` class:

 * `event_id` (size `NEvents`) - provides a way of mapping the event to the detector. This could be a detector ID, see below for further discussion.
 * `event_time_offset` (size `NEvents`) - a list of timestamps for each event. These are relative to the `event_time_zero` entry. In Mantid these are currently need to be in units of microsecond and of type Float32.
 * `event_time_zero` (size `NPulses`) - the start time of each pulse. This is given as an offset from an offset attribute on the entry, which is an ISO 8601 timestamp (e.g. `2018-03-25T12:08:37+02:00`). The units should be given, but Mantid currently assumes seconds (stored as 64-bit floating point).
 * `event_index` (size `NPulses`) - this gives an index into `event_id` and `event_time_offset` for when the current pulse started. For example if the first values are 0, 39, 89... then the first pulse corresponds to events 0 - 38 in `event_id` and `event_time_offset`, the second pulse 39 - 88 etc.

Here `NEvents` it the number of neutron events, and NPulses is the number of pulses (could be chopper pulses, or just number of times a new `event_time_zero` is required to be written).

The following is useful to have in the file, but not essential:

 * `total_counts` - the total number of counts, this is used by Mantid if it exists, if not the total number of counts is assumed to be the size of the first dimension for the `event_id `entry.

The SNS files `CNCS_7860_event.nxs` and `LARMOR00013065.nxs` provide good examples of the `NXevent_data` entry.

## Event ID to Detector ID Mapping

The SNS event NeXus files write event IDs as detector IDs (TBC if this is correct), ISIS write a mapping from spectra to detector IDs in the `isis_vms_compat` entry.

The event ID could be written as the detector ID used in Mantid for the ILL instruments. For counts or histogram data a mapping is used to associate the counts or histograms to a detector ID in Mantid, defined by the loader for the ILL data and the Mantid Instrument Definition file. The mapping used in Mantid for the ILL instrument can vary depending on the technique or instrument, but generally starts at 1 and goes along tubes from bottom to top, and then can go in either increasing or decreasing scattering angle.

Ideally in the event NeXus files we will be able to write the detector IDs, as used in Mantid, as the event IDs. These will need to be set correctly for each technique (and possibly instrument).

Alternatively an arbitrary event ID could be written, and a mapping to the correct detector ID could be used. This mapping could be written in the NeXus files themselves, or alternatively be part of the instrument parameters in Mantid.

## Time Series Logs for Metadata

To record meta-data that varies with time the [NXlog class](http://download.nexusformat.org/sphinx/classes/base_classes/NXlog.html) can be used in the NeXus file. These logs can be used whether working with histogram data or event data. They are used at ISIS and SNS and are well supported in Mantid, giving quick access to the statistics for the log - see [TimeSeriesProperty](http://docs.mantidproject.org/nightly/api/python/mantid/kernel/TimeSeriesProperty.html).

To write the times series log the following is needed:

 * time (size `N`) - the time of the logged entry, relative to a start attribute which is an ISO8601 timestamp (e.g. `2018-03-25T12:08:37+02:00`). Units should also be set, currently minutes and seconds are supported in Mantid (`s`, `second`, `seconds` or `minutes`).
 * value (size `N`) - the value corresponding to the time, units should also be set.

`N` is the number of changes logged. These are the only `NXlog` entries used in Mantid, but other logs are supported in the NeXus standard so `raw_value`, `average_value`, `minimum_value`, `maximum_value` etc. can be written for convenience.

A good example is in the file `CNCS_7860_event.nxs`, for the entry `/entry/DASlogs/SampleTemp/`.

## Compression

ISIS apply gzip level 1 compression to the data, while SNS apply gzip level 6. It is worth benchmarking the performance for larger instruments with both, but for the ILL higher compression levels (smaller file sizes) are likely to be beneficial for transferring and storing the data.

For a LARMOR example file (`LARMOR00013065.nxs`) there are 6 715 256 events, and the file size is 47.4 MB. This works out as ~56 bits per event, including all the additional metadata. This is with the lowest level of compression, so a smaller file is still possible.
