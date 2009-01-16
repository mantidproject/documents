def my_add(file1,file2,output):
	LoadRaw(file1,"raw1")
	LoadRaw(file2,"raw2")
	Plus("raw1","raw2",output)
	mtd.deleteWorkspace("raw1")
	mtd.deleteWorkspace("raw2")

path = "c:/MantidInstall/data/"
my_add(path+"HET15958.RAW",path+"HET15958.RAW","summed")