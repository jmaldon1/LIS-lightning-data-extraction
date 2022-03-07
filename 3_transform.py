import csv
# from math import sin, cos, sqrt, asin, radians

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from shapely.geometry import MultiPoint


# def read_csv(csv_file):
#     with open(csv_file, "r") as f:
#         reader = csv.reader(f)
#         next(reader)  # skip header
#         coords = []
#         for lat, lon in reader:
#             coords.append((float(lat), float(lon)))
#     return coords

def csv_to_df(csv_file):
    df = pd.read_csv(csv_file)
    return df

def get_centermost_point(cluster):
    print("cluster len: ", len(cluster))
    cluster_weight = len(cluster)
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)


def main():
    coords_df = csv_to_df("lightning_lat_lon.csv")
    coords = coords_df.to_numpy()

    kms_per_radian = 6371.0088
    epsilon = 1.5 / kms_per_radian

    print("Calculating clusters...")
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels))
    clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])
    print('Number of clusters: {}'.format(num_clusters))
    print(clusters)

    centermost_points = clusters.map(get_centermost_point)

if "__main__" == __name__:
    main()
