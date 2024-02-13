from flask import Flask, send_from_directory, request, redirect, url_for, render_template
from timezone import get_time_zone
from calcs import loop_months

srlocat = Flask(__name__, static_url_path='', static_folder='static')

@srlocat.route('/')

def index():
    return srlocat.send_static_file('srlocat.html')

@srlocat.route('/process_form', methods=['POST'])

def process_form():
    # Extract the form data
    r_lat = request.form.get('LAT', 'Not specified')
    r_lon = request.form.get('LON', 'Not specified')
    year = int(request.form.get('YEAR', 'Not specified'))
    month = int(request.form.get('MONTH', 'Not specified'))

    time_zone,tzLow,tzHigh, itzone = get_time_zone(r_lon)

    print("r_lat type:", type(r_lat))
    # Ensure r_lat and r_lon are floats and format them with 3 decimal places
    try:
        formatted_r_lat = "{:.3f}".format(float(r_lat))

    except ValueError:

        formatted_r_lat = r_lat  # In case of conversion failure, use the original string
    
    try:
        formatted_r_lon = "{:.3f}".format(float(r_lon))

    except ValueError:

        formatted_r_lon = r_lon  # In case of conversion failure, use the original string

    r_lat = float(r_lat)
    r_lon = float(r_lon)
    daily_data = loop_months(month,year,r_lat, r_lon)


    return render_template('print_to_screen.html', formatted_r_lat=formatted_r_lat, formatted_r_lon=formatted_r_lon, time_zone=time_zone, tzLow=tzLow, tzHigh=tzHigh, year=year, month=month, daily_data=daily_data)


if __name__ == '__main__':
    srlocat.run(debug=True)
