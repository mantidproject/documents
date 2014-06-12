#
# Instrument view
#

filename = 'D33041421_tof.nxs'

run = Load(filename)
instrument_view = getInstrumentView(run.name())
render = instrument_view.getTab(InstrumentWindow.RENDER)
render.changeColorMap('/opt/Mantid/colormaps/BlackBodyRadiation.MAP')
render.setMinValue(0)
render.setMaxValue(500) 
instrument_view.show()