import numpy as np
# make these smaller to increase the resolution
dx, dy = 0.2, 0.2

# generate 2 2d grids for the x & y bounds
y, x = np.mgrid[slice(-4, 4 + dy, dy),
                slice(-4, 4 + dx, dx)]

z = np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)


z=(z*5+5).astype(int)
z[np.where(z<0)]=0

size=len(z)
n1=0.*x+1
z1=z*1.0
z1[np.where(y<-2)]=0
n1[np.where(y<-2)]=0
z2=z*2.0
n2=0.*x+2
z2[np.where(y>2)]=0
n2[np.where(y>2)]=0

#z[np.where(x>3)]=0
z1[np.where(x>3)]=0
z2[np.where(x>3)]=0
n1[np.where(x>3)]=0
n2[np.where(x>3)]=0


f1=open("sim.txt","w")
f1.write("DIMENSIONS\n")
f1.write("Qx Qx rlu 40\n")
f1.write("Qy Qy rlu 40\n")
f1.write("MDEVENTS\n")
#f1.write("#")
for i in range(size):
    for j in range(size):
        for ev in range(int(z[i][j])):
            f1.write("1.\t1.\t1\t1\t"+str(x[i][j])+"\t"+str(y[i][j])+"\n")
f1.close()

f1=open("sim1.txt","w")
f1.write("DIMENSIONS\n")
f1.write("Qx Qx rlu 40\n")
f1.write("Qy Qy rlu 40\n")
f1.write("MDEVENTS\n")
#f1.write("#")
for i in range(size):
    for j in range(size):
        for ev in range(int(z1[i][j])):
            f1.write("1.\t1.\t1\t1\t"+str(x[i][j])+"\t"+str(y[i][j])+"\n")
f1.close()

f1=open("sim2.txt","w")
f1.write("DIMENSIONS\n")
f1.write("Qx Qx rlu 40\n")
f1.write("Qy Qy rlu 40\n")
f1.write("MDEVENTS\n")
#f1.write("#")
for i in range(size):
    for j in range(size):
        for ev in range(int(z2[i][j])):
            f1.write("1.\t1.\t1\t1\t"+str(x[i][j])+"\t"+str(y[i][j])+"\n")
f1.close()

f1=open("norm1.txt","w")
f1.write("DIMENSIONS\n")
f1.write("Qx Qx rlu 40\n")
f1.write("Qy Qy rlu 40\n")
f1.write("MDEVENTS\n")
#f1.write("#")
for i in range(size):
    for j in range(size):
        if(n1[i][j]>0):
            f1.write("1.\t0.\t1\t1\t"+str(x[i][j])+"\t"+str(y[i][j])+"\n")
f1.close()

f1=open("norm2.txt","w")
f1.write("DIMENSIONS\n")
f1.write("Qx Qx rlu 40\n")
f1.write("Qy Qy rlu 40\n")
f1.write("MDEVENTS\n")
#f1.write("#")
for i in range(size):
    for j in range(size):
        if(n2[i][j]>0):
            f1.write("2.\t0.\t1\t1\t"+str(x[i][j])+"\t"+str(y[i][j])+"\n")
f1.close()


