import glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import os
import h5py

plt_style_dir = '/Users/daniel_vander-hyde/Documents/git/my_python/matplotlib/stylelib/'
if os.path.isdir(plt_style_dir) == True:
    plt.style.use(plt_style_dir + 'pptsize')

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

def phase_wrap(phase_array, type='deg'):
    if type == 'deg':
        fin_phase_array = (phase_array + 180) % (2 * 180) - 180
    if type == 'rad':
        fin_phase_array = (phase_array + np.pi) % (2 * np.pi) - np.pi
    return fin_phase_array

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


def pock_cal(meas_data_dir, date, final_dir, meas_type='noise', spectra_type='pk', sample='algaas', plot_saving=False, model=False):
    """
    This function undergoes the AlGaAs electro-optic experiment calibration to convert the error signal voltage spectra from the PDH loop into a displacement spectra. The function takes multiple directories as inputs which contain
    the necessary spectra and transfer functions. The output compresses all of the raw datasets, some intermediate datasets and calibrated voltage
    """

    plt_style_dir = '/Users/daniel_vander-hyde/Documents/git/my_python/matplotlib/stylelib/'
    if os.path.isdir(plt_style_dir) == True:
        plt.style.use(plt_style_dir + 'pptsize')

    #Make final directory
    labl = date + '_' + meas_type + '_' + spectra_type + '_' + sample
    new_final_dir = final_dir + '/' + labl
  #  figure_dir = new_final_dir + '/figs'
  #  calib_data_dir = new_final_dir + '/data'
    if os.path.isdir(new_final_dir) == False:
        os.mkdir(new_final_dir)
  #  if os.path.isdir(figure_dir) == False:
  #      os.mkdir(figure_dir)
  #  if os.path.isdir(calib_data) == False:
  #      os.mkdir(calib_data_dir)

    #Common_directories
    HVA_common_dir = '../../measurements/HVASVR_tf/'
    OLG_common_dir = '../../measurements/OLG/'
    HVA_dir = HVA_common_dir + 'HVACH3_plus_pomona/' + date + '/'
    #OLG_dir = OLG_common_dir + date + '/'
    OLG_dir = OLG_common_dir + sample + '/' + date + '/'

    HVA = tf_import(HVA_dir)
    OLG = tf_import(OLG_dir)
    #If the data is a swept frequency measurement
    if meas_type == 'swept':
        #HVA_CH1_dir = HVA_common_dir + 'HVACH1/' + date + '/'
        HVA_CH1_dir = HVA_common_dir + 'HVACH1_w_LPF/' + date + '/'
        electrode_type = 'disk'
        if sample == 'sio2ta2o5':
            Electcap_dir = '../../measurements/electrode_capacitence/' + electrode_type + '/' + sample + '/03_12_2021/'
        else:
            Electcap_dir = '../../measurements/electrode_capacitence/' + electrode_type + '/' + sample + '/03_10_2021/'
        #Import the measured tf from SR785
        meas_swep = tf_import(meas_data_dir)
        if plot_saving == True:
            bode_plt(meas_swep, new_final_dir, date.replace("_", "\_"), 'Pockels_effect_frequency_response_uncalibrated_dB')
        swept_tf = transfer_function(meas_swep[1], meas_swep[2])

        #HVA CH1 import and interpolation
        HVA_CH1 = tf_import(HVA_CH1_dir)
        HVA_CH1_inter = tf_interpolate(meas_swep[0], HVA_CH1)
        HVA_CH1_tf = transfer_function(HVA_CH1_inter[1], HVA_CH1_inter[2])

        #Electrode capacitence transfer function import and interpolation
        ECAP = tf_import(Electcap_dir)
        ECAP_inter = tf_interpolate(meas_swep[0], ECAP)
        ECAP_tf = transfer_function(ECAP_inter[1], ECAP_inter[2])

        inp_voltage = 5                                                          #Vpk

        #interpolate related tfs
        HVA_inter = tf_interpolate(meas_swep[0], HVA)
        OLG_inter = tf_interpolate(meas_swep[0], OLG)

    else:
        spectra = concat_vecs(meas_data_dir)
        #interpolate related tfs
        HVA_inter = tf_interpolate(spectra[0], HVA)
        OLG_inter = tf_interpolate(spectra[0], OLG)
        if plot_saving == True:
            #Spectra plotting
            plt.loglog(spectra[0], spectra[1], label=labl.replace("_","\_"))
            plt.legend()
            plt.xlabel('frequency [Hz]')
            plt.xlim([spectra[0][0],spectra[0][-1]])
            if spectra_type == 'pk':
                plt.ylabel('$$V_\mathrm{pk}$$')
            elif spectra_type == 'rms':
                plt.ylabel('$$V_\mathrm{rms}$$')
            plt.savefig(new_final_dir + '/v_spectra_' + labl + '.png',dpi=300, bbox_inches='tight')
            plt.close()

    if plot_saving == True:
        #HVA plotting
        bode_plt(HVA, new_final_dir, 'HVA.75\_total\_gain', 'HVACH3+pomona')
        #OLG plotting
        bode_plt(OLG, new_final_dir , date.replace('_', '\_'), 'OLG' )


    #transfer function
    HVA_tf = transfer_function(HVA_inter[1], HVA_inter[2])
    OLG_tf = transfer_function(OLG_inter[1], OLG_inter[2])

    if meas_type == 'swept':
        volt_divider = True
        if volt_divider == True:
            # Voltage divider with r_1 as the first resistor and r_2 as the resistor connected to ground
            r_1 = 100000
            r_2 = 50
            pom_vdivider = (r_2)/(r_1+r_2)

            swept_tf = swept_tf*pom_vdivider

        stf_unnorm = swept_tf*inp_voltage

        s_unnorm = [meas_swep[0], abs(stf_unnorm), np.angle(stf_unnorm, deg=True)]

        if plot_saving == True:
            bode_plt(s_unnorm, new_final_dir, date.replace('_','\_'), 'Pockels_effect_frequency_response_vspectra', ylbl='$V_\mathrm{pk}$')

        v_direct = inp_voltage*HVA_CH1_tf*ECAP_tf                                  # This is the voltage directly across the coating for all measured frequencies (with phase information)
        vdirec = [meas_swep[0], abs(v_direct), np.angle(v_direct,deg=True)]
        if plot_saving==True:
            bode_plt(vdirec, new_final_dir, date.replace('_','\_'), 'Potential difference across electrodes', ylbl='$V_\mathrm{pk}$')

    #Laser frequency spectra calibration
    laserV2Hz = 2.0e6
    HzpV = HVA_tf*laserV2Hz

    #loop calibration
    CLG = 1/(1-OLG_tf)
    CAL = OLG_tf*CLG
    CALVpHz=CAL/HzpV
    CALHzpV=HzpV/CAL

    #phase correction to swept measurement (HVA and loop correction factor)
    if meas_type == 'swept':
        freq_noise = CALHzpV*stf_unnorm
    else:
        freq_noise = abs(CALHzpV)*spectra[1]


    #plot loop calibration

    #Laser frequency noise
    if plot_saving == True and meas_type != 'swept':
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
    if meas_type == 'swept':
        disp_spect_norm = displac_spect/v_direct                              #Displacement spectra normalized by the frequency dependent injection (leaves us with mpk/Vpk)

    #Model estimation
    model_freq = 10000
    marty_estimate = 3.8e-16 #mpk/[V*m]
    Efield_strength_estimate = 6350 #[V*m]

    #Displacement spectra
    if  meas_type == 'swept':
        displac_spect_unnorm = [meas_swep[0], abs(displac_spect), np.angle(displac_spect, deg=True)]
        displac_spect_norm = [meas_swep[0], abs(disp_spect_norm), np.angle(disp_spect_norm, deg=True)]
        final_fig = bode_plt(displac_spect_unnorm, new_final_dir, date.replace('_','\_'), 'Displacement spectra for AlGaAs Pockels effect measurement', ylbl='Displacement [$\mathrm{m}_\mathrm{pk}$]')
    else:
        final_fig = plt.loglog(spectra[0],displac_spect,color='m',label=labl, linewidth=3)

    if model == True and meas_type != 'swept':
        plt.axhline(y=marty_estimate*Efield_strength_estimate,linestyle='--',color='k', label='Marty estimate')
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
            freq = f.create_dataset("freq", data=meas_swep[0])                                 # common frequency vector
            hva_save_ch1 = f.create_group("raw/hva/ch1")
            hva_save_ch1.attrs['dir'] = HVA_CH1_dir
            pomona_vdiv=f.create_dataset("pomona_vdivider",data=pom_vdivider)
            trans_func = f.create_group("raw/meas_freq_resp")
            meas_db = f.create_dataset("raw/meas_freq_resp/db", data=meas_swep[1])
            meas_deg = f.create_dataset("raw/meas_freq_resp/deg", data=meas_swep[2])
            trans_func.attrs['dir'] = meas_data_dir
            direc_volt = f.create_group("raw/vdirect")                                  # the Vpk voltage and phase information of the signal directly sent to the electrodes
        else:
            freq = f.create_dataset("freq", data=spectra[0])                                 # common frequency vector
            vdata_save = f.create_dataset("raw/v_spect", data=spectra[1])
            vdata_save.attrs['units'] = spectra_type
            vdata_save.attrs['dir'] = meas_data_dir               # where error signal spectra will be saved
        cav_length = f.create_dataset("cav_length", data=Lcav)
        laser_freq = f.create_dataset("laser_freq", data=nu)
        laserPZTresp = f.create_dataset("laserV2Hz", data=laserV2Hz )
        hva_save_ch3.attrs['dir'] = HVA_dir
        olg_save = f.create_group("raw/olg")                                             # where olg data will be saved
        cal_save = f.create_group("raw/cal")                                             # easily accessible loop calibration factor data
        olg_save.attrs['dir'] = OLG_dir
        if meas_type == 'swept':
            hvadb_save_ch1 = f.create_dataset("raw/hva/ch1/db", data=HVA_CH1[1])
            hvadeg_save_ch1 = f.create_dataset("raw/hva/ch1/deg", data=HVA_CH1[2])
            vdirec_db = f.create_dataset("raw/vdirect/db", data=vdirec[1])
            vdirec_deg = f.create_dataset("raw/vdirect/deg", data=vdirec[2])
        hvadb_save_ch3 = f.create_dataset("raw/hva/ch3+pomona/db", data=HVA_inter[1])
        hvadeg_save_ch3 = f.create_dataset("raw/hva/ch3+pomona/deg", data=HVA_inter[2])
        olgdb_save = f.create_dataset("raw/olg/db", data=OLG_inter[1])
        olgdeg_save = f.create_dataset("raw/olg/deg", data=OLG_inter[2])
        calgain_save = f.create_dataset("raw/cal/gain", data=abs(CAL))
        caldeg_save = f.create_dataset("raw/cal/deg", data=np.angle(CAL, deg=True))


        #Calibrated data
        calibra = f.create_group("calibrated")
        hvatf_save = f.create_group("calibrated/hva")
        hvach3tf_save = f.create_dataset("calibrated/hva/ch3+pomona",data=HVA_tf)
        olgtf_save = f.create_dataset("calibrated/olg",data=OLG_tf)
        freqnoise_save = f.create_dataset("calibrated/HzpV",data=CALHzpV)
        if meas_type == 'swept':
            hvach1tf_save = f.create_dataset("calibrated/hva/ch1",data=HVA_CH1_tf)
            displacement_spect = f.create_dataset("calibrated/disp_spect_unnorm", data=displac_spect_unnorm[1])
            phase_resp1 = f.create_dataset("calibrated/phase_resp_unnorm", data=displac_spect_unnorm[2])
            displacement_spect_norm = f.create_dataset("calibrated/disp_spect_norm", data=displac_spect_norm[1])
            displacement_spect_norm.attrs['units'] = 'm' + spectra_type + '/Vpk'
            phase_resp2 = f.create_dataset("calibrated/phase_resp_norm", data=displac_spect_norm[2])

        else:
            displacement_spect = f.create_dataset("calibrated/disp_spect",data=displac_spect)
        displacement_spect.attrs['units'] = spectra_type
        displacement_spect.attrs['meas_type'] = meas_type
        f.close()

    return final_fig
