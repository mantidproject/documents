# 
# Write a program that prints out the first 25 Fibonacci numbers. (The Fibonacci sequence starts as with 0,1 and next number is the sum of the two previous numbers)
# Extend the program to also print the ratio of successive numbers of the sequence.
# 

# prev_2 - One before previous number
# prev_1 - Previous number
prev_2, prev_1 = 0, 1

# Already have first 2 terms above
print prev_2
print prev_1

# Now the next 23 terms (range(0,23) will run the loop 23 times)
for i in range(0,23):
    current = prev_2 + prev_1
    print current,
    # Ratio to previous
    print "ratio to previous=",float(current)/prev_1
    # Move the previous markers along one for the next time around
    prev_2 = prev_1
    prev_1 = current
