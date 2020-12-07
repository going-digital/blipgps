#%%
# PVT solver

from gps_ephemeris import get_ephemeris
import datetime as dt
import numpy as np
# %%
observation_time = dt.date(2013, 4, 4)
eph = get_ephemeris(observation_time)
print(eph)
#%%
eph1 = eph.sel(sv='G01').sel(time=dt.datetime(2013,4,4,0,0,0))
# %%

# %%
# Start with a time window.
# For each 1ms chip time within the window, work out position and velocity of
# satellite in ECEF units using the ephemeride
# s.

# Useful reference:
# http://web.cecs.pdx.edu/~ssp/Reports/2006/Monaghan.pdf
# From table 2 above

# Better reference:
# https://gssc.esa.int/navipedia/index.php/GPS_and_Galileo_Satellite_Coordinates_Computation

# We have:
# SVclockBias, SVclockDrift, SVclockDriftRate
# IODE, Crs, DeltaN, M0, Cuc, Eccentricity, Cus, sqrtA, Toe, Cic, Omega0, Cis,
# Io, Crc, omega, OmegaDot, IDOT
# CodesL2, GPSWeek, L2Pflag, SVacc, health, TGD, IODC, TransTime, FitIntvl


def calc_position(eph, t):
    # Need t current time and toe (ephemerides reference)
    tk = t - eph['Toe']

    # Correct for end of GPS week
    if tk > 302400:
        tk -= 604800
    if tk < -302400:
        tk += 604800

    # Need M0, sqrt_mu, sqrt_a3, delta_n
    Mk = eph['M0'] + (sqrt_mu / sqrt_a3 + delta_n) * tk

# Solve Ek for Mk
Mk = Ek - e * np.sin(Ek) # TODO: Solve

# Calculate true anomaly
vk = np.arctan2(np.sqrt(1-e**2)*np.sin(Ek), np.cos(Ek)-e)
# TODO: Seems silly to to arctan then immediate cos and sin - could trig be
# avoided with complex vectors?

# Compute the argument of latitude uk from the argumennt of perigee w, true
# anomaly vk and corrections cuc and cus
uk = w + vk + cuc * cos(2*(w+vk))+ cus * sin(2*(w+vk))
# Compute the radial distance rk, considering corrections crc and crs
rk = a * (1 - e*cos(Ek)) + crc * np.cos(2*(w+vk)) + crs * np.sin(2*(w+vk))
# Compute the inclination ik of the orbital plane from the inclination i0 at
# the reference time t0e and corrections cic and cis
ik = i0 + i_dot * tk + cic * np.cos(2*(w+vk)) + cis * np.sin(2*(w+vk))
