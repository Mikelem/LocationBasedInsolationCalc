import math
import static.data.table_data as table_data
from config import RAD_PER_DEG, TWOPI

# Function to calculate obliquity
def calculate_obliquity(ym1950, table1):
    # Summation over the elements in table1
    sum_c = sum(table1[i][0] * math.cos(RAD_PER_DEG * (ym1950 * table1[i][1] / 3600 + table1[i][2])) for i in range(47))
    # Calculate obliquity in degrees
    obliqd = 23.320556 + sum_c / 3600
    # Convert obliquity to radians
    return obliqd * RAD_PER_DEG

# Function to calculate eccentricity
def calculate_eccentricity(ym1950, table4):
    # Calculate the sum of the product of elements in table4 and the sine of some angle
    sine_sum_table4 = sum(table4[i][0] * math.sin(RAD_PER_DEG * (ym1950 * table4[i][1] / 3600 + table4[i][2])) for i in range(19))
    # Calculate the sum of the product of elements in table4 and the cosine of some angle
    cosine_sum_table4 = sum(table4[i][0] * math.cos(RAD_PER_DEG * (ym1950 * table4[i][1] / 3600 + table4[i][2])) for i in range(19))
    # Calculate eccentricity using the Pythagorean theorem
    eccen = math.sqrt(sine_sum_table4**2 + cosine_sum_table4**2)
    # Return eccentricity and the sums used to calculate it
    return eccen, sine_sum_table4, cosine_sum_table4

# Function to calculate omegvp
def calculate_omegvp(ym1950, table5, pie):
    # Summation over the elements in table5
    fsinfd = sum(table5[i][0] * math.sin(RAD_PER_DEG * (ym1950 * table5[i][1] / 3600 + table5[i][2])) for i in range(78))
    # Calculate PSI
    psi = RAD_PER_DEG * (3.392506 + (ym1950 * 50.439273 + fsinfd) / 3600)
    # Calculate omegvp
    return (pie + psi + 0.5 * TWOPI) % TWOPI

# Main function to calculate orbital parameters
def orbpar(year):
    # Calculate the number of years since 1950
    ym1950 = year - 1950
    # Calculate obliquity using the calculate_obliquity function
    obliq = calculate_obliquity(ym1950, table_data.TABLE1)
    # Calculate eccentricity and the sums used to calculate it using the calculate_eccentricity function
    eccen, sine_sum_table4, cosine_sum_table4 = calculate_eccentricity(ym1950, table_data.TABLE4)
    # Calculate PIE using the atan2 function
    pie = math.atan2(sine_sum_table4, cosine_sum_table4)
    # Calculate omegvp using the calculate_omegvp function
    omegvp = calculate_omegvp(ym1950, table_data.TABLE5, pie)
    # Return the calculated parameters
    return eccen, obliq, omegvp

if __name__ == '__main__':
    # Test the function with the year 2024
    year = 2024
    eccen, obliq, omegvp = orbpar(year)
    print("Obliquity: ", obliq)
    print("Eccentricity: ", eccen)  
    print("Omegvp: ", omegvp)