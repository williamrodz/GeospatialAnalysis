import pandas as pd
import matplotlib.pyplot as plt
import folium
from tqdm import tqdm

from geopy.geocoders import Nominatim

def get_coordinates_for_postal_code(postal_code):
    """
    Returns the latitude and longitude for a given Belgian postal code.
    If the postal code is not found, returns None.
    """
    geolocator = Nominatim(user_agent="belgian_postal_code_mapper")
    location = geolocator.geocode(f"{postal_code}, Belgium")
    if location:
        return location.latitude, location.longitude
    else:
        return None

# Replace 'your_file.csv' with the actual path to your file
df = pd.read_csv("CommutingData.csv")

# Show the first 5 rows (default behavior of head)
print(df.head())


# Assuming "Employee postal number" is the column name
postal_number_counts = df['Employee postal number'].value_counts()

# Print out the frequency of each postal number
print("Postal Number\tFrequency")
print("---------------------------")
for postal_number, frequency in postal_number_counts.items():
    print(f"{postal_number}\t\t{frequency}")


# Assuming "Employee postal number" is the column name
employee_postal_numbers = df['Employee postal number']

# Plot the histogram
plt.hist(employee_postal_numbers, bins=10, color='skyblue', edgecolor='black')
plt.title('Employee Postal Number Histogram')
plt.xlabel('Postal Number')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Create a map centered on Belgium
m = folium.Map(location=[50.8503, 4.3517], zoom_start=8)

# Iterate over postal numbers and add markers to the map
progress_bar = tqdm(total=len(postal_number_counts), desc="Processing Postal Codes")

for postal_number, frequency in postal_number_counts.items():
    # Retrieve latitude and longitude for the postal code (You need a mapping from postal codes to coordinates)
    # For demonstration, let's just use a dummy function
    lat, lon = get_coordinates_for_postal_code(postal_number)
    # Add marker for each occurrence
    folium.Marker([lat, lon], popup=f'Postal Number: {postal_number}\nFrequency: {frequency}').add_to(m)
    # Update the progress bar
    progress_bar.update(1)
progress_bar.close()

# Save the map to an HTML file
m.save('employee_postal_numbers_map.html')
