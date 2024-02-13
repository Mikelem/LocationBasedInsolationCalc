import math
from config import TWOPI

# Getting  sunrise_time + sunset_time is the last item before printing
# Ensure all the variables (DUSK, eq_time, r_lon, itzone, coszt, sundis) are defined before this block of code.

# dusk_angle_rad is returned by sunset.py
# eq_time is returned by ORBIT.py
# r_lon, itzone come from obvious places
# coszt is returned by coszij.py
# sundis is returned by ORBIT.py


def get_sunrise_sunset_times(dusk_angle_rad, eq_time, r_lon, itzone, coszt, sundis):
    # Calculate solar radiation incidence
    SRINC = 1367 * coszt / sundis ** 2
    # Calculate dawn and dusk times in decimal hours
    DAWN_decimal = (-dusk_angle_rad - eq_time) * 24 / TWOPI + 12 - r_lon / 15 + itzone
    DUSK_decimal = (dusk_angle_rad - eq_time) * 24 / TWOPI + 12 - r_lon / 15 + itzone
    print("DAWN_decimal", DAWN_decimal)
    print("DUSK_decimal", DUSK_decimal)
    
    if DUSK_decimal >= 999999:
        sunset_time = ""
        sunrise_time = "Always Day Light"
        return sunrise_time, sunset_time, SRINC
    elif DUSK_decimal <= -999999:
        sunrise_time = ""
        sunset_time = "Always Nightime"
        return sunrise_time, sunset_time, SRINC
    
    # Convert decimal hours to hours and minutes
    def format_time(decimal_time):
        hours, remainder = divmod(abs(decimal_time), 1)
        minutes = round(remainder * 60)
        # Ensure minutes are two digits
        return f"{int(hours):02d}:{minutes:02d}"

    sunrise_time = format_time(DAWN_decimal)
    sunset_time = format_time(DUSK_decimal)

    return sunrise_time, sunset_time, SRINC

def sunset(r_lat, sin_d, cos_d, rsm_ezm):
    """
    Calculate the time of DUSK in temporal radians at mean local time based on latitude,
    sine and cosine of the declination angle, and the angular radius of the sun as seen from Earth.
    
    Parameters:
    - r_lat: Latitude in degrees
    - sin_d, cos_d: Sine and cosine of the declination angle
    - rsm_ezm: (Sun Radius - Earth Radius) / distance to Sun
    
    Returns:
    - dusk_angle_rad: Time of dusk in temporal radians. Returns large positive or negative values
            for constant daylight or nighttime, respectively.
    """

    sin_j = math.sin(TWOPI * r_lat / 360)
    cos_j = math.cos(TWOPI * r_lat / 360)
    sjsd = sin_j * sin_d
    CJCD = cos_j * cos_d
    
    if sjsd + rsm_ezm + CJCD <= 0:
        dusk_angle_rad = -999999  # Constant nighttime
    elif sjsd + rsm_ezm - CJCD >= 0:
        dusk_angle_rad = 999999  # Constant daylight
    else:
        # Compute DUSK (at local time)
        CDUSK = -(sjsd + rsm_ezm) / CJCD  # cosine of DUSK
        dusk_angle_rad = math.acos(CDUSK)
    
    return dusk_angle_rad

# # Function to calculate the dusk angle in radians
# def sunset(r_lat, sin_d, cos_d, rsm_ezm):
#     # Calculate the cosine of the dusk angle
#     cos_dusk_angle = (math.sin(rsm_ezm) - sin_d * math.sin(r_lat)) / (cos_d * math.cos(r_lat))
#     # Ensure the value is within the valid range for acos
#     cos_dusk_angle = max(min(cos_dusk_angle, 1), -1)
#     # Calculate the dusk angle in radians
#     dusk_angle_rad = math.acos(cos_dusk_angle)
#     return dusk_angle_rad

if __name__ == '__main__':
    r_lat = 40.0150 # Boulder, CO
    r_lon = -105.270 # Boulder, CO
    itzone = round(r_lon/15)
    rsm_ezm = 0.014904593128673706
    sin_d= -0.2936935287630569 # From ORBIT.py
    cos_d= 0.9558996344610158  # From ORBIT.py
    eq_time= -0.05904885296383622 # From ORBIT.py
    sundis= 0.985347907494622 # From ORBIT.py
    coszt= 0.14641057726860077 # From coszij
    COSZS= 0.42914126440073946

    dusk_angle_rad = sunset(r_lat, sin_d, cos_d, rsm_ezm)
    
    print("DUSK_ANGLE_RAD=",dusk_angle_rad)

    sunrise_time, sunset_time, SRINC = get_sunrise_sunset_times(dusk_angle_rad, eq_time, r_lon, itzone, coszt, sundis)
    print(f"Dawn: {sunrise_time}, Dusk: {sunset_time}, Solar Radiation: {SRINC}")