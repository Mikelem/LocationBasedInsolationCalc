import numpy as np
from config import TWOPI

def coszij(r_lat, sin_d, cos_d):
    """
    coszij calculates the daily average cosine of the zenith angle, both weighted by time and sunlight.
    r_lat: latitude in radians
    sin_d, cos_d: sine and cosine of the declination angle
    """

    # Calculate sine and cosine of latitude
    sin_j = np.sin(TWOPI * r_lat / 360)
    cos_j = np.cos(TWOPI * r_lat / 360)

    # Calculate products of sine and cosine of latitude and declination
    sjsd = sin_j * sin_d
    cjcd = cos_j * cos_d

    if sjsd + cjcd <= 0:
        # Constant nighttime at this latitude
        coszt = 0
        coszs = 0
    elif sjsd - cjcd >= 0:
        # Constant daylight at this latitude
        ecosz = sjsd * TWOPI
        qcosz = sjsd * ecosz + 0.5 * cjcd**2 * TWOPI
        coszt = sjsd  # = ecosz / TWOPI
        coszs = qcosz / ecosz
    else:
        # Nighttime at initial and final times with daylight in between
        cdusk = -sjsd / cjcd
        dusk = np.arccos(cdusk)
        sdusk = np.sqrt(cjcd**2 - sjsd**2) / cjcd
        s2dusk = 2 * sdusk * cdusk
        dawn = -dusk
        sdawn = -sdusk
        s2dawn = -s2dusk

        ecosz = sjsd * (dusk - dawn) + cjcd * (sdusk - sdawn)
        qcosz = sjsd * ecosz + cjcd * (sjsd * (sdusk - sdawn) + 0.5 * cjcd * (dusk - dawn + 0.5 * (s2dusk - s2dawn)))
        coszt = ecosz / TWOPI
        coszs = qcosz / ecosz

    return coszt, coszs

if __name__ == '__main__':
    # sin_d, cos_d are returned from ORBIT.py
    r_lat = 40.0150
    sin_d= -0.2936935287630569
    cos_d= 0.9558996344610158
    coszt, coszs = coszij(r_lat, sin_d, cos_d)
    print("coszt =", coszt)
    print("coszs =", coszs)

    coszt= 0.14641057726860077
    coszs= 0.42914126440073946