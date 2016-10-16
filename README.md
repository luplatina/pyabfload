# optimized-version-abfload-in-python
Use python to efficiently load specific time region from large abf file.

##OVERVIEW
abf (Axon Binary File) format is created for the storage of binary experimental data. It originates with the pCLAMP suite of data acquisition and analysis programs. It is widely used in Electrophysiology data aquisition. As a typical issue for data aquisition, large file size sometimes creat a memory problem, if the users only want to read and analyze a small segment from a large abf file. Such problem is inevitable for abf file in gap-free mode, as with the highest sampling rate in pCLAMP, 30mins recording can generate over 1GB abf data easily. Reading such entire file into memory is inconvinient and impractical. 
A previous module called [axonio](https://pythonhosted.org/neo/io.html) has already implemented the function loading abf file into python for general purpose. However, unlike the abfload in matlab. axonio does not allow users to load certain time region of an abf file in gap free mode. I actually strongly suggest the Axonio developer improve it in their later version.

##CORE IDEA OF THIS CODE
This code provides an easy way to load the data of specific time region from a large abf file. A reasonable solution is to extract the key information from abf headfile and apply them into numpy.memap, which allowes reading small segments of large file without loading the entire file into memory. 
numpy.memap creates a memory-map to an array stored in a binary file on disk. Memory-mapped files are used for accessing small segments of large files on disk without reading the entire file into memory. But it require user to specify the starting and ending position of the target data segment in the binary file.
abf file has a proprietory design on its file format. its header is separated from its main data and include all the abstract information about the data, like sampling rate, channel number. These are key imput variable to make numpy.memap work for reading abf file.

![abf file structure](https://cloud.githubusercontent.com/assets/19654472/19421453/9750eb54-93cf-11e6-8afd-473723f56554.png)

Based on the structure of the abf file shown above, I extracted several key parameters from head file and optimized the read position and length settings with numpy.memmap. I tried to keep this code follow axonio's data structure and function flows. axonio has very good "read_header" function. 


##EXAMPLE
A quick example is presented in test_axonread.ipynb file, ploting 12 sec data from a long time recording abf file.
```
import axonread_LuBo as AR
start_t=4.0 #starting position of the reading region; 
end_t=16.0 #ending position of the reading region;
fn='H:\\axon data\\2016Jun09\\Aug04001.abf'
data, si =AR.abfload(fn,start_t, end_t)

import numpy as np
import matplotlib.pyplot as plt
Itrace=data[:,0]
Vtrace=data[:,1] 
ttrace=np.arange(1,len(Itrace)+1,1.0)/si

plt.subplot(211)
plt.plot(ttrace[:],Itrace[:])
plt.xlabel('Time (sec)')
plt.ylabel('Current (nA)')

plt.subplot(212)
plt.plot(ttrace[:],Vtrace[:])
plt.xlabel('Time (sec)')
plt.ylabel('Voltage (V)')
plt.show()
```
![figure_1](https://cloud.githubusercontent.com/assets/19654472/19011742/9dc59a16-876d-11e6-9773-fa8b5f17366e.png)

