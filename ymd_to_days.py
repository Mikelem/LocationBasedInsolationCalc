def ymd_to_days(year, month, adj_day_frac):
    """
    For a given year (A.D.), month, and date (between 0 and 31),
    calculate the number of days measured from 2000 January 1, hour 0.
    """
    # Constants for day counts in various periods
    days_in_4_centuries = 365 * 400 + 97
    days_in_1_century = 365 * 100 + 24
    days_in_4_years = 365 * 4 + 1
    days_in_1_year = 365

    # Days sum for non-leap and leap years
    days_sum_non_leap = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    days_sum_leap = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]

    # Calculate components
    n_4_cent = (year - 2000) // 400
    i_yr_4_c = year - 2000 - n_4_cent * 400
    n_1_cent = i_yr_4_c // 100
    i_yr_1_c = i_yr_4_c - n_1_cent * 100
    n_4_year = i_yr_1_c // 4
    i_yr_4_y = i_yr_1_c - n_4_year * 4
    n_1_year = i_yr_4_y

    # Calculate days
    days_from_y2k = n_4_cent * days_in_4_centuries
    if n_1_cent > 0:
        days_from_y2k += days_in_1_century + 1 + (n_1_cent - 1) * days_in_1_century
        if n_4_year > 0:
            days_from_y2k += days_in_4_years - 1 + (n_4_year - 1) * days_in_4_years
        else:
            days_from_y2k += n_1_year * days_in_1_year
    else:
        days_from_y2k += n_4_year * days_in_4_years
        if n_1_year > 0:
            days_from_y2k += 0  # Placeholder for potential additional logic

    # Adjust for month and day, considering leap year
    is_leap_year = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
    if is_leap_year:
        days_from_y2k += days_sum_leap[month - 1] + adj_day_frac
    else:
        days_from_y2k += days_sum_non_leap[month - 1] + adj_day_frac

    return days_from_y2k


if __name__ == '__main__':
    r_lon = -105.270
    year = 2024
    month = 2
    adj_day_frac = 1 - 1 + .5 - r_lon / 360  # 0.7924166666666667
    print("ADJ DAY =", adj_day_frac)
    days_from_y2k = ymd_to_days(year, month, adj_day_frac)  # 8797.792416666667
    print("days_from_y2k:", days_from_y2k)