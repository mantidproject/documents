run = Load('PG3_4871_event')
nevents = run.getNumberEvents()
logger.information(str(nevents))
filtered = FilterBadPulses(run, LowerCutoff=99.5)
aligned = AlignDetectors(InputWorkspace=filtered, CalibrationFile='PG3_Golden.cal')
rebinned = Rebin(InputWorkspace=aligned, Params=[1.4,-0.0004, 8])
focused = DiffractionFocussing(InputWorkspace=rebinned, GroupingFileName='PG3_Golden.cal')
compressed = CompressEvents(InputWorkspace=focused)
nevents = compressed.getNumberEvents()
logger.information(str(nevents))