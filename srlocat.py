from flask import Flask, send_from_directory, request, redirect, url_for, render_template
from timezone import get_time_zone
from calcs import loop_months

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')

def index():
    return app.send_static_file('srlocat.html')

@app.route('/process_form', methods=['POST'])

def process_form():
    # print(request.form) # AS NEEDED


    r_lat = request.form.get('LAT') or '40.015'  # Use '40.015' if LAT is empty or not submitted
    r_lon = request.form.get('LON') or '-105.270'
    year_str = request.form.get('YEAR') or '2024' # Default year if empty or not submitted
    month_str = request.form.get('MONTH') or '0'
    
    try:
        year = int(year_str)
    except ValueError:
        year = 2024  # Default year if conversion fails
    
    try:
        month = int(month_str)
    except ValueError:
        month = 0  # Default month if conversion fails

    time_zone,tzLow,tzHigh, itzone = get_time_zone(r_lon)

    # Ensure r_lat and r_lon are floats and format them with 3 decimal places
    try:
        formatted_r_lat = "{:.3f}".format(float(r_lat))

    except ValueError:

        formatted_r_lat = r_lat  # In case of conversion failure, use the original string
    
    try:
        formatted_r_lon = "{:.3f}".format(float(r_lon))

    except ValueError:

        formatted_r_lon = r_lon  # In case of conversion failure, use the original string

    # Attempt to convert latitude and longitude to float and check their ranges
    try:
        r_lat = float(r_lat)
        if not -90 <= r_lat <= 90:
            raise ValueError("Latitude out of range.")
    except ValueError:
        return render_template('error_page.html', error_message="Latitude out of range.")

    try:
        r_lon = float(r_lon)
        if not -360 <= r_lon <= 360:
            raise ValueError("Longitude out of range.")
    except ValueError:
        return render_template('error_page.html', error_message="Longitude out of range.")

    daily_data = loop_months(month,year,r_lat, r_lon)


    return render_template('print_to_screen.html', formatted_r_lat=formatted_r_lat, formatted_r_lon=formatted_r_lon, time_zone=time_zone, tzLow=tzLow, tzHigh=tzHigh, year=year, month=month, daily_data=daily_data)


if __name__ == '__main__':
    app.run(debug=True)
