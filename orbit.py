import numpy as np
from config import TWOPI, EDAYzY, VE2000

def orbit(eccen, obliq, omegvp, DaysFromY2K):

    BSEMI = np.sqrt(1 - eccen**2)
    TAofVE = -omegvp
    EAofVE = np.arctan2(BSEMI * np.sin(TAofVE), eccen + np.cos(TAofVE))
    MAofVE = EAofVE - eccen * np.sin(EAofVE)

    MA = (TWOPI * (DaysFromY2K - VE2000) / EDAYzY + MAofVE) % TWOPI

    EA = MA + eccen * (np.sin(MA) + eccen * np.sin(2 * MA) / 2)
    while True:
        dEA = (MA - EA + eccen * np.sin(EA)) / (1 - eccen * np.cos(EA))
        EA += dEA
        if np.abs(dEA) < 1e-10:
            break

    SUNDIS = 1 - eccen * np.cos(EA)
    TA = np.arctan2(BSEMI * np.sin(EA), np.cos(EA) - eccen)

    SIND = np.sin(TA - TAofVE) * np.sin(obliq)
    COSD = np.sqrt(1 - SIND**2)
    SUNX = np.cos(TA - TAofVE)
    SUNY = np.sin(TA - TAofVE) * np.cos(obliq)
    SLNORO = np.arctan2(SUNY, SUNX)

    VEQLON = TWOPI * VE2000 - TWOPI / 2 + MAofVE - TAofVE
    ROTATE = TWOPI * (DaysFromY2K - VE2000) * (EDAYzY + 1) / EDAYzY
    SUNLON = (SLNORO - ROTATE - VEQLON) % TWOPI
    if SUNLON > TWOPI / 2:
        SUNLON -= TWOPI
    SUNLAT = np.arcsin(np.sin(TA - TAofVE) * np.sin(obliq))

    SLMEAN = TWOPI / 2 - TWOPI * (DaysFromY2K - np.floor(DaysFromY2K))
    EQTIME = (SLMEAN - SUNLON) % TWOPI
    if EQTIME > TWOPI / 2:
        EQTIME -= TWOPI

    return SIND, COSD, SUNDIS, SUNLON, SUNLAT, EQTIME

if __name__ == '__main__':
    # ORBPAR returned: eccen, obliq, omegvp
    # YMDtoD returned: DaysFromY2K
    obliq = 0.4090466375073551
    eccen = 0.016693907860030634
    omegvp = 4.9446341796410085
    DaysFromY2K = 8797.792416666667
    SIND, COSD, SUNDIS, SUNLON, SUNLAT, EQTIME = orbit(eccen, obliq, omegvp, DaysFromY2K)

    print("SIND=",SIND)
    print("COSD=",COSD)
    print("SUNDIS=",SUNDIS)
    print("SUNLON=",SUNLON)
    print("SUNLAT=",SUNLAT)
    print("EQTIME=",EQTIME)
    SIND= -0.2936935287630569
    COSD= 0.9558996344610158
    SUNDIS= 0.985347907494622
    SUNLON= -1.7782592506134591
    SUNLAT= -0.2980884859599151
    EQTIME= -0.05904885296383622