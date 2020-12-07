# PRN: SV, name, CA offset, CA test vector, P offset, P test vector
"""
Abbreviations:
ASAL Algerian Space Agency
AUS-NZ Geoscience Australia/New Zealand System
BDSBAS BeiDou Satellite-Based Augmentation System
EGNOS European Geostationary Navigation Overlay Service
GAGAN GPS Aided Geo-Augmented Navigation
GBAS Ground Based Augmentation System
KASS Korean Augmented Satellite System
MSAS MTSAT Space-Based Augmentation System
NSAS Nigerian Satellite Augmentation System
QZSS Quasi-Zenith Satellite System
SDCM System of Differential Correction and Monitoring
WAAS Wide Area Augmentation System
"""
import datetime as dt

sats_info = {
    # List of all PRN allocations on the L1C/A band
    # GPS satellites are changed regularly - check with US gov. for current list.
    1: ('GPS', 'PRN 1', '-'),
    2: ('GPS', 'PRN 2', '-'),
    3: ('GPS', 'PRN 3', '-'),
    4: ('GPS', 'PRN 4', '-'),
    5: ('GPS', 'PRN 5', '-'),
    6: ('GPS', 'PRN 6', '-'),
    7: ('GPS', 'PRN 7', '-'),
    8: ('GPS', 'PRN 8', '-'),
    9: ('GPS', 'PRN 9', '-'),
    10: ('GPS', 'PRN 10', '-'),
    11: ('GPS', 'PRN 11', '-'),
    12: ('GPS', 'PRN 12', '-'),
    13: ('GPS', 'PRN 13', '-'),
    14: ('GPS', 'PRN 14', '-'),
    15: ('GPS', 'PRN 15', '-'),
    16: ('GPS', 'PRN 16', '-'),
    17: ('GPS', 'PRN 17', '-'),
    18: ('GPS', 'PRN 18', '-'),
    19: ('GPS', 'PRN 19', '-'),
    20: ('GPS', 'PRN 20', '-'),
    21: ('GPS', 'PRN 21', '-'),
    22: ('GPS', 'PRN 22', '-'),
    23: ('GPS', 'PRN 23', '-'),
    24: ('GPS', 'PRN 24', '-'),
    25: ('GPS', 'PRN 25', '-'),
    26: ('GPS', 'PRN 26', '-'),
    27: ('GPS', 'PRN 27', '-'),
    28: ('GPS', 'PRN 28', '-'),
    29: ('GPS', 'PRN 29', '-'),
    30: ('GPS', 'PRN 30', '-'),
    31: ('GPS', 'PRN 31', '-'),
    32: ('GPS', 'PRN 32', '-'),
    33: ('GPS', 'PRN 33', '-'),
    34: ('GPS', 'PRN 34', '-'),
    35: ('GPS', 'PRN 35', '-'),
    36: ('GPS', 'PRN 36', '-'),
    37: ('GPS', 'PRN 37', '-'),
    120: ('EGNOS', 'INMARSAT 3F2 AOR-E', '15.5 W'),
    121: ('EGNOS', 'Eutelsat 5WB', '5 W'),
    122: ('AUS-NZ', 'INMARSAT 4F1', '143.5 E'),
    123: ('EGNOS', 'ASTRA 5B', '31.5 E'),
    124: ('EGNOS', 'Reserved PRN124', '-'),
    125: ('SDCM', 'Luch-5A', '16 W'),
    126: ('EGNOS', 'INMARSAT 4F2', '63.9 E'),
    127: ('GAGAN', 'GSAT-8', '55 E'),
    128: ('GAGAN', 'GSAT-10', '83 E'),
    129: ('MSAS', 'MTSAT-2', '145 E'),
    130: ('BDSBAS', 'G6', '80 E'),
    131: ('WAAS', 'Eutelsat 117 West B', '117 W'),
    132: ('GAGAN', 'GSAT-15', '93.5 E'),
    133: ('WAAS', 'SES-15', '129 W'),
    134: ('KASS', 'MEASAT-3D', '91.5 E'),
    135: ('WAAS', 'Intelsat Galaxy 30', '125 W'),
    136: ('EGNOS', 'SES-5', '5 E'),
    137: ('MSAS', 'MTSAT-2', '145 E'),
    138: ('WAAS', 'ANIK F1R', '107.3 W'),
    140: ('SDCM', 'Luch-5B', '95 E'),
    141: ('SDCM', 'Luch-4', '167 E'),
    143: ('BDSBAS', 'G3', '110.5 E'),
    144: ('BDSBAS', 'G1', '140 E'),
    147: ('NSAS', 'NIGCOMSAT-1R', '42.5 E'),
    148: ('ASAL', 'ALCOMSAT-1', '24.8 W'),
    # https://qzss.go.jp/en/technical/satellites/index.html#QZSS
    #183: ('QZSS', 'QZS-1 L1S', ''),
    #184: ('QZSS', 'QZS-2 L1S', ''),
    #185: ('QZSS', 'QZS-4 L1S', ''),
    #186: ('QZSS', 'Reserved', ''),
    #187: ('QZSS', 'Reserved', ''),
    #188: ('QZSS', 'Reserved', ''),
    #189: ('QZSS', 'QZS-3 L1S', ''),
    #190: ('QZSS', 'Reserved', ''),
    #191: ('QZSS', 'Reserved', ''),
    #192: ('QZSS', 'Reserved', ''),
    193: ('QZSS', 'QZS-1', ''),
    194: ('QZSS', 'QZS-2', ''),
    195: ('QZSS', 'QZS-4', ''),
    #196: ('QZSS', 'QZS-2 L5S', ''),
    #197: ('QZSS', 'Reserved', ''),
    #198: ('QZSS', 'Reserved', ''),
    199: ('QZSS', 'QZS-3', ''),
    #200: ('QZSS', 'QZS-4 L5S', ''),
    #201: ('QZSS', 'Reserved', ''),
    #202: ('QZSS', 'Reserved', ''),
}

prn_lookup = {
    "OPS 5111": {
        'SVN': 1, 'PRN slots': [
            (4, dt.date(1978, 2, 22), dt.date(1985, 7, 17)),
        ]
    },
    "OPS 5112": {
        'SVN': 2, 'PRN slots': [
            (7, dt.date(1978, 5, 13), dt.date(1981, 7, 16)),
        ]
    },
    "OPS 5113": {
        'SVN': 3, 'PRN slots': [
            (6, dt.date(1978, 10, 7), dt.date(1992, 5, 18)),
        ]
    },
    "OPS 5114": {
        'SVN': 4, 'PRN slots': [
            (8, dt.date(1978, 12, 11), dt.date(1989, 10, 14)),
        ]
    },
    "OPS 5117": {
        'SVN': 5, 'PRN slots': [
            (5, dt.date(1980, 12, 9), dt.date(1983, 11, 28)),
        ]
    },
    "OPS 5118": {
        'SVN': 6, 'PRN slots': [
            (9, dt.date(1980, 4, 26), dt.date(1991, 3, 6)),
        ]
    },
    "OPS 9794": {
        'SVN': 6, 'PRN slots': [
            (9, dt.date(1983, 7, 14), dt.date(1993, 5, 4)),
        ]
    },
    "USA-1": {
        'SVN': 9, 'PRN slots': [
            (13, dt.date(1984, 6, 13), dt.date(1994, 6, 20)),
        ]
    },
    "USA-5": {
        'SVN': 10, 'PRN slots': [
            (12, dt.date(1984, 9, 8), dt.date(1995, 11, 18)),
        ]
    },
    "USA-10": {
        'SVN': 11, 'PRN slots': [
            (11, dt.date(1985, 10, 9), dt.date(1994, 4, 13)),
        ]
    },
    "USA-35": {
        'SVN': 14, 'PRN slots': [
            (14, dt.date(1989, 2, 14), dt.date(2000, 3, 26)),
        ]
    },
    "USA-38": {
        'SVN': 13, 'PRN slots': [
            (2, dt.date(1989, 6, 10), dt.date(2004, 2, 22)),
        ]
    },
    "USA-42": {
        'SVN': 16, 'PRN slots': [
            (16, dt.date(1989, 8, 18), dt.date(2000, 10, 13)),
        ]
    },
    "USA-47": {
        'SVN': 19, 'PRN slots': [
            (19, dt.date(1989, 10, 21), dt.date(2001, 3, 16)),
        ]
    },
    "USA-49": {
        'SVN': 17, 'PRN slots': [
            (17, dt.date(1989, 12, 11), dt.date(2005, 2, 23)),
        ]
    },
    "USA-50": {
        'SVN': 18, 'PRN slots': [
            (18, dt.date(1990, 1, 24), dt.date(2000, 8, 18)),
        ]
    },
    "USA-54": {
        'SVN': 20, 'PRN slots': [
            (20, dt.date(1990, 3, 26), dt.date(1996, 5, 21)),
        ]
    },
    "USA-63": {
        'SVN': 21, 'PRN slots': [
            (21, dt.date(1990, 8, 2), dt.date(2002, 9, 25)),
        ]
    },
    "USA-64": {
        'SVN': 15, 'PRN slots': [
            (15, dt.date(1990, 10, 1), dt.date(2006, 11, 17)),
        ]
    },
    "USA-66": {
        'SVN': 23, 'PRN slots': [
            (23, dt.date(1990, 11, 26), dt.date(2004, 2, 13)),
            (32, dt.date(2008, 2, 25), dt.date(2016, 1, 25)),
        ]
    },
    "USA-71": {
        'SVN': 24, 'PRN slots': [
            (24, dt.date(1991, 7, 4), dt.date(2011, 9, 30)),
        ]
    },
    "USA-79": {
        'SVN': 25, 'PRN slots': [
            (25, dt.date(1992, 2, 23), dt.date(2009, 12, 18)),
        ]
    },
    "USA-80": {
        'SVN': 28, 'PRN slots': [
            (28, dt.date(1992, 4, 10), dt.date(1997, 8, 15)),
        ]
    },
    "USA-83": {
        'SVN': 26, 'PRN slots': [
            (26, dt.date(1992, 7, 7), dt.date(2015, 1, 6)),
        ]
    },
    "USA-84": {
        'SVN': 27, 'PRN slots': [
            (27, dt.date(1992, 9, 9), dt.date(2011, 8, 10)),
        ]
    },
    "USA-85": {
        'SVN': 32, 'PRN slots': [
            (31, dt.date(1992, 11, 22), dt.date(1993, 1, 1)),
            (1, dt.date(1993, 1, 1), dt.date(2008, 3, 17)),
        ]
    },
    "USA-87": {
        'SVN': 29, 'PRN slots': [
            (29, dt.date(1992, 12, 18), dt.date(2007, 10, 23)),
        ]
    },
    "USA-88": {
        'SVN': 22, 'PRN slots': [
            (22, dt.date(1993, 2, 3), dt.date(2002, 12, 3)),
        ]
    },
    "USA-90": {
        'SVN': 31, 'PRN slots': [
            (31, dt.date(1993, 2, 3), dt.date(2002, 12, 3)),
        ]
    },
    # TODO: Complete this list
}