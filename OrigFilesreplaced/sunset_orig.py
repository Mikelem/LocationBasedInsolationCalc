import math

def sunset(RLAT, SIND, COSD, RSmEzM):
    """
    Calculate the time of DUSK in temporal radians at mean local time based on latitude,
    sine and cosine of the declination angle, and the angular radius of the sun as seen from Earth.
    
    Parameters:
    - RLAT: Latitude in degrees
    - SIND, COSD: Sine and cosine of the declination angle
    - RSmEzM: (Sun Radius - Earth Radius) / distance to Sun
    
    Returns:
    - DUSK: Time of dusk in temporal radians. Returns large positive or negative values
            for constant daylight or nighttime, respectively.
    """
    TWOPI = 2 * math.pi
    SINJ = math.sin(TWOPI * RLAT / 360)
    COSJ = math.cos(TWOPI * RLAT / 360)
    SJSD = SINJ * SIND
    CJCD = COSJ * COSD
    
    if SJSD + RSmEzM + CJCD <= 0:
        DUSK = -999999  # Constant nighttime
    elif SJSD + RSmEzM - CJCD >= 0:
        DUSK = 999999  # Constant daylight
    else:
        # Compute DUSK (at local time)
        CDUSK = -(SJSD + RSmEzM) / CJCD  # cosine of DUSK
        DUSK = math.acos(CDUSK)
    
    return DUSK
