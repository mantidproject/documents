import h5py
from shutil import copyfile


def testFile(sourceFiles, destFile):
    for i in [1,2]:
        destFile = destFilePath + '00000' +str(i)+'.nxs'
        copyfile(sourceFiles[i-1], destFile)
        with h5py.File(destFile, "r+") as f:
            print(f['entry0'])
            # for member in f['entry0']:
            #     print member
            f['entry0/time'][0] = 123.4
            f['entry0/user/name'][0] = "ILL"
            f['entry0/user/namelocalcontact'][0] = "CS"
            f['entry0/user/proposal'][0] = "Test"
            f['entry0/run_number'][0] = i
            f['entry0/title'][0] = "Nexus Test"
            f['entry0/sample/chemicalFormula'][0] = ""
        ws = LoadILLReflectometry(Filename=destFile, OutputWorkspace=str(i))
        print(ws.getRun().getLogData('run_number').value)
        print(ws.getRun().getLogData('time').value)
        print(ws.getRun().getLogData('user.name').value)
        print(ws.getRun().getLogData('user.namelocalcontact').value)
        print(ws.getRun().getLogData('user.proposal').value)
        print(ws.getRun().getLogData('title').value)
        print(ws.getRun().getLogData('sample.chemicalFormula').value)

# Objective: Modify and save a few Nexus files (1 .. 9) for using as test data
# Usage example (insert experiment, run number, modify instrument, file location):
#sourceFiles = ['/net/serdon/illdata/181/d17/xxxxx/rawdata/xxxxx.nxs',
#        '/net/serdon/illdata/181/figaro/xxxxxx/rawdata/xxxxx.nxs']
#destFilePath = '/home/cs/xxxxx/' 
#testFile(sourceFiles, destFilePath)
