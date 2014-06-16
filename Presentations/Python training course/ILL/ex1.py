# Only edit this bit!

dataFileNames = ['164198','164199','164200']
mergedWorkspaceName = 'data_merged'

spectraListToMask = [1,2,3,4,5,6,11,14,30,69,90,93,95,97,175,184,190,215,216,217,251,252,253,255,289,317,335,337]

transmission  =  0.95  # Sample transmission

############


# Load Samples

for file in dataFileNames:
    fullPath = file+'.nxs'
    Load(Filename=fullPath,OutputWorkspace=file)

# Merge runs
if len(dataFileNames) > 1 :
    fileNamesToMerge = ','.join(map(str,dataFileNames))
    MergeRuns(InputWorkspaces=fileNamesToMerge,OutputWorkspace=mergedWorkspaceName)

#remove bad spectra
MaskDetectors(Workspace=mergedWorkspaceName,SpectraList=spectraListToMask)

# Calculate transmission
MultiplyRange(InputWorkspace=mergedWorkspaceName,OutputWorkspace='Data_t',Factor=transmission)

# Convert from TOF to DeltaEnergy
ConvertUnits(InputWorkspace='Data_t',OutputWorkspace='Data_t_DeltaE',Target='DeltaE',EMode='Direct')

# DetectorEfficiencyCorUser needs units in DeltaE
DetectorEfficiencyCorUser(InputWorkspace='Data_t_DeltaE',OutputWorkspace='Data_t_DeltaE_effc')

