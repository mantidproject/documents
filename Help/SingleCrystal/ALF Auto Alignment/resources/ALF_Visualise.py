folder_path = "C:\Some\Log\Folder\"

xmin='-10'
xmax='10'
ymin='-10'
ymax='10'
zmin='-10'
zmax='10'

# Get Flux & Solid Angle Matrices from Vanadium run
# ##########################################################

print "Loading vanadium run..."
ws_van = "ALF_Vanadium"
ws_van_max = "ALF_Vanadium_FindMax"
ws_van_sa = "ALF_Vanadium_SolidAngle"
ws_van_flux = "ALF_Vanadium_Flux"
ws_mask = "ALF_Mask"

Load(Filename= folder_path + "ALF68014.raw", OutputWorkspace = ws_van)
ConvertUnits(InputWorkspace=ws_van, Target='Momentum', OutputWorkspace = ws_van)

num_tubes = 24
tube_size = 64
# Mask top 3 and bottom 3 spectra per tube
MaskDetectors(ws_van, ','.join(['{0}-{1},{2}-{3}'.format(i*tube_size+1, i*tube_size+3, i*tube_size+62, i*tube_size+64) for i in range(num_tubes)]))
# Mask first and last tube
MaskDetectors(ws_van, '1-65, 1472-1535')
ExtractMask(ws_van, OutputWorkspace=ws_mask)

# Crop undefined detectors
CropWorkspace(InputWorkspace=ws_van, StartWorkspaceIndex=0, EndWorkspaceIndex=1535, OutputWorkspace = ws_van)

# Find bounds for momentum range
ws_van_max = Rebin(InputWorkspace=ws_van, Params="0,0.05,20")
ws_van_max = ConvertToPointData(ws_van_max)
ws_van_max = SumSpectra(ws_van_max)
ys = ws_van_max.readY(0)

# Momentum value threshold is one tenth of peak
threshold = ys.max(axis=0) / 10

# Get lower and upper index with value above threshold
lower = ys.searchsorted(threshold)
upper = len(ys) - ys[::-1].searchsorted(threshold)

kmin = ws_van_max.readX(0)[lower]
kmax = ws_van_max.readX(0)[upper]
DeleteWorkspace(ws_van_max)

# Create Solid Angle Workspace
Rebin(InputWorkspace = ws_van, Params = str(kmin) + "," + str(kmax-kmin) + "," + str(kmax), OutputWorkspace = ws_van_sa)

# Create Flux Workspace
Rebin(InputWorkspace = ws_van, Params = str(kmin)+',0.005,'+str(kmax), OutputWorkspace = ws_van_flux)
SumSpectra(InputWorkspace = ws_van_flux, OutputWorkspace = ws_van_flux)
IntegrateFlux(InputWorkspace = ws_van_flux, OutputWorkspace = ws_van_flux)

print "- - - - - - - - - - - - - - - - - - - -"


# Load, convert & normalise scan data
# ##########################################################

if mtd.doesExist('MDnorm_acc'):
    DeleteWorkspace('MDnorm_acc')
if mtd.doesExist('MDdata_acc'):
    DeleteWorkspace('MDdata_acc')
    
range_min = 75243
range_max = 75264
# For each sample rotation
for i in range(range_min, range_max+1):
    # Prepare dataset
    current_ws = "ALF" + str(i)
    current_md = "MD_" + current_ws
    current_mom = "Momentum_" + current_ws
    print "Loading Run " + str(i) + "..." 
    Load(Filename= folder_path + "ALF" + str(i) + ".raw",OutputWorkspace=current_ws)
    MaskDetectors(current_ws, MaskedWorkspace=ws_mask)
    CropWorkspace(InputWorkspace=current_ws, StartWorkspaceIndex=0, EndWorkspaceIndex=1535,OutputWorkspace=current_ws)
    
    # Set UB Matrix and goniometer information needed for merge
    SetGoniometer(Workspace=current_ws, Axis0="rrot, 0, 1, 0, 1")
    
    # Convert & Crop
    ConvertUnits(InputWorkspace=current_ws, Target='Momentum',OutputWorkspace=current_mom)
    Rebin(InputWorkspace = current_mom, Params = str(kmin)+',0.005,'+str(kmax),OutputWorkspace=current_mom)
    
    # Convert to MD
    print "Converting to MDWorkspace..."
    pars=dict()
    pars['QDimensions']='Q3D'
    pars['dEAnalysisMode']='Elastic'
    pars['Q3DFrames']='AutoSelect'
    pars['PreprocDetectorsWS']='preprDetMantid'
    pars['MinValues']=xmin+','+ymin+','+zmin
    pars['MaxValues']=xmax+','+ymax+','+zmax
    pars['SplitInto']=100
    pars['MaxRecursionDepth']=1
    pars['MinRecursionDepth']=1
    pars['InputWorkspace']=current_mom
    pars['OutputWorkspace']=current_md
    ConvertToMD(**pars)
    
    # Normalise
    print "Normalise MD Workspace..."
    MDdata, MDnorm = MDNormSCD(InputWorkspace=current_md,
            AlignedDim0='Q_sample_x,'+xmin+','+xmax+',100',
            AlignedDim1='Q_sample_y,'+ymin+','+ymax+',100',
            AlignedDim2='Q_sample_z,'+zmin+','+zmax+',100',
            FluxWorkspace=ws_van_flux,
            SolidAngleWorkspace=ws_van_sa,)
   
    # Add to accumulated data / normalisation workspaces
    if mtd.doesExist('MDdata_acc'):
        MDdata_acc = MDdata_acc + MDdata
    else:
        MDdata_acc = CloneMDWorkspace(MDdata)
    if mtd.doesExist('MDnorm_acc'):
        MDnorm_acc = MDnorm_acc +  MDnorm
    else:
        MDnorm_acc = CloneMDWorkspace(MDnorm)
        
    print "Finished processing " + current_md
    DeleteWorkspace(current_mom)
    print "- - - - - - - - - - - - - - - - - - - -"

# Step 3 - Create workspace merging all normalized data
# ##########################################################
print "Creating merged normalised workspace..."

MD_merged_normalised = MDdata_acc/MDnorm_acc

print "Done."

            