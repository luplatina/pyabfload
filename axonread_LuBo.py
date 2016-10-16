import neo as neo
import numpy as np
import matplotlib.pyplot as plt
def abfload(fn,start_t,end_t):
    
    header = neo.io.AxonIO(filename=fn).read_header()#even though abf file could be large, all key informations are in heard file;
    si=1/(header['fADCSampleInterval']*header['nADCNumChannels']*1.e-6)#sampling rate
    nbchannel = header['nADCNumChannels']#number of channle;
    BLOCKSIZE=512
    if header['nDataFormat'] == 0:
        dt = np.dtype('i2')
    elif header['nDataFormat'] == 1:
        dt = np.dtype('f4')
        
    
    ####################headOffset1 give the flexible starting time#####################################
    t_startbit=int(start_t*si*nbchannel)
    totalsize1=int((end_t-start_t)*si*nbchannel)
    headOffset1 = header['lDataSectionPtr'] * BLOCKSIZE +(header['nNumPointsIgnored']+t_startbit) * dt.itemsize
    ####################totalsize1 give the flexible ending time######################################
    
    data1 = np.memmap(fn, dt, 'r', shape=(totalsize1), offset=headOffset1)
    #The key step! np.memap Create a memory-map to an array stored in a binary file on disk.
    #Memory-mapped files are used for accessing small segments of large files on disk, 
    #without reading the entire file into memory.
    data1 = data1.reshape((int(data1.size/nbchannel),nbchannel)).astype('f')
    
    
    def reformat_integer_V1(data, nbchannel, header):
        #transfer the binary data into the readable data format for the users;
        #all the transfer factors have been stored in header file.
        chans = [chan_num for chan_num in
                 header['nADCSamplingSeq'] if chan_num >= 0]
        for n, i in enumerate(chans[:nbchannel]):  # respect SamplingSeq
            data[:, n] /= header['fInstrumentScaleFactor'][i]
            data[:, n] /= header['fSignalGain'][i]
            data[:, n] /= header['fADCProgrammableGain'][i]
            if header['nTelegraphEnable'][i]:
                data[:, n] /= header['fTelegraphAdditGain'][i]
            data[:, n] *= header['fADCRange']
            data[:, n] /= header['lADCResolution']
            data[:, n] += header['fInstrumentOffset'][i]
            data[:, n] -= header['fSignalOffset'][i]
    
    
    reformat_integer_V1(data1, nbchannel, header) 
    return data1, si
