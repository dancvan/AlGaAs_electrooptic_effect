import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import os
import h5py

plt.style.use('/Users/daniel_vander-hyde/Documents/git/my_python/matplotlib/stylelib/pptsize')

def concat_vecs(directory):
    txtcounter = len(glob.glob1(directory,"*.TXT"))
    freq = np.zeros((801,txtcounter))
    freq1 = np.zeros((801,txtcounter))
    vpk = np.zeros((801,txtcounter))

    columns = range(0,txtcounter)
    fff = 0
    vpkn = 0
    ##  import and measurements
    for i in columns: 
        data = np.loadtxt(directory + str(i).zfill(2) + '.TXT')
        freq[:,i] = data[:,0]
        vpk[:,i] = data[:,1]
        if i == columns[0]:
            fff = freq[:,i]
            vpkn = vpk[:,i]
        elif i == columns[-1]:
            fff = np.append(fff,freq[:,i])
            vpkn=np.append(vpkn,vpk[:,i])
        else: 
            fff = np.append(fff, freq[:,i][:-1])
            vpkn = np.append(vpkn, vpk[:,i][:-1])
    return fff, vpkn

def transfer_function(amplitude, phase): 
    return 10**(amplitude/20)* np.exp(1j*(phase/180)*np.pi)

def tf_import(tf_path): 
    db = np.loadtxt(tf_path + 'db.TXT')
    deg = np.loadtxt(tf_path + 'deg.TXT')
    ff = db[:,0]
    return ff, db[:,1], deg[:,1]

def tf_interpolate(new_freq, tf_tuple): 
    new_db = np.interp(new_freq, tf_tuple[0], tf_tuple[1])
    new_deg = np.interp(new_freq, tf_tuple[0], tf_tuple[2])
    return new_freq, new_db, new_deg

def bode_plt(data_path, save_path, lbl, title):
    tot = tf_import(data_path)
    ff = tot[0]
    db = tot[1]
    deg = tot[2]
    
    plt.subplot(211)
    plt.semilogx(ff,db, label = lbl)
    plt.xlim(ff[0], ff[-1])
    plt.ylabel('dB')
    plt.legend()
    plt.title(title)
    plt.subplot(212)
    plt.semilogx(ff,deg, label = lbl)
    plt.xlim(ff[0], ff[-1])
    plt.legend()
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('phase [deg]')
    plt.savefig(save_path + '/' + title + '.png', dpi=300,bbox_inches='tight')
    plt.close()
    

def pock_cal(vdata_dir, spectra_type, HVA_dir, OLG_dir, final_dir, labl, plot_saving=False, model=False):
    
    #Make final directory
    new_final_dir = final_dir + '/' + labl
  #  figure_dir = new_final_dir + '/figs'
  #  calib_data_dir = new_final_dir + '/data'
    if os.path.isdir(new_final_dir) == False:
        os.mkdir(new_final_dir)
  #  if os.path.isdir(figure_dir) == False: 
  #      os.mkdir(figure_dir)
  #  if os.path.isdir(calib_data) == False:
  #      os.mkdir(calib_data_dir)
    
    plt.style.use('/Users/daniel_vander-hyde/Documents/git/my_python/matplotlib/stylelib/pptsize')
    spectra = concat_vecs(vdata_dir)
    if plot_saving == True: 
        
        #Spectra plotting
        plt.loglog(spectra[0], spectra[1], label=labl)
        plt.legend()
        plt.xlabel('frequency [Hz]')
        plt.xlim([spectra[0][0],spectra[0][-1]])
        if spectra_type == 'pk': 
            plt.ylabel('$$V_\mathrm{pk}$$')
        elif spectra_type == 'rms':
            plt.ylabel('$$V_\mathrm{rms}$$')
        plt.savefig(new_final_dir + '/v' + spectra_type + '_spectra_' + labl + '.png',dpi=300, bbox_inches='tight')
        plt.close()
        
        #HVA plotting
        bode_plt(HVA_dir, new_final_dir, '.75 total gain', 'HVA')
        
        #OLG plotting
        bode_plt(OLG_dir, new_final_dir , labl, 'OLG' )
        
    #Interpolate to common frequency vector
    HVA = tf_import(HVA_dir)
    OLG = tf_import(OLG_dir)
    HVA_inter = tf_interpolate(spectra[0], HVA)
    OLG_inter = tf_interpolate(spectra[0], OLG)
    
    
    #transfer function
    HVA_tf = transfer_function(HVA_inter[1], HVA_inter[2])
    OLG_tf = transfer_function(OLG_inter[1], OLG_inter[2])
    
    #Laser frequency spectra calibration
    laserV2Hz = 2.0e6
    HzpV = HVA_tf*laserV2Hz
    
    #loop calibration
    CLG = 1/(1-OLG_tf)
    CAL = OLG_tf*CLG
    CALVpHz=CAL/HzpV
    CALHzpV=HzpV/CAL
    
    #Laser frequency spectra
    freq_noise = abs(CALHzpV)*spectra[1]
    
    
    #plot loop calibration
    
    #Laser frequency noise
    if plot_saving == True:
        plt.loglog(spectra[0],freq_noise, label='Frequency comb (FEB1721)',linewidth=3)
        plt.xlim([spectra[0][0], spectra[0][-1]])
        plt.legend()
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('$$\mathrm{Hz}_\mathrm{pk}$$')
        plt.title("Laser frequency noise from measured voltage noise")
        plt.savefig(new_final_dir + '/Hz' + spectra_type + '_spectra_' + labl + '.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    #Cavity parameters
    c = 299792458
    lamb =1.064e-6
    nu = c/lamb
    Lcav = 0.165
    
    #Displacement spect
    displac_spect = freq_noise*Lcav/nu
    
    #Model estimation
    model_freq = 10000
    marty_estimate = 3.8e-16 #mpk/[V*m]
    Efield_strength_estimate = 6350 #[V*m]
    
    #Displacement spectra
    final_fig = plt.loglog(spectra[0],displac_spect,color='m',label=labl, linewidth=3)
    if model == True:
        plt.loglog(model_freq,marty_estimate*Efield_strength_estimate ,'*',color='m', label='Estimated AlGaAs dn/dE effect with $V_\mathrm{electrode}= 300\; V_\mathrm{pk}$ @ 10000 Hz (inside coating)',markersize=20)
    plt.xlim([spectra[0][0], spectra[0][-1]])
    plt.legend()
    plt.xlabel('Frequency [Hz]')
    if spectra_type == 'pk':
        plt.ylabel('Displacement [$\mathrm{m}_\mathrm{pk}$]')
    if spectra_type == 'rms':
        plt.ylabel('Displacement [$\mathrm{m}_\mathrm{rms}$]')
    plt.title("Displacement spectra for AlGaAs Pockels effect measurement")
    plt.savefig(new_final_dir + '/' + labl + '_' + 'displacement_normal_electrodes.png',dpi=300,bbox_inches='tight')
    
    #Store raw / calibrated data along with metadata in data directory
    with h5py.File(new_final_dir + "/data.hdf5", "a") as f:
        
        ##Initialize hdf5 datasets
        
        #Raw data
        raw = f.create_group("raw")
        freq = f.create_dataset("freq", data=spectra[0])                                 ## common frequency vector
        hva_save = f.create_group("raw/hva")                          # where hva data will be saved
        cav_length = f.create_dataset("cav_length", data=Lcav)
        laser_freq = f.create_dataset("laser_freq", data=nu)
        laserPZTresp = f.create_dataset("laserV2Hz", data=laserV2Hz )
        hva_save.attrs['dir'] = HVA_dir
        olg_save = f.create_group("raw/olg")                          # where olg data will be saved
        olg_save.attrs['dir'] = OLG_dir
        vdata_save = f.create_dataset("raw/v_spect", data=spectra[1])                  # where error signal spectra will be saved
        vdata_save.attrs['units'] = spectra_type
        vdata_save.attrs['dir'] = vdata_dir
        hvadb_save = f.create_dataset("raw/hva/db", data=HVA_inter[1])
        hvadeg_save = f.create_dataset("raw/hva/deg", data=HVA_inter[2])
        olgdb_save = f.create_dataset("raw/olg/db", data=OLG_inter[1])
        olgdeg_save = f.create_dataset("raw/olg/deg", data=OLG_inter[2])
        
        
        #Calibrated data
        calibra = f.create_group("calibrated")
        hvatf_save = f.create_dataset("calibrated/hva",data=HVA_tf) 
        olgtf_save = f.create_dataset("calibrated/olg",data=OLG_tf) 
        freqnoise_save = f.create_dataset("calibrated/HzpV",data=freq_noise)
        displacement_spect = f.create_dataset("calibrated/disp_spect",data=displac_spect)
        displacement_spect.attrs['units'] = spectra_type
        f.close()
        
    return final_fig
