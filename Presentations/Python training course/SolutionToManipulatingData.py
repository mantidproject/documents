ws = Load(Filename="HRP39182.RAW")
ws = Rebin(InputWorkspace=ws, Params=1e4) 
nbins = ws.blocksize()
print nbins

xMin = ws.getDimension(0).getMinimum()
xMax = ws.getDimension(0).getMaximum()
xRange = [xMin, xMax]

''' ----------- Part One Solution using nested loop and implementing a max condition by hand ----------- '''
new_y = []
for i in range(ws.getNumberHistograms()):
	y = ws.readY(i)
	maxY = -1
	# Inner loop. Loop over bins.
	for j in range(nbins):
		current = y[j]
		if current > maxY:
			maxY = current
	new_y.append(maxY)

solution_1 = CreateWorkspace(DataY=new_y, DataX=xRange, NSpec=ws.getNumberHistograms())

''' ----------- Part One Solution  using nested loop and implementing an inbuild max function ----------- '''
new_y = []
for i in range(ws.getNumberHistograms()):
	y = ws.readY(i)
	maxY = -1.0
	# Inner loop. Loop over bins.
	for j in range(nbins):
		maxY = max(y[j], maxY) # Using the input Max method.
	new_y.append(maxY)
	
solution_2 = CreateWorkspace(DataY=new_y, DataX=xRange, NSpec=ws.getNumberHistograms())

''' ----------- Part One Solution  using single loop and numpy max function ----------- '''
new_y = []
for i in range(ws.getNumberHistograms()):
	y = ws.readY(i)
	maxY = numpy.max(y)
	new_y.append(maxY)
	
solution_3 = CreateWorkspace(DataY=new_y, DataX=xRange, NSpec=ws.getNumberHistograms())

''' ----------- Part Two Solution ----------- '''
table = CreateEmptyTableWorkspace()
table.addColumn('int', 'Spectrum Number')
table.addColumn('double', 'Max')
table.addColumn('double', 'Min')
for i in range(ws.getNumberHistograms()):
	y = ws.readY(i)
	maxY = numpy.max(y)
	minY = numpy.min(y)
	specNumber = ws.getSpectrum(i).getSpectrumNo()
	table.addRow([specNumber, maxY, minY])






