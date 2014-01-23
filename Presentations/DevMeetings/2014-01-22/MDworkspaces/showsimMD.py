import os
path=r'C:\Users\Andrei Savici\Desktop\MDworkspaces'
#data
ImportMDEventWorkspace(Filename=os.path.join(path,'sim.txt'),OutputWorkspace='sim')
BinMD(InputWorkspace='sim',AxisAligned='0',BasisVector0='Qx,rlu,1,0',BasisVector1='Qy,rlu,0,1',OutputExtents='-4,4,-4,4',OutputBins='40,40',Parallel='1',OutputWorkspace='sim_rebinned')
s=plotSlice('sim_rebinned',colormin=0,colormax=10,normalization =0)
s.saveImage(os.path.join(path,'sim.png'))

ImportMDEventWorkspace(Filename=os.path.join(path,'sim1.txt'),OutputWorkspace='sim1')
BinMD(InputWorkspace='sim1',AxisAligned='0',BasisVector0='Qx,rlu,1,0',BasisVector1='Qy,rlu,0,1',OutputExtents='-4,4,-4,4',OutputBins='40,40',Parallel='1',OutputWorkspace='sim1_rebinned')
s=plotSlice('sim1_rebinned',colormin=0,colormax=10,normalization =0)
s.saveImage(os.path.join(path,'sim1.png'))

ImportMDEventWorkspace(Filename=os.path.join(path,'sim2.txt'),OutputWorkspace='sim2')
BinMD(InputWorkspace='sim2',AxisAligned='0',BasisVector0='Qx,rlu,1,0',BasisVector1='Qy,rlu,0,1',OutputExtents='-4,4,-4,4',OutputBins='40,40',Parallel='1',OutputWorkspace='sim2_rebinned')
s=plotSlice('sim2_rebinned',colormin=0,colormax=10,normalization =0)
s.saveImage(os.path.join(path,'sim2.png'))

ImportMDEventWorkspace(Filename=os.path.join(path,'norm1.txt'),OutputWorkspace='norm1')
BinMD(InputWorkspace='norm1',AxisAligned='0',BasisVector0='Qx,rlu,1,0',BasisVector1='Qy,rlu,0,1',OutputExtents='-4,4,-4,4',OutputBins='40,40',Parallel='1',OutputWorkspace='norm1_rebinned')
ImportMDEventWorkspace(Filename=os.path.join(path,'norm2.txt'),OutputWorkspace='norm2')
BinMD(InputWorkspace='norm2',AxisAligned='0',BasisVector0='Qx,rlu,1,0',BasisVector1='Qy,rlu,0,1',OutputExtents='-4,4,-4,4',OutputBins='40,40',Parallel='1',OutputWorkspace='norm2_rebinned')

#sum
MergeMD(InputWorkspaces='sim1,sim2',OutputWorkspace='sim1and2')
BinMD(InputWorkspace='sim1and2',AxisAligned='0',BasisVector0='Qx,rlu,1,0',BasisVector1='Qy,rlu,0,1',OutputExtents='-4,4,-4,4',OutputBins='40,40',Parallel='1',OutputWorkspace='sim1and2_rebinned')
s=plotSlice('sim1and2_rebinned',colormin=0,colormax=30,normalization =0)
s.saveImage(os.path.join(path,'sim1and2.png'))
#normalized then sum
sim2half=mtd["sim2"]*0.5
MergeMD(InputWorkspaces='sim1,sim2half',OutputWorkspace='sim1and2half')
BinMD(InputWorkspace='sim1and2half',AxisAligned='0',BasisVector0='Qx,rlu,1,0',BasisVector1='Qy,rlu,0,1',OutputExtents='-4,4,-4,4',OutputBins='40,40',Parallel='1',OutputWorkspace='sim1and2half_rebinned')
s=plotSlice('sim1and2half_rebinned',colormin=0,colormax=20,normalization =0)
s.saveImage(os.path.join(path,'sim1and2half.png'))
#sum then normalized
MergeMD(InputWorkspaces='norm1,norm2',OutputWorkspace='norm1and2')
BinMD(InputWorkspace='norm1and2',AxisAligned='0',BasisVector0='Qx,rlu,1,0',BasisVector1='Qy,rlu,0,1',OutputExtents='-4,4,-4,4',OutputBins='40,40',Parallel='1',OutputWorkspace='norm1and2_rebinned')
final=DivideMD("sim1and2_rebinned","norm1and2_rebinned")
s=plotSlice('norm1and2_rebinned',colormin=0,colormax=10,normalization =0)
s.saveImage(os.path.join(path,'norm.png'))
s=plotSlice('final',colormin=0,colormax=10,normalization =0)
s.saveImage(os.path.join(path,'final.png'))