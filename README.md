# optimized-version-abfload-in-python
load specific time region from large abf file into python 
A ealier module called axonio has already implment the function that load abf file into python for general purpose.
However, unlike the abfload in matlab. axonio does not allow users to load certain time region of an abf file in gap free mode. 
I actually strongly suggest the developer can make it improved in their later versio. Reading the total length of abf is the 
only option in current version axonio. That setting is fine fore small abf file, but it is very impractical for large abf file.
This code provide a easy way to keep the same data structure as axion and allow user to load the specific time region from a large
abf file. The key step is to extract useful parameters from the headreader function in axion and set the reading initial position and
length careful in the numpy.memmap.
An example is present in test_axonread.ipynb file, ploting 12 sec data from a long time recording abf file.
