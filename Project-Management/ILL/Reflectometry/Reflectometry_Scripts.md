## ILL Reflectometry Scripts

### Example script for D17

Data - [D17_example_files.zip](https://www.ill.eu/fileadmin/users_files/img/instruments_and_support/support_facilities/computing_for_science/Computing_for_Science/Data_analysis/D17_example_files.zip)

```python
def load_and_convert_data(filename):
    # Load
    ws = Load(filename)
    # Scale by monitor
    ws = Scale(ws, 1.0 / ws.getRun().getLogData("monitor1.monsum").value, "Multiply")
    # Integrate
    ws = SumSpectra(InputWorkspace=ws, StartWorkspaceIndex=201, EndWorkspaceIndex=205)
    # Convert
    ws = ConvertUnits(InputWorkspace=ws, Target='Wavelength', AlignBins=True)
    # Rebin
    ws = Rebin(InputWorkspace=ws, Params='2,0.1,27')
    # Set workspace name
    RenameWorkspace(ws, 'ws_' + filename)

# Direct beam raw data file
load_and_convert_data('161875')

# Raw data file (Ni)
load_and_convert_data('161876')

# Divide by direct beam
DataByDB = Divide(LHSWorkspace='ws_161876', RHSWorkspace='ws_161875', WarnOnZeroDivide=False)
DataByDB_Q = ConvertUnits(InputWorkspace=DataByDB, Target='MomentumTransfer', EMode='Direct', AlignBins=True)

# Plot output
plotSpectrum(DataByDB_Q,  0, error_bars=True)
```
