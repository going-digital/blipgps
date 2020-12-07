# %%
# # Extract short segment from sample recording

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from gps_sat_info import sats_info

# The fftw library provides faster FFTs, but is not included in numpy
# due to license incompatibilities.
#
# The following lines upgrade the section of the numpy library.
import pyfftw
np.fft = pyfftw.interfaces.numpy_fft
pyfftw.interfaces.cache.enable()

#%%
# Generate a source sample
# This data is 4MHz sampled IQ pairs at 16 bits centered on 1575.42MHz
fn = "2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.dat"
fc = 1575.42e6
fs = 4e6
chip_samples = fs//1000
offset = 1000000
# Only reading 4 chips worth (4ms) of data
num_chips = 4
count = num_chips * chip_samples
data = np.fromfile(fn, dtype=np.int16, count=int(offset+count)*2)
#%%
# Quantise to 2 bits per channel
# This is to simulate the 2 bit quantisation of common GPS frontend ICs
# TODO: These numbers are hand picked - should be some form of AGC
data = np.clip(np.floor_divide(data, 150), -2, 1) + 0.5
#%%
# The recording is with quadrature oscillators,
# resulting in complex samples. I and Q in radio parlance, or
# real and imaginary in complex numbers.
#
# Convert to complex form
data = np.reshape(data, (data.shape[0]//2, 2))
data = data[offset:, 0] + 1j * data[offset:, 1]
# %%
# Plot some source data
plt.plot(data.real[:50])
plt.plot(data.imag[:50])
plt.title('Incoming data, I and Q')
plt.show()
#%%
data_f = np.fft.fft(data)
freq = np.fft.fftfreq(data.size, 1/fs) + fc
plt.plot(freq, abs(data_f)**2)
plt.xticks(rotation=90)
plt.title('Signal power spectrum')
plt.show()
# This graph shows a huge blip at 1160
#%%
plt.semilogy(freq, abs(data_f)**2)
plt.xticks(rotation=90)
plt.ylim(1e4,4e5)
plt.title('Signal power spectrum rescaled')
plt.show()
# %%
# Course acquisition
#
# Calculate chip signals from every possible satellite

from gps_chip import ca_table
ca_chip_table = ca_table(int(fs))
# %%
# C/A Centre frequency is 1575.42MHz
# Doppler offset is near zero
# Code frequency 1.023MHz = 1023000 samples per second
# 1 chip in exactly 1ms
# 4000 samples in 1ms

# Calculate FFT of CA chips
# Don't know the alignment of the chip, so sample for 2 chip durations, and
# correlate a 1 chip chunk

# Calculate fourier transform each chip
# Every 20 chips the phase might invert, and that inversion might be within
# the sampling period. Attempt to match over a window of half the sampling
# period.
chip_window = min(10, num_chips//2)
# Calculate FFT of all the chip windows
fft_ca_chips = {
    i: np.conjugate(np.fft.fft(
        # Pad to 2 durations
        np.concatenate((
            np.tile(ca, chip_window),
            np.zeros(ca.shape[0] * (num_chips - chip_window))
        ))
    )) for (i, ca) in ca_chip_table.items()
}
# %%
# Useful references:
# How GNSS-SDR does it:
# https://gnss-sdr.org/docs/sp-blocks/acquisition/#implementation-gps_l1_ca_pcps_acquisition
# Soltanian et al:
# https://link.springer.com/article/10.1186/1687-6180-2014-143
# Cui et al:
# https://file.scirp.org/pdf/IJCNS_2017081113460335.pdf
#
# https://theses.eurasip.org/media/theses/documents/perna-ivana-cyclic-spectral-analysis-of-gps-signal.pdf
# Key techniques:
#   Working in the fourier domain gives speedups:
#     Cross correlation => element-wise multiplication with conjugate
#     Time offset => phase offset
#     Doppler shift => array value shift with padding
# %%
# Calculate frequency shifted received data
phase_array = -2j * np.pi * np.arange(num_chips * chip_samples) / fs
fft_rx_shifted = {
    doppler: np.fft.fft(np.exp(doppler * phase_array) * data)
    for doppler in range(-10000, 10001, 250)
}
# TODO: Extend this match across the whole sample period.
# Don't know the phase of the chips.
# TODO: Transform that removes 180 degree phase? ie. squaring?
# Better solution, frequency shifting in frequency domain
#fft_rx = np.fft.fft(data)
#fft_rx_shifted = {
#    doppler: fft_rx.roll(doppler*len(data)/fs)
# or
#    doppler: fft_rx.pad(data[])
#}
# %%
# Cross correlate all chips with all doppler shifts.
# Cross correlation in the time domain is equivalent to
# per-element multiplication with the conjugate in the frequency domain.
# Bonus: cross correlation is O(n^2), but per-element multiplication is O(n)

results = {}
for prn, ca_fft in tqdm(fft_ca_chips.items()):
    max_align = 0
    for doppler, rx_fft in fft_rx_shifted.items():
        correlation_freq = ca_fft * rx_fft
        correlation_power = np.sum(correlation_freq**2)
        correlation = np.abs(np.fft.ifft(correlation_freq))
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
print('\n')

# Sort PRNs by correlation score
prn_sorted_list = sorted(
    results.keys(),
    key=lambda n: results[n]['score'],
    reverse=True
)

for prn in prn_sorted_list:
    r = results[prn]
    print(
        "Score {:4.1f}: {} Phase {:3.4f}us Doppler {}Hz".format(
            r['score'], sats_info[prn], r['chip phase']*1e6, r['doppler']
        )
    )
# %%
# Would expect to see:
# PRN1: Doppler 7070Hz
# PRN11: Doppler 5474Hz
# PRN17: Doppler 7073Hz
# PRN20: Doppler 8312Hz
# PRN32: Doppler 6430Hz
