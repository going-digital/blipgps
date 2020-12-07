#%%
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from gps_sat_info import sats_info
import pyfftw
np.fft = pyfftw.interfaces.numpy_fft
pyfftw.interfaces.cache.enable()
from gps_chip import ca_table
#%%
fn = "2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.dat"
fc = 1575.42e6
fs = 4e6
chip_samples = int(fs//1000)
offset = 1000000
num_chips = 2
count = num_chips * chip_samples
data = np.fromfile(fn, dtype=np.int16, count=int(offset+count)*2)
data = np.clip(np.floor_divide(data, 150), -2, 1) + 0.5
data = np.reshape(data, (data.shape[0]//2, 2))
data = data[offset:, 0] + 1j * data[offset:, 1]
#%%
ca_chip_table = ca_table(int(fs))
chip_window = min(10, num_chips//2)
fft_ca_chips = {
    i: np.conjugate(np.fft.fft(
        # Pad to 2 durations
        np.concatenate((
            np.tile(ca, chip_window),
            np.zeros(ca.shape[0] * (num_chips - chip_window))
        ))
    )) for (i, ca) in ca_chip_table.items()
}
#%%
# doppler in range -10000 - 10000 Hz
# FFT frequency bins are -fs/2 to +fs/2
# FFT length is chip_samples*num_chips
# So for fs=4MHz, bins are fs/(chip_samples*num_chips) apart

from mpl_toolkits.mplot3d import Axes3D
doppler_offset = 15000
xx = np.arange(chip_samples)/chip_samples
yy = np.arange(-doppler_offset, doppler_offset+1, 250)

threshold = 10 # 15

for prn in tqdm(fft_ca_chips.keys()):
    # Cp* is fft_ca_chips[1]
    S = np.fft.fft(data)
    results_phase = np.zeros(chip_samples)
    results_doppler = []
    for doppler in range(-doppler_offset, doppler_offset+1, 250):
        offset = int(doppler / fs * chip_samples * num_chips)
        S_ = np.roll(S, offset)
        X = fft_ca_chips[prn] * S_
        x = np.fft.ifft(X)
        x = np.sum(x.reshape(num_chips, chip_samples), axis=0)
        x_abs = abs(x)**2
        results_doppler.append(x_abs.max())
        results_phase = np.maximum(x_abs, results_phase)
    results_doppler = np.array(results_doppler)
    snr_doppler = results_doppler.max() / results_doppler.mean()
    snr_phase = results_phase.max() / results_phase.mean()
    if (snr_doppler * snr_phase > threshold):
        # Plot matches over doppler and phase
        fig, axs = plt.subplots(1,2,figsize=(10,5))
        axs[0].plot(xx, results_phase)
        axs[1].plot(yy, results_doppler)
        plt.title("PRN {}".format(prn))
        plt.show()

# %%
