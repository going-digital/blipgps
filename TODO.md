- [x] Find sources of GPS IQ recordings
- [x] Resolve position with GNSS-SDR
- [x] Generate L1 C/A chips
- [x] Generate L1 C/A signals
- [x] Locate L1 C/A signals in Python
- [ ] Python interface to NASA Daily GPS Broadcast Ephemeris files
- [ ] Measure phase and code chip for each satellite
- [ ] Extend to Galileo E1 and Beidou B1C, which are on same frequency.
- [ ] Consider switching to L5

L1 Project plan:
- [x] L1 C/A: Identify satellites by chip
- [x] L1 C/A: Calibrate out inaccuracies in sample clock
- [x] L1 C/A: Measure satellite doppler
- [x] L1 C/A: Measure satellite chip phase
- [ ] L1 P:Match up P codes to get time of week
- [ ] Refine fix using Galileo
- [ ] Refine fix using BeiDou
- [ ] Refine fix using QZSS
- [ ] Refine fix using EGNOS, WAAS and other SBAS

L2 Project plan:
- [ ] L2C, P Attempt to get position
- [ ] Refine fix using QZSS

L5 Project plan:
- [ ] L5 Attempt to get position
- [ ] Refine fix using Galileo E5a
- [ ] Refine fix using BeiDou B2a
- [ ] Refine fix using QZSS, IRNSS
- [ ] Refine fix using SBAS

