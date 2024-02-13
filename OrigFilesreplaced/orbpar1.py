import math
import static.data.table_data as table_data
from config import TWOPI, RAD_PER_DEG
# Import table_data.py (could also be json file)

# Gets the orbital parameters for a given year

# Input:  year   = years A.D. are positive, B.C. are negative
# Output: eccen  = eccentricity of orbital ellipse
#         obliq  = latitude of Tropic of Cancer in radians
#         omegvp = longitude of perihelion =
#                = spatial angle from vernal equinox to perihelion
#                  in radians with sun as angle vertex

def orbpar(year):

    TABLE1 = table_data.TABLE1
    TABLE4 = table_data.TABLE4
    TABLE5 = table_data.TABLE5

    YM1950 = year - 1950

    # Calculate Obliquity (OBLIQ) 110
    SUMC = 0
    for i in range(47):
        ARG = RAD_PER_DEG * (YM1950 * TABLE1[i][1] / 3600 + TABLE1[i][2])
        SUMC += TABLE1[i][0] * math.cos(ARG)
    OBLIQD = 23.320556 + SUMC / 3600
    obliq = OBLIQD * RAD_PER_DEG

    # Calculate Eccentricity (eccen)  210
    ESINPI = 0
    ECOSPI = 0
    for i in range(19):
        ARG = RAD_PER_DEG * (YM1950 * TABLE4[i][1] / 3600 + TABLE4[i][2])
        ESINPI += TABLE4[i][0] * math.sin(ARG)
        ECOSPI += TABLE4[i][0] * math.cos(ARG)

    eccen = math.sqrt(ESINPI**2 + ECOSPI**2)
 
    # PIE   = ATan2(ESINPI,ECOSPI) aTan2 is used to calculate the arctangent of y/x
    PIE = math.atan2(ESINPI, ECOSPI)
    FSINFD = 0
    for i in range(78): #Do 310 I=1,78
        ARG    = RAD_PER_DEG * (YM1950 * TABLE5[i][1] / 3600 + TABLE5[i][2])
        FSINFD +=  TABLE5[i][0] * math.sin(ARG)

    PSI    = RAD_PER_DEG * (3.392506+(YM1950*50.439273 +FSINFD)/3600)

    omegvp = (PIE + PSI + 0.5 * TWOPI) % TWOPI

    return eccen, obliq, omegvp

if __name__ == '__main__':
    # main()
        
    year = 2024
    eccen, obliq, omegvp = orbpar(year)

    print("OBLIQ-Obliquity: ", obliq)
    print("ECCEN-Eccentricity: ", eccen)  
    print("OMEGVP: ", omegvp)
    # Results:
    # OBLIQ-Obliquity =  0.4090466375073551
    # ECCEN-Eccentricity:  0.016693907860030634
    # OMEGVP:  4.9446341796410085
