def ymd_to_days(year, month, adjDayFrac):

    """
    For a given year (A.D.), month, and date (between 0 and 31),
    calculate the number of days measured from 2000 January 1, hour 0.
    """
    # Constants for day counts in various periods
    JDAY4C = 365 * 400 + 97  # days in 4 centuries
    JDAY1C = 365 * 100 + 24  # days in 1 century
    JDAY4Y = 365 * 4 + 1     # days in 4 years
    JDAY1Y = 365             # days in 1 year

    # Days sum for non-leap and leap years
    JDSUMN = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    JDSUML = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]

    # Calculate components
    N4CENT = (year - 2000) // 400
    IYR4C = year - 2000 - N4CENT * 400
    N1CENT = IYR4C // 100
    IYR1C = IYR4C - N1CENT * 100
    N4YEAR = IYR1C // 4
    IYR4Y = IYR1C - N4YEAR * 4
    N1YEAR = IYR4Y
    
    # Calculate days
    days_from_y2k = N4CENT * JDAY4C
    if N1CENT > 0:
        days_from_y2k += JDAY1C + 1 + (N1CENT - 1) * JDAY1C
        if N4YEAR > 0:
            days_from_y2k += JDAY4Y - 1 + (N4YEAR - 1) * JDAY4Y
        else:
            days_from_y2k += N1YEAR * JDAY1Y
    else:
        days_from_y2k += N4YEAR * JDAY4Y
        if N1YEAR > 0:
            days_from_y2k += 0  # Placeholder for potential additional logic

    # Adjust for month and day, considering leap year
    is_leap_year = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
    if is_leap_year:
        days_from_y2k += JDSUML[month - 1] + adjDayFrac
    else:
        days_from_y2k += JDSUMN[month - 1] + adjDayFrac

    return days_from_y2k

if __name__ == '__main__':
    r_lon = -105.270
    year = 2024
    month = 2
    adjDayFrac = 5.833333333333333
    adjDayFrac = 1-1 + .5 - r_lon/360 # 0.7924166666666667
    print("ADJ DAY =", adjDayFrac)
    days_from_y2k = ymd_to_days(year, month, adjDayFrac) #8797.792416666667
    print("days_from_y2k:", days_from_y2k)