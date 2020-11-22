# %%
# # Extract short segment from sample recording

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from gps_sat_info import sats_info

# This data is 4MHz sampled IQ pairs at 16 bits centered on 1575.42MHz
fn = "2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.dat"
fs = 4000000
chip_samples = fs//1000
offset = 1000000
num_chips = 2
count = num_chips * chip_samples
data = np.fromfile(fn, dtype=np.int16, count=(offset+count)*2)
# Deinterlace into I and Q streams
data = np.reshape(data, (data.shape[0]//2, 2))
# Convert to native complex samples
data = data[offset:, 0] + 1j * data[offset:, 1]
#
# %%
plt.plot(data.real)
plt.show()
# %%
data_f = np.fft.fft(data)
#data_f[1160]=0
plt.plot(abs(data_f))
plt.show()
# This graph shows a huge blip at 1160
# %%
# Course acquisition
# Correlate signal with chips from each satellite
# Look for Gold code

from gps_chip import ca_table
ca_chip_table = ca_table(fs)
# %%
# C/A Centre frequency is 1575.42MHz
# Doppler offset is near zero
# Code frequency 1.023MHz = 1023000 samples per second
# 1 chip in exactly 1ms
# 4000 samples in 1ms

# Calculate FFT of CA chips
# Don't know the alignment of the chip, so sample for 2 chip durations, and
# correlate a 1 chip chunk
fft_ca_chips = {
    i: np.conjugate(np.fft.fft(
        # Pad to 2 durations
        np.tile(ca, num_chips)
    )) for (i, ca) in ca_chip_table.items()
}

# Calculate frequency shifted received data
phase_array = -1j * 2 * np.pi * np.arange(num_chips * chip_samples) / fs
fft_rx_shifted = {
    doppler: np.fft.fft(np.exp(doppler * phase_array) * data)
    for doppler in range(-10000, 10001, 250)
}
# %%
# Cross correlate all chips with all doppler shifts.

results = {}
for prn, ca_fft in tqdm(fft_ca_chips.items()):
    max_align = 0
    for doppler, rx_fft in fft_rx_shifted.items():
        correlation = np.abs(np.fft.ifft(ca_fft * rx_fft))
        best_corr = np.argmax(correlation)
        align = correlation[best_corr]
        if align > max_align:
            max_align = align
            max_phase = best_corr / fs  # Chip phase in seconds
            max_doppler = doppler  # Hz
    results[prn] = {
        'score': max_align,
        'chip phase': max_phase,
        'doppler': max_doppler
    }
    #print(prn, results[prn])

for prn, r in results.items():
    print(
        "Score {}: {} Phase {}s Doppler {}Hz".format(
            r['score'], sats_info[prn], r['chip phase'], r['doppler']
        )
    )
# %%
# Would expect to see:
# PRN1: Doppler 7070Hz
# PRN11: Doppler 5474Hz
# PRN17: Doppler 7073Hz
# PRN20: Doppler 8312Hz
# PRN32: Doppler 6430Hz
