# demostrating multispectra fitting

# create a test dataset
Load(r'MUSR00015189.nxs', OutputWorkspace='musr')
musr=CropWorkspace(InputWorkspace='musr', StartWorkspaceIndex=0, EndWorkspaceIndex=0)
musr_1 = Rebin('musr_1','0.5,0.1,30')
musr_2 = Rebin('musr_2','0.5,0.1,30')
musr_2 *= 2
musr_3 = Rebin('musr_2','0.5,0.1,30')
musr_3 *= 1.5
musr=GroupWorkspaces('musr, musr_3')
workspaces = ['musr_1','musr_2','musr_3']

# we will fit 3 spectra simultaneously: one from each workspace
func= """
composite=MultiDomainFunction,NumDeriv=1;(
    composite=CompositeFunction,$domains=0;
    name=LinearBackground,A0=0,A1=0,ties=(A1=0);
    name=UserFunction,Formula=Intensity*exp(-(x/Tau)^Beta),Intensity=1000.0,Tau=2,Beta=1
);
(
    composite=CompositeFunction,$domains=1;
    name=LinearBackground,A0=0,A1=0,ties=(A1=0);
    name=UserFunction,Formula=Intensity*exp(-(x/Tau)^Beta),Intensity=1000.0,Tau=2,Beta=1
);
(
    composite=CompositeFunction,$domains=2;
    name=LinearBackground,A0=0,A1=0,ties=(A1=0);
    name=UserFunction,Formula=Intensity*exp(-(x/Tau)^Beta),Intensity=1000.0,Tau=2,Beta=1
);"""

kwargs = {'InputWorkspace_2': 'musr_3', 'InputWorkspace_1': 'musr_2', 'WorkspaceIndex_1': 0, 'WorkspaceIndex_2': 0}

# do the fit
Fit(Function=func,InputWorkspace=workspaces[0],WorkspaceIndex=0,Output='output',Minimizer='Levenberg-MarquardtMD,Debug=1',**kwargs)