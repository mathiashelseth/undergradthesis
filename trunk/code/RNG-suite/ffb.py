#Import necessary modules
import numpy as np
import sys

#Function to normalize the data between
#greater than or equal to zero (0) and less than one (1)
#Can be written as [0, 1)
def NormalizeData(a):
    return np.interp(a, (a.min(), a.max()), (0,0.9999999999))

#Open the file given through the first argument that will be
#provided by the main program.
with open(sys.argv[1], 'rb') as f:
	#Use numpy to set each byte to an integer value
	#Which will be represented as a floating point value
    data = np.fromfile(f, '<i4')
    #Take the converted input and normalize it.
    cleaned_data = NormalizeData(abs(data))

#Print all floats with a space that is read to standard output
#This output will be interpreted by the main python program.
for float_number in cleaned_data:
    print(str(float_number) + ' ')




