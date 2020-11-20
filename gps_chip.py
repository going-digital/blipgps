# Generate the chip sequences for each GPS satellite
#%%
import numpy as np
from scipy.signal import max_len_seq


def gps_ca_chip(prn):
    """From IS-GPS-200L 3.3.2.3, Table 3-Ia
    Generate first 10 chips of SV 1
    >>> gps_ca_chip(1)[:10]
    array([1, 1, 0, 0, 1, 0, 0, 0, 0, 0], dtype=int8)

    Generate First 10 Chips Octal C/A column of Table 3-Ia
    >>> p = np.power(2, np.arange(9,-1,-1))
    >>> r=[oct(np.sum(gps_ca_chip(prn)[:10] * p)) for prn in range(1, 38)]
    >>> r[:7]
    ['0o1440', '0o1620', '0o1710', '0o1744', '0o1133', '0o1455', '0o1131']
    >>> r[7:14]
    ['0o1454', '0o1626', '0o1504', '0o1642', '0o1750', '0o1764', '0o1772']
    >>> r[14:21]
    ['0o1775', '0o1776', '0o1156', '0o1467', '0o1633', '0o1715', '0o1746']
    >>> r[21:28]
    ['0o1763', '0o1063', '0o1706', '0o1743', '0o1761', '0o1770', '0o1774']
    >>> r[28:35]
    ['0o1127', '0o1453', '0o1625', '0o1712', '0o1745', '0o1713', '0o1134']
    >>> r[35:37]
    ['0o1456', '0o1713']
    """
    lookup = {
        1: (2, 6), 2: (3, 7), 3: (4, 8), 4: (5, 9), 5: (1, 9), 6: (2, 10),
        7: (1, 8), 8: (2, 9), 9: (3, 10), 10: (2, 3), 11: (3, 4), 12: (5, 6),
        13: (6, 7), 14: (7, 8), 15: (8, 9), 16: (9, 10), 17: (1, 4),
        18: (2, 5), 19: (3, 6), 20: (4, 7), 21: (5, 8), 22: (6, 9), 23: (1, 3),
        24: (4, 6), 25: (5, 7), 26: (6, 8), 27: (7, 9), 28: (8, 10),
        29: (1, 6), 30: (2, 7), 31: (3, 8), 32: (4, 9), 33: (5, 10),
        34: (4, 10), 35: (1, 7), 36: (2, 8), 37: (4, 10),
    }
    # max_len_seq operates in a reverse orientation to IS-GPS-200L,
    # so tap numbers are 10-n
    g1 = max_len_seq(10, taps=[7])[0]
    g2 = max_len_seq(10, taps=[8, 7, 4, 2, 1])[0]
    g2a = np.bitwise_xor(
        np.roll(g2, lookup[prn][0]-10),
        np.roll(g2, lookup[prn][1]-10)
    )
    return np.bitwise_xor(g1, g2a)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

#%%