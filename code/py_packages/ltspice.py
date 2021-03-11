#sdc = spice data convert
import numpy as np 
import matplotlib as plt
import pandas as pd
import re
import h5py
path = '/Users/daniel_vander-hyde/Documents/git/SU/algaas_electrooptic_effect/measurements/FSS_tfs/spice/'

class sdc:
    def spice2hdf5(path,filename):
        dater = pd.read_csv(path + filename + '.txt', encoding ='unicode_escape')
        ndata = dater.to_csv(header=False)
        ndata = ndata.replace('dB,','\t')
        ndata = ndata.replace('(','')
        ndata = ndata.replace('°)','')
        lines = ndata.splitlines()
        datas = np.zeros([len(lines),3])
        for i in range(len(datas)):
            datas[i,:] = re.split('; |, |\t',lines[i])
        hf = h5py.File(path + filename + '.h5', 'w')   
        hf.create_dataset('freq', data=datas[:,0])
        hf.create_dataset('dB', data=datas[:,1])
        hf.create_dataset('deg', data=datas[:,2])
        hf.close()