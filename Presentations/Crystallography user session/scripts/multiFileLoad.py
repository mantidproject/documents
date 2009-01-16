path = "C:/Mantid/Test/Data/"
rawfiles = ["HRP37125.RAW", "HRP38692.RAW","GEM38370.raw","GEM40979.raw"]

# Load in all files with a loop
for item in rawfiles:
	LoadRaw(path+item,item[:8])
