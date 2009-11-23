#
# Write a program that prints out the square of the first
# 20 integers a block such that the block has a dimension of 4x5.
#

# range(i,j) produces a list of numbers from i -> j-1
for i in range(1,21):
    print str(i*i).center(3), # center is a function for strings that centers the contesnt to the given width
    if i % 4 == 0:
        print

# ------------ Produces -------------
# 1   4   9   16
# 25  36  49  64
# 81 100 121 144
#169 196 225 256
#289 324 361 400
