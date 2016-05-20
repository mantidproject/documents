## ILL Backscattering Scripts Examples

These scripts are from the [Indirect ILL Reduction](http://docs.mantidproject.org/nightly/algorithms/IndirectILLReduction-v1.html) documentation page. File `ILLIN16B_034745.nxs` is contained in the external data for the Mantid unit tests - `ExternalData/Testing/Data/UnitTest`.

### Running Standard IndirectILLReduction

```python
IndirectILLReduction(Run='ILLIN16B_034745.nxs',
                     RawWorkspace='raw_workspace',
                     ReducedWorkspace='reduced_workspace')

print "Reduced workspace has %d spectra" % mtd['reduced_workspace'].getNumberHistograms()
print "Raw workspace has %d spectra" % mtd['raw_workspace'].getNumberHistograms()

```

### Running IndirectILLReduction in mirror mode

```python
IndirectILLReduction(Run='ILLIN16B_034745.nxs',
                     RawWorkspace='raw_workspace',
                     ReducedWorkspace='reduced_workspace',
                     LeftWorkspace='reduced_workspace_left',
                     RightWorkspace='reduced_workspace_right',
                     MirrorMode=True)

print "Raw workspace has %d spectra" % mtd['raw_workspace'].getNumberHistograms()
print "Reduced workspace has %d spectra" % mtd['reduced_workspace'].getNumberHistograms()
print "Reduced left workspace has %d spectra" % mtd['reduced_workspace_left'].getNumberHistograms()
print "Reduced right workspace has %d spectra" % mtd['reduced_workspace_right'].getNumberHistograms()

```

