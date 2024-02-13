import math
from config import TWOPI

def sunset(r_lat, sin_d, cos_d, rsm_ezm):
    # Convert latitude from degrees to radians
    sin_j = math.sin(TWOPI * r_lat / 360)
    cos_j = math.cos(TWOPI * r_lat / 360)

    # Calculate the product of the sine of latitude and declination
    sjsd = sin_j * sin_d
     # Calculate the product of the cosine of latitude and declination
    cjcd = cos_j * cos_d

    # Check for constant nighttime
    if sjsd + rsm_ezm + cjcd <= 0:
        dusk_angle_rad = -999999  # Constant nighttime
    # Check for constant daylight
    elif sjsd + rsm_ezm - cjcd >= 0:
        dusk_angle_rad = 999999  # Constant daylight
    else:
         # Calculate the cosine of dusk
        cdusk = -(sjsd + rsm_ezm) / cjcd 
        # Calculate the dusk angle in radians
        dusk_angle_rad = math.acos(cdusk)

    return dusk_angle_rad

def get_sunrise_sunset_times(dusk_angle_rad, eq_time, r_lon, itzone, coszt, sundis):
    # Calculate solar radiation incidence
    srinc = 1367 * coszt / sundis ** 2

    # Calculate dawn and dusk times in decimal hours
    dawn_decimal = (-dusk_angle_rad - eq_time) * 24 / TWOPI + 12 - r_lon / 15 + itzone
    dusk_decimal = (dusk_angle_rad - eq_time) * 24 / TWOPI + 12 - r_lon / 15 + itzone

    # Check for constant daylight
    if dusk_decimal >= 999999:
        sunset_time = ""
        sunrise_time = "Always Day Light"
        return sunrise_time, sunset_time, srinc
    # Check for constant nighttime
    elif dusk_decimal <= -999999:
        sunrise_time = ""
        sunset_time = "Always Nightime"
        return sunrise_time, sunset_time, srinc

    # Function to convert decimal hours to hours and minutes
    def format_time(decimal_time):
        hours, remainder = divmod(abs(decimal_time), 1)
        minutes = round(remainder * 60)
        return f"{int(hours):02d}:{minutes:02d}"
    
    # Convert dawn and dusk times to hours and minutes
    sunrise_time = format_time(dawn_decimal)
    sunset_time = format_time(dusk_decimal)

    return sunrise_time, sunset_time, srinc

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
    coszs= 0.42914126440073946

    dusk_angle_rad = sunset(r_lat, sin_d, cos_d, rsm_ezm)
    
    print("DUSK_ANGLE_RAD=",dusk_angle_rad)

    sunrise_time, sunset_time, srinc = get_sunrise_sunset_times(dusk_angle_rad, eq_time, r_lon, itzone, coszt, sundis)
    print(f"Dawn: {sunrise_time}, Dusk: {sunset_time}, Solar Radiation: {srinc}")