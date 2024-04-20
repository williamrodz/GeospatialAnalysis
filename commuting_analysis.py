import pandas as pd
import matplotlib.pyplot as plt
import folium
from tqdm import tqdm
import geopandas as gpd
from folium.plugins import MarkerCluster
import matplotlib.cm as cm
from matplotlib.colors import rgb2hex
import webbrowser


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
# print(df.head())


# # Assuming "Employee postal number" is the column name
# postal_number_counts = df['Employee postal number'].value_counts()

# # Print out the frequency of each postal number
# print("Postal Number\tFrequency")
# print("---------------------------")
# for postal_number, frequency in postal_number_counts.items():
#     print(f"{postal_number}\t\t{frequency}")


# # Assuming "Employee postal number" is the column name
# employee_postal_numbers = df['Employee postal number']

# # Plot the histogram
# plt.hist(employee_postal_numbers, bins=10, color='skyblue', edgecolor='black')
# plt.title('Employee Postal Number Histogram')
# plt.xlabel('Postal Number')
# plt.ylabel('Frequency')
# plt.grid(True)
# plt.show()

# Create a map centered on Belgium
m = folium.Map(location=[50.8503, 4.3517], zoom_start=8)

# # Iterate over postal numbers and add markers to the map
# progress_bar = tqdm(total=len(postal_number_counts), desc="Processing Postal Codes")


postcodes_to_coordinates = {}
postcodes_to_counts = {}



# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Get the value of the target column for the current row
    postcode = row["Employee postal number"]
    latitude,longitude = (row["Latitude"],row["Longitude"])
    postcodes_to_coordinates[postcode] = (latitude,longitude)
    if not (postcode  in postcodes_to_counts):
        postcodes_to_counts[postcode] = 1
    else:
        postcodes_to_counts[postcode] += 1

maximum_frequency = max(list(postcodes_to_counts.values()))


for postcode in postcodes_to_counts:
    # Retrieve latitude and longitude for the postal code (You need a mapping from postal codes to coordinates)
    # For demonstration, let's just use a dummy function
    lat, lon = postcodes_to_coordinates[postcode]
    frequency = postcodes_to_counts[postcode]
    # Add marker for each occurrence
    folium.Marker([lat, lon], popup=f'Postal Number: {postcode}\nFrequency: {frequency}').add_to(m)
    # Update the progress bar


coordinates_to_counts = {postcodes_to_coordinates[postcode]:postcodes_to_counts[postcode] for postcode in postcodes_to_coordinates}
print(coordinates_to_counts)


# Save the map to an HTML file
m.save('employee_postal_numbers_map.html')



# Load the geographic data of Belgium
belgium = gpd.read_file("georef-belgium-postal-codes.shx")
print(belgium.columns)

# Sample dictionary with coordinates or postcodes and employee counts
# Replace this with your actual dictionary

# Convert the dictionary to a DataFrame
# import pandas as pd
employee_df = pd.DataFrame(list(coordinates_to_counts.items()), columns=["coordinates", "employee_count"])

# # Create a GeoDataFrame from the DataFrame with coordinates
gdf = gpd.GeoDataFrame(employee_df, geometry=gpd.points_from_xy(employee_df['coordinates'].apply(lambda x: x[1]), employee_df['coordinates'].apply(lambda x: x[0])))

# # Normalize employee counts to adjust marker sizes
max_count = employee_df['employee_count'].max()
min_count = employee_df['employee_count'].min()
normalized_sizes = (employee_df['employee_count'] - min_count) / (max_count - min_count)

# # Plot the map
fig, ax = plt.subplots(figsize=(10, 10))
belgium.plot(ax=ax, color='lightgrey')
gdf.plot(ax=ax, color='red', markersize=normalized_sizes * 100, alpha=0.5, label='Employee Locations')
plt.title("Employee Locations in Belgium")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()
# plt.show()




# Create a Folium map centered around Belgium
belgium_weight_map = folium.Map(location=[50.8503, 4.3517], zoom_start=8)

# Calculate the maximum and minimum employee counts
max_count = max(coordinates_to_counts.values())
min_count = min(coordinates_to_counts.values())

# Define a colormap
colormap = cm.viridian_r

# Add circle markers to the map
for coord, count in coordinates_to_counts.items():
    # Normalize the radius based on employee count
    normalized_radius = (count - min_count) / (max_count - min_count) * 40  # Adjust the multiplier for desired scale
    
    # Normalize the count inversely to map it to a color
    normalized_count = 1 - ((count - min_count) / (max_count - min_count))
    color = rgb2hex(colormap(normalized_count)[:3])
    
    folium.CircleMarker(location=coord, 
                        radius=normalized_radius,  
                        color=color,
                        fill=True,
                        fill_opacity=0.9).add_to(belgium_weight_map)

# Display the map
html_file_path = "belgium_weight_employees_map.html"

belgium_weight_map.save(html_file_path)
# Open the HTML file in the default web browser
webbrowser.open(html_file_path)