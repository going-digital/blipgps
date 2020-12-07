# Next task - PVT algorithm

This works out the position, velocity and time - ie. the fix. As we are only
working with a 2ms snippet of signal, that isn't enough information to know the
current ephemeris or take a full time reading.

Need to know approximately what the time and position before the data is enough
a fix. First step is to get an approximate fix by any means necessary - a
pseudo-range.

## Pseudo-ranging

The timebase of the system will be inaccurate, so we don't know:
    * Exact frequency offset - so can only rely on relative doppler
    * Exact time and position
      * Time probably only known to within 10 seconds
      * Position not known
      * Need to narrow those down by any means necessary.
        * Satellite visibility (probably narrows down to about 1000km circle?)
        * Satellite doppler measurement (Hopefully narrow down to 300km or less?)
        * L1C/A data transitions (happens every 20ms)

Assuming we know each satellites chip timing offset (sub-1ms), but not how many milliseconds:
1ms at speed of light is 300km. So c x 1ms = 300km. Within a 300km diameter
circle, we can set a multiple of ms for each satellite transmission, then check
if that is consistent. 300km x 300km is 9,000km2 for a square. Earth surface
area is about 510,000,000km2. So ballpark 57,000 circles to check for the whole
globe. Maybe 100k circles including tiling overlaps. Should be possible to
compute several regions in parallel until they can be ruled out through
contradiction. (Should be possible to tesselate the earth by tiling triangular
faces of an icosahedron - 20 x triangle number) or maybe a cube (6 x n^2)


## Satellite positions

Need way to query satellite positions at a given time.

## Ephemeris changes

Might be useful to attempt to predict satellite tracks

  * [ ] Look at consistency of existing tracks
  * [ ] How accurately can historic data be predicted?
  * [ ] Can live ephemerides be forecast in the same way?
