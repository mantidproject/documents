#script: multiple downhill fitting

from random import random
from time import sleep

startX = 93000
endX = 93300
#Fit(InputWorkspace='HRP39182', WorkspaceIndex=0, \
#	   StartX = startX, EndX=endX, Output='fit', \
#	   Function='name=Gaussian,Height=10,PeakCentre=93150,Sigma=20')


chiSqBest = 1e+100

for i in range(10):
	tryCentre = str(startX + random()*(endX-startX))
	d0, chiSq, d1, d2, d3 = Fit(InputWorkspace='HRP39182', WorkspaceIndex=0, \
	   StartX = startX, EndX=endX, Output='fit', \
	   Function='name=Gaussian,Height=10,PeakCentre='+tryCentre+',Sigma=20')
	   
	if chiSq < chiSqBest:
		chiSqBest = chiSq
		CloneWorkspace(InputWorkspace='fit_Workspace',OutputWorkspace='fitBest')
		
	print chiSq
	sleep(2)



