import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.basemap import Basemap

# Read the CSV file into a DataFrame
df = pd.read_csv('CommutingData.csv', sep=',')

def plot_all_employees(df):
  # Plot all the points
  numpoints = 0
  for index, row in df.iterrows():
      color = 'blue' if row['Collar'] == 'b' else 'silver'
      plt.scatter(row['Longitude'], row['Latitude'], color=color)
      numpoints += 1

  # Add labels and title
  plt.xlabel('Longitude')
  plt.ylabel('Latitude')
  plt.title(f'Employee Locations (Total employees= {numpoints})')

  # Show plot
  plt.show()
   
def plot_specific_points(title, df, color):
  num_points = 0
  for index, row in df.iterrows():
      num_points += 1
      plt.scatter(row['Longitude'], row['Latitude'], color=color)

  # Add labels and title
  plt.xlabel('Longitude')
  plt.ylabel('Latitude')
  plt.title(f'{title} ({num_points} employees)')

  # Show plot
  plt.show()

def run_k_means(title, data_frame_sub_dimensions, num_clusters):
  print("")
  print(title)
  print(f"Running k means with {num_clusters} clusters")
   # Prepare data for clustering
  X = data_frame_sub_dimensions

  # Run KMeans clustering
  kmeans = KMeans(n_clusters=num_clusters)
  kmeans.fit(X)

  # Get cluster centers and labels
  cluster_centers = kmeans.cluster_centers_
  cluster_labels = kmeans.labels_

  # Plot the points with cluster centers
  
  plt.scatter(data_frame_sub_dimensions['Longitude'], data_frame_sub_dimensions['Latitude'], c=cluster_labels, cmap='viridis', alpha=0.5)
  plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], marker='x', color='red', s=100, label='Cluster Centers')

  # Annotate cluster centers with number of points
  for i, center in enumerate(cluster_centers):
      plt.annotate(f'Cluster {i+1}\n{sum(cluster_labels==i)} people', (center[0], center[1]), textcoords="offset points", xytext=(0,-20), ha='center')
      print(f"Center {center}: {sum(cluster_labels==i)} people")

  # Add labels and title
  plt.xlabel('Longitude')
  plt.ylabel('Latitude')
  plt.title(title)

  # Show plot
  plt.legend()
  plt.show()

white_collar_df = df[df['Collar'] == 'w']
blue_collar_df = df[df['Collar'] == 'b']
# print(df.head())
# print("")
# print(white_collar_df.head())

plot_all_employees(df)
plot_specific_points("White collar", white_collar_df, 'silver')
plot_specific_points("Blue collar", blue_collar_df, 'blue')

#run_k_means("White collar clustering", white_collar_df[['Longitude', 'Latitude']], 3,)
#run_k_means("Blue collar clustering", blue_collar_df[['Longitude', 'Latitude']], 3,)
#run_k_means("All employees", df[['Longitude', 'Latitude']], 3,)

for k_means_num_clusters in reversed(range(1,11)):
	run_k_means("White collar clustering", white_collar_df[['Longitude', 'Latitude']], k_means_num_clusters,)
	run_k_means("Blue collar clustering", blue_collar_df[['Longitude', 'Latitude']], k_means_num_clusters,)
	run_k_means("All employees", df[['Longitude', 'Latitude']], k_means_num_clusters,)

