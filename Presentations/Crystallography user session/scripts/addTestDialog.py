def my_add(output):
	LoadRawDialog(OutputWorkspace="raw1")
	LoadRawDialog(OutputWorkspace="raw2")
	Plus("raw1","raw2",output)
	mtd.deleteWorkspace("raw1")
	mtd.deleteWorkspace("raw2")

my_add("summed")
