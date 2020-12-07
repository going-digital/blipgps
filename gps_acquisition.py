# %%
import numpy as np
from tqdm import tqdm
from gps_sat_info import sats_info
import pyfftw
np.fft = pyfftw.interfaces.numpy_fft
pyfftw.interfaces.cache.enable()
from gps_chip import ca_table
# %%


def gps_acquisition(data, fs, fc):
    chip_samples = int(fs // 1000)
    num_chips = len(sample) // chip_samples
    count = num_chips * chip_samples

    ca_chip_table = ca_table(int(fs))
    chip_window = min(10, num_chips // 2)
    fft_ca_chips = {
        i: np.conjugate(np.fft.fft(
            # Pad to 2 durations
            np.concatenate((
                np.tile(ca, chip_window),
                np.zeros(ca.shape[0] * (num_chips - chip_window))
            ))
        )) for (i, ca) in ca_chip_table.items()
    }

    doppler_offset = 15000
    xx = np.arange(chip_samples)/chip_samples
    yy = np.arange(-doppler_offset, doppler_offset+1, 250)

    threshold = 10  # 15

    coarse_acq = {}
    for prn in tqdm(fft_ca_chips.keys()):
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
            coarse_acq[prn] = {
                'chip phase': np.argmax(results_phase),
                'doppler': np.argmax(results_doppler)
            }

    # Fine acquisition:
    # At this point doppler is a fraction of a sample bin.
    return coarse_acq

    # Fc is 1575420000Hz. Wavelength is 19cm. So 1m/s is approx. 5Hz doppler.
    # 10kHz doppler is 2km/s
