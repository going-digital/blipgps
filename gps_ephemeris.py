import requests
import time
import georinex as gr

# TODO: Check http://www.igs.org/products for a source of high precision
# ephemerides


def ephemeris_filename(ephemeris_date):
    # Return daily filename
    return ephemeris_date.strftime("brdc%j0.%yn.Z")


def get_ephemeris(ephemeris_date):
    print(ephemeris_date)
    fn = ephemeris_filename(ephemeris_date)
    try:
        print("Looking for file {}".format(fn))
        open(fn, 'rb').close()
    except FileNotFoundError:
        # Attempt download from NASA if not locally available
        # TODO: Add authentication required for this to work.
        raise NotImplementedError
        url = (
            "https://cddis.nasa.gov/archive/gnss/data/daily/" +
            ephemeris_date.strftime("%Y/%j/%yn/brdc%j0.%yn.Z")
        )
        response = requests.get(url)
        if response.status_code >= 300:
            response.raise_for_status()
        with open(fn, 'wb') as fh:
            fh.write(response.content)
        time.sleep(1)  # Simple rate limiting
    return gr.load(fn)
