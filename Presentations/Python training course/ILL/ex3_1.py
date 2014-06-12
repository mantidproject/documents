#
# Graphing
#

filename = '164198.nxs'

run = Load(filename)
graph1 = plotSpectrum(source=run, indices=205)
graph2 = plotSpectrum(source=run, indices=209)
mergePlots(graph1, graph2)
layer = graph1.activeLayer()
layer.setAxisScale(Layer.Bottom, 4400, 5000)
layer.logYlinX()
