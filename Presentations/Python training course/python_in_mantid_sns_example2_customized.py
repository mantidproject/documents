load_alg = LoadDialog(OutputWorkspace='run',LoadMonitors='1')
filename = load_alg.getProperty('Filename').value
logger.information("Filename is: " + filename)

ConvertUnits(InputWorkspace='run_monitors',OutputWorkspace='run_monitors_lam',Target='Wavelength')

rebin_alg = RebinDialog(Message="Rebin the monitors by providing rebin parameters", InputWorkspace='run_monitors_lam',
				    OutputWorkspace='run_monitors_lam_rebinned',Params='2.5,0.1,5.5', Enable='Params')
				    
params = rebin_alg.getProperty('Params').value

ConvertUnits(InputWorkspace='run',OutputWorkspace='run_lam',Target='Wavelength')
Rebin(InputWorkspace='run_lam',OutputWorkspace='run_lam_rebinned',Params=params)

SumSpectra(InputWorkspace='run_lam_rebinned', OutputWorkspace='run_lam_summed')
Divide(LHSWorkspace='run_lam_summed', RHSWorkspace='run_monitors_lam_rebinned', OutputWorkspace='normalized')
