# optimized-version-abfload-in-python
load specific time region from large abf file into python.

An ealier module called axonio has already implemented the function loading abf file into python for general purpose.
However, unlike the abfload in matlab. axonio does not allow users to load certain time region of an abf file in gap free mode. 
I actually strongly suggest the Axonio developer improve it in their later version. Reading the total length of abf is the 
only option in current version axonio. Such setting is fine for small abf files, but it is very inconvenient and impractical for large abf files.
This code provides an easy way to load the data of specific time region from a large abf file. The key step or the main optimization is to extract useful parameters from the headreader function in axonio and optimize the read position and length settings with numpy.memmap. I tried to keep this code follow axonio's data structure and function flows.

An example is presented in test_axonread.ipynb file, ploting 12 sec data from a long time recording abf file.

![figure_1](https://cloud.githubusercontent.com/assets/19654472/19011742/9dc59a16-876d-11e6-9773-fa8b5f17366e.png)

