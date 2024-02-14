# Import necessary modules and constants
from ymd_to_days import ymd_to_days
from orbpar import orbpar
from orbit import orbit
from coszij import coszij
from sunset import sunset, get_sunrise_sunset_times
from config import TWOPI, RSUNd, REFRAC, days_per_month


def generate_daily_data(year, month, date, r_lon, itzone, eccen, obliq, omegvp, r_lat):
    adj_day_frac = date - 1 + 0.5 - r_lon / 360
    days_from_y2k = ymd_to_days(year, month, adj_day_frac)
    sin_d, cos_d, sundis, sun_lon, sun_lat, eq_time = orbit(eccen, obliq, omegvp, days_from_y2k)
    coszt, coszs = coszij(r_lat, sin_d, cos_d)
    rsm_ezm = (REFRAC + RSUNd / sundis) * TWOPI / 360
    dusk_angle_rad = sunset(r_lat, sin_d, cos_d, rsm_ezm)
    sunrise_time, sunset_time, srinc = get_sunrise_sunset_times(dusk_angle_rad, eq_time, r_lon, itzone, coszt, sundis)
    formatted_date = f"{year}/{month:02}/{date:02}" if date == 1 else f"{date:0>2}"
    data = {
        'date': formatted_date,
        'sunrise_time': f'{sunrise_time:9}',
        'sunset_time': f'{sunset_time:9}',
        'avg_sunlight': srinc,
        'cosine_zenith': coszs
    }
    return data


def is_leap_year(year):
    return (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0)


def loop_months(month, year, r_lat, r_lon):
    eccen, obliq, omegvp = orbpar(year)
    itzone = round(r_lon / 15)
    mo_min = 1 if month == 0 else month
    mo_max = 12 if month == 0 else month
    daily_data = []
    for month in range(mo_min, mo_max + 1):
        date_max = 29 if month == 2 and is_leap_year(year) else days_per_month.get(month, 30)
        for date in range(1, date_max + 1):
            data = generate_daily_data(year, month, date, r_lon, itzone, eccen, obliq, omegvp, r_lat)
            daily_data.append(data)
    return daily_data


if __name__ == '__main__':

    # Test scenarios:
    boulder = (2, 2024, 40.015, -105.270)
    mcmurdo = (2, 2024, -77.85, 166.667)
    ellesmere = (2, 2024, 78.7833, -72.5000)
    denver = (2, 2024, 39.739, -104.9903)
    daily_data = loop_months(*ellesmere)
    # Check print out for data
    for data in daily_data:
        print(f"{data['date']:>10}{data['sunrise_time']:>18}{data['sunset_time']:>18}{data['avg_sunlight']:11.2f}{data['cosine_zenith']:11.3f}")