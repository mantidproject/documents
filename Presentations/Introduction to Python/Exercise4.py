## Exercise 4
#   1.  Build a list containing the 5 filenames of the text files that are going to be used.
#       (Hint: Can be done by hand or using the os.listdir() function in the os module)
#   2. Add a bogus file name that doesn't exist to the list (so that we have to do some error handling)
#   3. Loop over the list and for each file (Remember here that we have a non existent file in the list and calling open
#      on this will result in an IOError exception that needs to be dealt with)
#         1. Open the file;
#         2. Loop over each line;
#         3. Split the line up into sections (Hint: The string has a .split() function that splits the string on
#            whitespace and gives back a list with each section as an element of the list)
#         4. Convert the second column value into an integer
#         5. Keep track of the values for each line and compute an average for the file. 
#   4. Finally, print out a list of file,average-value pairs 
import os

file_dir = "C:\\MantidInstall\\data\\"
file_names = os.listdir(file_dir)
file_names.append('nonexistant.txt')
average_store = {}
print 'Computing average for log files in directory "' + file_dir + '"'
for name in file_names:
    # Skip all no text files
    if name.endswith('.txt') == False:
        continue
    try:
        file_handle = open(os.path.join(file_dir,name), 'r')
    except IOError:
        print '\tError: No such file: "' + name + '". Skipping file'
        continue
    print '\tReading file',name
    # At this point we have an open file
    average = 0.0
    nvalues = 0
    line_counter = 1
    for line in file_handle:
        columns = line.split()
        if len(columns) == 2:
            average += float(columns[1])
            nvalues += 1
        else:
            print '\tWarning: Unexpected file format encountered in file"',name,'" on line',line_counter
        line_counter += 1

    average /= nvalues
    average_store[name] = average
    file_handle.close()

# Print out file averages
column_width = 30
print
print '-'*column_width*2
print 'File'.center(column_width) + '|' + 'Average'.center(column_width)
print '-'*column_width*2
for key, value in average_store.iteritems():
    print key.center(column_width) + '|' + str(value).center(column_width)    
