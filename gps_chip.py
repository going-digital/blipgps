# Generate the chip sequences for each GPS satellite
# %%
import numpy as np
from scipy.signal import max_len_seq, resample
from tqdm import tqdm

# Generate delay table
ca_g2_delay = {}
prn_1 = [
    # Source: IS-GPS-200L
    # Note that 950 appears for both PRN34 and PRN37, so those sequences
    # can not be discerned.
    5, 6, 7, 8, 17, 18, 139, 140, 141, 251, 252, 254, 255, 256, 257, 258, 469,
    470, 471, 472, 473, 474, 509, 512, 513, 514, 515, 516, 859, 860, 861, 862,
    863, 950, 947, 948, 950,
]
for i, v in enumerate(prn_1):
    ca_g2_delay[1+i] = v
prn_120_sbas = [
    # This covers codes for augmentation systems and other navigation systems
    # using the same modulations.
    # Includes satellites that are yet to launch as of 22 Nov 2020
    # Source:
    # https://www.gps.gov/technical/prn-codes/L1-CA-PRN-code-assignments-2019-Oct.pdf
    145, 175, 52, 21, 237, 235, 886, 657, 634, 762,
    355, 1012, 176, 603, 130, 359, 595, 68, 386, 797,
    456, 499, 883, 307, 127, 211, 121, 118, 163, 628,
    853, 484, 289, 811, 202, 1021, 463, 568, 904, 670,
    230, 911, 684, 309, 644, 932, 12, 314, 891, 212,
    185, 675, 503, 150, 395, 345, 846, 798, 992, 357,
    995, 877, 112, 144, 476, 193, 109, 445, 291, 87,
    399, 292, 901, 339, 208, 711, 189, 263, 537, 663,
    942, 173, 900, 30, 500, 935, 556, 373, 85, 652,
    310
]
for i, v in enumerate(prn_120_sbas):
    ca_g2_delay[120+i] = v

# %%
operational_satellites = set()

# GPS constellation - 1 to 32, 14 currently not used
operational_satellites.update(range(1, 33))
operational_satellites.remove(14)

# EGNOS constellation
# European Geostationary Navigatoin Overlay Service
operational_satellites.update([120, 121, 123, 126, 136])

# GATBP satellite
operational_satellites.update([122])

# SDCM constellation
operational_satellites.update([125, 140, 141])

# GAGAN constellation
operational_satellites.update([127, 128])

# MSAS constellation
# Multi-functional Satellite Augmentation System
# MTSAT-1R (Himawari 6) and MTSAT-2 (Himawari 7)
operational_satellites.update([129, 137])

# WAAS constellation
# Wide Area Augmentation System
operational_satellites.update([131, 135, 138])

# BDSBAS constellation
operational_satellites.update([130, 143, 144])

# NSAS satellite
operational_satellites.update([147])

# QZSS (Michibiki / みちびき) constellation
# Provides enhanced positioning over Asia-Oceania esp. Japan
operational_satellites.update([193, 194, 195, 199])

# %%


def gps_ca_chip(prn):
    """From IS-GPS-200L 3.3.2.3, Table 3-Ia

    """
    g1 = max_len_seq(10, taps=[7])[0]
    g2 = max_len_seq(10, taps=[8, 7, 4, 2, 1])[0]
    return np.bitwise_xor(
        g1,
        np.roll(g2, ca_g2_delay[prn])
    )


def gps_ca_modulated(prn, fs=4000000):
    # Generate oversampled bitstream
    phase = np.repeat(2 * (gps_ca_chip(prn) - 0.5), 16)
    # Downsample to required rate
    return resample(phase, fs//1000)


def ca_code_test():
    """Test C/A code generator using vectors from IS-GPS-200L
    >>> ca_code_test()
    """
    # From IS-GPS-200L Table 3-Ia
    vectors = [
        (1, 0o1440), (2, 0o1620), (3, 0o1710), (4, 0o1744), (5, 0o1133),
        (6, 0o1455), (7, 0o1131), (8, 0o1454), (9, 0o1626), (10, 0o1504),
        (11, 0o1642), (12, 0o1750), (13, 0o1764), (14, 0o1772), (15, 0o1775),
        (16, 0o1776), (17, 0o1156), (18, 0o1467), (19, 0o1633), (20, 0o1715),
        (21, 0o1746), (22, 0o1763), (23, 0o1063), (24, 0o1706), (25, 0o1743),
        (26, 0o1761), (27, 0o1770), (28, 0o1774), (29, 0o1127), (30, 0o1453),
        (31, 0o1625), (32, 0o1712), (33, 0o1745), (34, 0o1713), (35, 0o1134),
        (36, 0o1456), (37, 0o1713), (120, 0o671), (121, 0o536), (122, 0o1510),
        (123, 0o1545), (124, 0o160), (125, 0o701), (126, 0o13), (127, 0o1060),
        (128, 0o245), (129, 0o527), (130, 0o1436), (131, 0o1226),
        (132, 0o1257), (133, 0o46), (134, 0o1071), (135, 0o561), (136, 0o1037),
        (137, 0o770), (138, 0o1327), (139, 0o1472), (140, 0o124), (141, 0o366),
        (142, 0o133), (143, 0o465), (144, 0o717), (145, 0o217), (146, 0o1742),
        (147, 0o1422), (148, 0o1442), (149, 0o523), (150, 0o736),
        (151, 0o1635), (152, 0o136), (153, 0o273), (154, 0o1026), (155, 0o3),
        (156, 0o1670), (157, 0o624), (158, 0o235), (159, 0o554), (160, 0o75),
        (161, 0o1341), (162, 0o42), (163, 0o115), (164, 0o207), (165, 0o204),
        (166, 0o1576), (167, 0o1142), (168, 0o40), (169, 0o107), (170, 0o1643),
        (171, 0o553), (172, 0o317), (173, 0o415), (174, 0o123), (175, 0o1267),
        (176, 0o1535), (177, 0o635), (178, 0o760), (179, 0o707), (180, 0o1276),
        (181, 0o1322), (182, 0o211), (183, 0o1562), (184, 0o774), (185, 0o323),
        (186, 0o112), (187, 0o1306), (188, 0o27), (189, 0o1470), (190, 0o1505),
        (191, 0o1013), (192, 0o355), (193, 0o727), (194, 0o170), (195, 0o30),
        (196, 0o472), (197, 0o1237), (198, 0o414), (199, 0o1050),
        (200, 0o1630), (201, 0o571), (202, 0o732), (203, 0o1301),
        (204, 0o1173), (205, 0o20), (206, 0o447), (207, 0o1114), (208, 0o341),
        (209, 0o1024), (210, 0o1046)
    ]
    p = np.power(2, np.arange(9, -1, -1))
    for prn, v in tqdm(vectors):
        gps_ca_code = gps_ca_chip(prn)
        r = np.sum(gps_ca_code[:10] * p)
        assert(v == r)


def ca_table(fs):
    table = {}
    for prn in tqdm(ca_g2_delay.keys()):
        if prn in operational_satellites:
            table[prn] = gps_ca_modulated(prn, fs)
    return table
# %%
# ca_table(4000000)
# %%
# import matplotlib.pyplot as plt
# fs = 4000000
# plt.plot(gps_ca_modulated(1, fs)[:100])
# plt.show()
# %%


if __name__ == "__main__":
    import doctest
    doctest.testmod()


# %%

# %%
