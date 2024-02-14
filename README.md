# LocationBasedInsolationCalc

Calculates the Insolation at a particular site for a month or a year at a time.

It takes in 4 variables:
Lat, Lon, Year, Month (Month can be a number from 1-12, for one month at a time or 0 for a complete year)

This program can run in two ways:

### 1. In a Flask environment as a web page which simulates the NASA site at:

https://data.giss.nasa.gov/modelE/ar5plots/srlocat.html

and is launched via the srlocat.py program

``` bash
$ flask run --app srlocat
```

then:

``` bash
$ srlocat.py
```

Running on a local server: http://127.0.0.1:5000


### 2. Or it can be run locally via the command line and output lines of data in the Terminal window:

``` bash
$ calcs.py
```

This will output the results to the Terminal.

In the calcs.py main block there are three default locations.

``` python
boulder = (2, 2024, 40.015, -105.270)
mcmurdo = (2, 2024, -77.85, 166.667)
denver = (2, 2024, 39.739, -104.9903)
```

Alternatively, you can create your own tuple with (month, year, lat, lon) and substitute it in the line:

''' python
daily_data = loop_months(*your_locale)
'''

``` python 
daily_data = loop_months(*mcmurdo)
# Print out the lines of data:
for data in daily_data:
    print(f"{data['date']:>10}{data['sunrise_time']:>13}{data['sunset_time']:>13}{data['avg_sunlight']:11.2f}{data['cosine_zenith']:11.3f}")
```