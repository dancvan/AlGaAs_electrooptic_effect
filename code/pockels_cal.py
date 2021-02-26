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

def function_transfer(freq,tf_in):
    db = abs(tf_in)
    deg = np.angle(tf_in, deg=True)
    return freq, db, deg

def tf_import(tf_path):
    db = np.loadtxt(tf_path + 'db.TXT')
    deg = np.loadtxt(tf_path + 'deg.TXT')
    ff = db[:,0]
    return ff, db[:,1], deg[:,1]

def tf_interpolate(new_freq, tf_tuple):
    new_db = np.interp(new_freq, tf_tuple[0], tf_tuple[1])
    new_deg = np.interp(new_freq, tf_tuple[0], tf_tuple[2])
    return new_freq, new_db, new_deg

def bode_plt(tf_tuple, save_path, lbl, title, ylbl='dB'):
    ff = tf_tuple[0]
    db = tf_tuple[1]
    deg = tf_tuple[2]
    bode_fig = plt.figure()
    plt.subplot(211)
    if not ylbl=='dB':
        plt.loglog(ff, db, label=lbl)
    else:
        plt.semilogx(ff,db, label = lbl)
    plt.xlim(ff[0], ff[-1])
    plt.ylabel(ylbl)
    plt.legend()
    plt.title(title.replace('_', '\_'))
    plt.subplot(212)
    plt.semilogx(ff,deg, label = lbl)
    plt.xlim(ff[0], ff[-1])
    plt.legend()
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('phase [deg]')
    plt.savefig(save_path + '/' + title + '.png', dpi=300,bbox_inches='tight')
    plt.close()
    return bode_fig


def pock_cal(meas_data_dir, date, final_dir, meas_type='noise', spectra_type='pk', plot_saving=False, model=False):
    #Make final directory
    labl = date + '_' + meas_type + '_' + spectra_type
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

    #Common_directories
    HVA_common_dir = '/Users/daniel_vander-hyde/Documents/git/SU/algaas_electrooptic_effect/measurements/HVASVR_tf/'
    OLG_common_dir = '/Users/daniel_vander-hyde/Documents/git/SU/algaas_electrooptic_effect/measurements/OLG/algaas/'
    HVA_dir = HVA_common_dir + 'HVACH3_plus_pomona/' + '02_17_2021/'
    OLG_dir = OLG_common_dir + date + '/'


    HVA = tf_import(HVA_dir)
    OLG = tf_import(OLG_dir)
    #If the data is a swept frequency measurement
    if meas_type == 'swept':
        HVA_CH1_dir = HVA_common_dir + 'HVACH1/' + date + '/'
        #Import the measured tf from SR785
        meas_swep = tf_import(meas_data_dir)
        if plot_saving == True:
            bode_plt(meas_swep, new_final_dir, date.replace("_", "\_"), 'Pockels_effect_frequency_response_uncalibrated_dB')
        swept_tf = transfer_function(meas_swep[1], meas_swep[2])
        #interpolate related tfs
        HVA_CH1 = tf_import(HVA_CH1_dir)
        HVA_CH1_tf = transfer_function(HVA_CH1[1], HVA_CH1[2])
        HVA_inter = tf_interpolate(meas_swep[0], HVA)
        OLG_inter = tf_interpolate(meas_swep[0], OLG)

    else:
        spectra = concat_vecs(meas_data_dir)
        #interpolate related tfs
        HVA_inter = tf_interpolate(spectra[0], HVA)
        OLG_inter = tf_interpolate(spectra[0], OLG)
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
            plt.savefig(new_final_dir + '/v_spectra_' + labl + '.png',dpi=300, bbox_inches='tight')
            plt.close()

        #HVA plotting
        bode_plt(HVA, new_final_dir, 'HVA.75_total_gain', 'HVACH3+pomona')

        #OLG plotting
        bode_plt(OLG, new_final_dir , date.replace("_", "\_"), 'OLG' )


    #transfer function
    HVA_tf = transfer_function(HVA_inter[1], HVA_inter[2])
    OLG_tf = transfer_function(OLG_inter[1], OLG_inter[2])

    if meas_type == 'swept':
        stf_noHVA = swept_tf/HVA_CH1_tf
        volt_divider = True
        if volt_divider == True:
            # Voltage divider with r_1 as the first resistor and r_2 as the resistor connected to ground
            r_1 = 100000
            r_2 = 50
            pom_vdivider = (r_2)/(r_1+r_2)
            stf_noHVA = stf_noHVA*pom_vdivider
        #Volts in error signal / Volts directly to electrodes
        new_swept_tf = function_transfer(meas_swep[0],stf_noHVA)
        if plot_saving == True:
            bode_plt(new_swept_tf, new_final_dir, date.replace('_','\_'), 'Pockels_effect_frequency_response_uncalibrated_vratio', ylbl='$V_\mathrm{err}$ / $V_\mathrm{electrodes}$')

        #Voltage spectra (with an input of 300Vpk) don't forget phase info
        spec_300Vpk = new_swept_tf[1]*300
        spectra = [new_swept_tf[0],spec_300Vpk, new_swept_tf[2]]

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
        plt.loglog(spectra[0],freq_noise, label= date.replace('_', '\_'),linewidth=3)
        plt.xlim([spectra[0][0], spectra[0][-1]])
        plt.legend()
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('$$\mathrm{Hz}_\mathrm{pk}$$')
        plt.title("Laser frequency noise from measured voltage noise")
        plt.savefig(new_final_dir + '/Hz' + '_spectra_' + labl + '.png', dpi=300, bbox_inches='tight')
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
    if  meas_type == 'swept':
        spectra_disp = [spectra[0], displac_spect, spectra[2]]
        final_fig = bode_plt(spectra, new_final_dir, date.replace('_','\_'), 'Pockels_effect_frequency_response_verrspectra', ylbl='Vpk')
    else:
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
        plt.savefig(new_final_dir + '/' + 'pockels_displacement_spectra' + labl + '.png',dpi=300,bbox_inches='tight')

    #Store raw / calibrated data along with metadata in data directory
    with h5py.File(new_final_dir + "/data.hdf5", "a") as f:

        #Raw data
        raw = f.create_group("raw")
        hva_save = f.create_group("raw/hva")                                             # where hva data will be saved
        hva_save_ch3 = f.create_group("raw/hva/ch3+pomona")
        if meas_type == 'swept':
            hva_save_ch1 = f.create_group("raw/hva/ch1")
            hva_save_ch1.attrs['dir'] = HVA_CH1_dir
            pomona_vdiv=f.create_dataset("pomona_vdivider",data=pom_vdivider)
            trans_func = f.create_group("raw/meas_freq_resp")
            meas_db = f.create_dataset("raw/meas_freq_resp/db", data=meas_swep[1])
            meas_deg = f.create_dataset("raw/meas_freq_resp/deg", data=meas_swep[2])
            trans_func.attrs['dir'] = meas_data_dir
        else:
            vdata_save = f.create_dataset("raw/v_spect", data=spectra[1])
            vdata_save.attrs['units'] = spectra_type
            vdata_save.attrs['dir'] = meas_data_dir               # where error signal spectra will be saved
        freq = f.create_dataset("freq", data=spectra[0])                                 # common frequency vector
        cav_length = f.create_dataset("cav_length", data=Lcav)
        laser_freq = f.create_dataset("laser_freq", data=nu)
        laserPZTresp = f.create_dataset("laserV2Hz", data=laserV2Hz )
        hva_save_ch3.attrs['dir'] = HVA_dir
        olg_save = f.create_group("raw/olg")                                                # where olg data will be saved
        olg_save.attrs['dir'] = OLG_dir
        if meas_type == 'swept':
            hvadb_save_ch1 = f.create_dataset("raw/hva/ch1/db", data=HVA_CH1[1])
            hvadeg_save_ch1 = f.create_dataset("raw/hva/ch1/deg", data=HVA_CH1[2])
        hvadb_save_ch3 = f.create_dataset("raw/hva/ch3+pomona/db", data=HVA_inter[1])
        hvadeg_save_ch3 = f.create_dataset("raw/hva/ch3+pomona/deg", data=HVA_inter[2])
        olgdb_save = f.create_dataset("raw/olg/db", data=OLG_inter[1])
        olgdeg_save = f.create_dataset("raw/olg/deg", data=OLG_inter[2])


        #Calibrated data
        calibra = f.create_group("calibrated")
        hvatf_save = f.create_group("calibrated/hva")
        hvach3tf_save = f.create_dataset("calibrated/hva/ch3+pomona",data=HVA_tf)
        olgtf_save = f.create_dataset("calibrated/olg",data=OLG_tf)
        freqnoise_save = f.create_dataset("calibrated/HzpV",data=freq_noise)
        if meas_type == 'swept':
            hvach1tf_save = f.create_dataset("calibrated/hva/ch1",data=HVA_CH1_tf)
            displacement_spect = f.create_dataset("calibrated/disp_spect", data=displac_spect)
            phase_resp = f.create_dataset("calibrated/phase_resp", data=spectra[2])
        else:
            displacement_spect = f.create_dataset("calibrated/disp_spect",data=displac_spect)
        displacement_spect.attrs['units'] = spectra_type
        displacement_spect.attrs['meas_type'] = meas_type
        f.close()

    return final_fig
