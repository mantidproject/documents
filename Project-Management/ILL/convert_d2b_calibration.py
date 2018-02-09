# Magic script to convert LAMP calibration files into Mantid workspaces
import numpy as np

N_TUBES = 128
N_PIXELS = 128
N_DETECTORS = N_TUBES * N_PIXELS

f = open('/users/bush/mantid_data/d2b/calibration/d2bcal_23Nov16_c.2d')
lines = f.readlines()

# Zones - converts to a workspace with good pixel start, end pairs (one for each tube)
zones = np.zeros((N_TUBES, 2))
for i in range(2, 66):
    index = i - 2 # tube number - 1
    numbers = [int(s) for s in lines[i].split(" ") if len(s) > 1]
    zones[index * 2, 0] = numbers[0] + index * 2 * N_PIXELS
    zones[index * 2, 1] = numbers[1] + index * 2 * N_PIXELS
    zones[index * 2 + 1, 0] = numbers[2] - 128 + (index * 2 + 1) * N_PIXELS
    zones[index * 2 + 1, 1] = numbers[3] - 128 + (index * 2 + 1) * N_PIXELS

zones = CreateWorkspace(DataX=np.zeros((N_TUBES, 2)), DataY=zones, Nspec=N_TUBES)

# Detector efficiencies - converts to a 1D array with an efficency for each detector
effs = np.zeros(N_DETECTORS)
eff_count = 0
for i in range(67, 2883):
    numbers = [float(s) for s in lines[i].split(" ") if len(s) > 1]
    for number in numbers:
        effs[eff_count] = number
        eff_count += 1
        
if eff_count != N_DETECTORS:
    print("Error, unexpected number of efficencies found!")
eff = CreateWorkspace(DataX=np.zeros(N_DETECTORS), DataY=effs, Nspec=N_DETECTORS)

# Angles - converts to a 1D array with an angle for each detector
angles = np.zeros(N_PIXELS)
angle_count = 0
for i in range(2884, 2906):
    numbers = [float(s) for s in lines[i].split(" ") if len(s) > 1]
    for number in numbers:
        angles[angle_count] = number
        angle_count += 1

if angle_count != N_TUBES:
    print("Error, unexpected number of angles found!")
angles = CreateWorkspace(DataX=np.zeros(N_TUBES), DataY=angles, Nspec=N_TUBES)
