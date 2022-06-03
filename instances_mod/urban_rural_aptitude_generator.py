import os
import numpy
import random
import math
import collections

import scipy.spatial

import sklearn.cluster
import sklearn.metrics

import matplotlib.pyplot

from sklearn.utils.extmath import density
from numpy.core.defchararray import center


density_per_min = None
ratio_urban_centers = None

max_urban_distance = None
save_figure = None
show_figure = None

# DBSCAN optional parameters and default values
density_clustering_per_distance = None


center_distances_methods = [
    "clustering", 
    "center_seeds", 
    "one_clustering"
]

density_methods = [
    "dbscan",
    "optics"
]



def generate_aptitude(points, number_urban_centers, method):

    distances_to_center = None
    labels = None

    if (method == "clustering"):
        distances_to_center = (
            generate_aptitude_by_clustering(points, number_urban_centers)
        )

    if (method == "center_seeds"):
        distances_to_center = (
            generate_aptitude_by_center_seeds(points, number_urban_centers)
        )
    
    if (method == "one_clustering"):
        distances_to_center = (
            generate_aptitude_by_one_clustering(points)
        )

    if (method == "dbscan"):
        labels = (
            generate_aptitude_by_DBSCAN_clustering(points)
        )
    
    if (method == "optics"):
        labels = (
            generate_aptitude_by_OPTICS_clustering(points)
        )
    

    # Min number 
    if (
        method in center_distances_methods
        and distances_to_center is None
    ):
        return None

    if (method in center_distances_methods):
        points_classif = (
            classify_using_distances_to_center(
                points, 
                distances_to_center, 
                method
            )
        )

    if (method in density_methods):
        points_classif = (
            classify_using_density(points, labels)
        )

    for i, point in enumerate(points):
        if (points_classif[i] == 0):
            matplotlib.pyplot.scatter(
                point[0],
                point[1],
                color="blue"
            )
        if (points_classif[i] == 1):
            matplotlib.pyplot.scatter(
                point[0],
                point[1],
                color="red"
            )

    return points_classif


def generate_aptitude_by_DBSCAN_clustering(points):
    points_arr = numpy.array(points)

    max_lat_lon = numpy.max(points_arr, axis=0)
    max_lat = max_lat_lon[0]
    max_lon = max_lat_lon[1]

    min_lat_lon = numpy.min(points_arr, axis=0)
    min_lat = min_lat_lon[0]
    min_lon = min_lat_lon[1]


    axis_x_size = abs(max_lat - min_lat)
    axis_y_size = abs(max_lon - min_lon)

    min_axis = min(axis_x_size, axis_y_size)
    min_distance_dbscan = abs(
        min_axis 
        * density_clustering_per_distance
    )

    if (min_distance_dbscan <= 0):
        min_distance_dbscan = 0.01

    dbscan = sklearn.cluster.DBSCAN(
        eps=min_distance_dbscan,
        metric="haversine",
        min_samples=2
    )

    dbscan.fit(points_arr)

    labels = []
    for i in range(len(dbscan.labels_)):
        if (dbscan.labels_[i] == -1):
            labels.append("unlabeld")
        else:
            labels.append(int(dbscan.labels_[i]))

    return labels

def generate_aptitude_by_OPTICS_clustering(points):
    points_arr = numpy.array(points)

    max_lat_lon = numpy.max(points_arr, axis=0)
    max_lat = max_lat_lon[0]
    max_lon = max_lat_lon[1]

    min_lat_lon = numpy.min(points_arr, axis=0)
    min_lat = min_lat_lon[0]
    min_lon = min_lat_lon[1]


    axis_x_size = abs(max_lat - min_lat)
    axis_y_size = abs(max_lon - min_lon)

    min_axis = min(axis_x_size, axis_y_size)
    min_distance_optics = min_axis * density_clustering_per_distance

    optics = sklearn.cluster.OPTICS(
        eps=min_distance_optics,
        metric="haversine",
        cluster_method="dbscan",
        min_samples=2
    )

    optics.fit(points_arr)

    labels = []
    for i in range(len(optics.labels_)):
        if (optics.labels_[i] == -1):
            labels.append("unlabeld")
        else:
            labels.append(int(optics.labels_[i]))

    return labels


def generate_aptitude_by_one_clustering(points):
    points_arr = numpy.array(points)

    kmeans = sklearn.cluster.KMeans(n_clusters=1)
    kmeans.fit(points_arr)
    
    matplotlib.pyplot.scatter(
        kmeans.cluster_centers_[:,0],
        kmeans.cluster_centers_[:,1],
        color="black"
    )
    for x,y in kmeans.cluster_centers_:
        matplotlib.pyplot.annotate(
            "center",
            (x,y),
            textcoords="offset points",
            xytext=(0,10),
            ha="center"
        )

    distances_to_center = scipy.spatial.distance.cdist(
                    points_arr,
                    kmeans.cluster_centers_,
                    metric="euclidean"
                )

    return distances_to_center


def generate_aptitude_by_clustering(points, number_of_clusters):

    points_arr = numpy.array(points)

    kmeans = sklearn.cluster.KMeans(n_clusters=number_of_clusters)
    kmeans.fit(points_arr)
    
    matplotlib.pyplot.scatter(
        kmeans.cluster_centers_[:,0],
        kmeans.cluster_centers_[:,1],
        color="black"
    )
    for x,y in kmeans.cluster_centers_:
        matplotlib.pyplot.annotate(
            "center",
            (x,y),
            textcoords="offset points",
            xytext=(0,10),
            ha="center"
        )

    distances_to_center = scipy.spatial.distance.cdist(
                    points_arr,
                    kmeans.cluster_centers_,
                    metric="euclidean"
                )

    return distances_to_center


def generate_aptitude_by_center_seeds(points, number_of_seeds):

    points_set = set(points)

    center_seeds = set()

    first_point = points[random.randint(0, len(points)-1)]

    center_seeds.add(first_point)
    number_of_seeds -= 1

    points_set.remove(first_point)

    candidates_set_size = math.ceil(len(points)**(1/2))

    while(number_of_seeds > 0):
        candidates_set = random.sample(points_set, candidates_set_size)

        number_of_seeds -= 1

        candidates_arr = numpy.array(candidates_set)
        center_seeds_arr = numpy.array(list(center_seeds))


        distances = scipy.spatial.distance.cdist(
                                    candidates_arr, 
                                    center_seeds_arr,
                                    metric="euclidean"
                                )

        seed_position = numpy.argmax(numpy.amin(distances, axis=1))

        center_seeds.add(candidates_set[seed_position])
        points_set.remove(candidates_set[seed_position])

    points_arr = numpy.array(points)
    center_seeds_arr = numpy.array(list(center_seeds))


    matplotlib.pyplot.scatter(
        center_seeds_arr[:,0],
        center_seeds_arr[:,1],
        color="black"
    )
    for x,y in center_seeds_arr:
        matplotlib.pyplot.annotate(
            "center",
            (x,y),
            textcoords="offset points",
            xytext=(0,10),
            ha="center"
        )

    distances_to_center_seeds = scipy.spatial.distance.cdist(
                    points_arr,
                    center_seeds_arr,
                    metric="euclidean"
                )

    return distances_to_center_seeds


def classify_using_distances_to_center(points, distances_to_center, method):
    distances = scipy.spatial.distance.cdist(
        points, 
        points,
        metric="euclidean"
    )

    space_max_size = distances.max()
    abs_max_urban_distance = (space_max_size * max_urban_distance)/2
    points_min_distance = numpy.amin(distances_to_center, axis=1)

    urb_rur_points = []

    for i in range(len(points)):
        # print(points_min_distance[i], abs_max_urban_distance)
        if (points_min_distance[i] == 0 
            and method == "clustering"):
            urb_rur_points.append(1)
            continue
        
        if (points_min_distance[i] > abs_max_urban_distance):
            urb_rur_points.append(1)
            continue

        urb_rur_points.append(0)
    return urb_rur_points


def classify_using_density(points, labels):
    dict_label_num_points = dict(collections.Counter(labels))

    densities = {}
    for key, value in dict_label_num_points.items():
        densities[key] = float(value) / float(len(labels))

    urb_rur_points = []

    for index in range(len(points)):
        label = labels[index]
        if (
            label == "unlabeld"
            or densities[label] < density_per_min
        ):
            urb_rur_points.append(1)
        else:
            urb_rur_points.append(0)

    return urb_rur_points




def get_urb_rural_division(
    points, 
    method, 
    figure_path=".", 
    figure_name="no_name"
):
    number_urban_centers = math.ceil(
                                (
                                    len(points) 
                                    * ratio_urban_centers
                                ) 
                            )

    urban_rural_aptitude = generate_aptitude(
        points, 
        number_urban_centers, 
        method
    )

    if (show_figure):
        matplotlib.pyplot.show()
    
    if (save_figure):

        matplotlib.pyplot.gca().set_aspect('equal', adjustable='box')
        matplotlib.pyplot.xticks(rotation=-15)

        fig_name = "fig_" + figure_name + "_gen_by_" + method + ".png"
        fig_file_name = os.path.join(figure_path, fig_name)
        print(fig_file_name)
        matplotlib.pyplot.savefig(fig_file_name)

    return urban_rural_aptitude