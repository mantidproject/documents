import h5py, numpy

# Choose the numors and working directory
# ASCII and NeXus should be in the same directory
numors = range(532008, 532035+1)
working_dir = '/users/bush/mantid_data/d2b/d2b_CALIB_Vana2/'

for numor in numors:
    print('Updating numor: ' + str(numor))
    f = open(working_dir  + str(numor))
    lines = f.readlines()
    date_string = numpy.array(lines[5][14:32])
    f.close()
    h = h5py.File(working_dir + str(numor) + '.nxs', 'r+')
    start_time = h['/entry0/start_time']
    print('Old start time: ' + str(start_time.value))
    h.__delitem__('/entry0/start_time')
    print('New start time: ' + str(date_string) + '|')
    h.create_dataset('/entry0/start_time', (1,), 'S18', [date_string])
    h.close()

