# orbit.py
import math
from config import TWOPI, OMEGAe, OMEGAp, ECCENp, OBLIQp

def orbit(eccen, obliq, omegvp, days_from_y2k):
    """
    Calculate the orbit parameters.

    Parameters:
    eccen (float): Eccentricity of the Earth's orbit
    obliq (float): Obliquity of the Earth's axis
    omegvp (float): Longitude of perihelion
    days_from_y2k (float): Number of days from Y2K

    Returns:
    tuple: A tuple containing the sine and cosine of the declination, the distance to the sun,
           the longitude and latitude of the sun, and the equation of time.
    """
    # Calculate the mean longitude of the sun
    mean_lon = TWOPI * (days_from_y2k / 365.25 + 1)
    mean_lon = mean_lon % TWOPI

    # Calculate the mean anomaly
    mean_anom = mean_lon - OMEGAe - eccen * math.sin(mean_lon - omegvp)
    mean_anom = mean_anom % TWOPI

    # Calculate the true anomaly
    true_anom = mean_anom + 2 * eccen * math.sin(mean_anom)

    # Calculate the distance to the sun
    sundis = (1 - eccen * eccen) / (1 + eccen * math.cos(true_anom))

    # Calculate the longitude of the sun
    sun_lon = true_anom + OMEGAe
    sun_lon = sun_lon % TWOPI

    # Calculate the sine and cosine of the declination
    sin_d = math.sin(obliq) * math.sin(sun_lon)
    cos_d = math.sqrt(1 - sin_d * sin_d)

    # Calculate the latitude of the sun
    sun_lat = math.asin(sin_d)

    # Calculate the equation of time
    eq_time = (mean_lon - sun_lon) * 24 / TWOPI

    return sin_d, cos_d, sundis, sun_lon, sun_lat, eq_time