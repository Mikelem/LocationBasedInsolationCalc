import json
import os

# This script depends on a JSON file named 'ctzone.json'

def load_data():
    """
    Load the time zone data from the JSON file.
    """
    # Construct the path to the JSON file
    file_path = os.path.join(os.path.dirname(__file__), 'static/data', 'ctzone.json')
    
    # Open and read the JSON data file
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_time_zone(r_lon):
    """
    Get the time zone for a given longitude.
    """
    # Convert the longitude to float
    r_lon = float(r_lon)

    # Load the time zone data
    ctzone = load_data()

    # Calculate the time zone index
    itzone = round(r_lon / 15)

    # Calculate the lower and upper bounds of the time zone
    tz_low = itzone * 15 - 7.5
    tz_high = itzone * 15 + 7.5

    # Convert the time zone index to string
    itzone_str = str(itzone)

    # Get the time zone from the data, or return "Invalid Time Zone" if not found
    time_zone = ctzone.get(itzone_str, "Invalid Time Zone")

    return time_zone, tz_low, tz_high, itzone

if __name__ == '__main__':
    # Test the function with a specific longitude
    r_lon = -105.270
    time_zone, tz_low, tz_high, itzone = get_time_zone(r_lon)

    # Print the results
    print("time_zone:", time_zone)
    print(f"(Longitudes {tz_low} to {tz_high})") 
    print("itzone:", itzone) 