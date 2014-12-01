#
# Running an analysis Manually
#

ws = Load(Filename='164198.nxs',OutputWorkspace='data')

 
# Extracting algorithm properties
run = ws.run()
ei = run.getProperty("Ei")
print ei.value
wavelength = run.getProperty("wavelength")
print wavelength.value

Integration(InputWorkspace='data', OutputWorkspace='mon', EndWorkspaceIndex=0)

Divide(LHSWorkspace='data', RHSWorkspace='mon', OutputWorkspace='data_norm')

ConvertUnits(InputWorkspace='data',OutputWorkspace='data_DeltaE',Target='DeltaE',EMode='Direct')

Rebin(InputWorkspace='data_DeltaE', OutputWorkspace='data_E_Rebin', Params='-50,0.1,3')


