import math
import numpy as np


def __get_rads(latitude, longitude):

    latitude_rads = (math.pi / 180) * latitude
    longitude_rads = (math.pi / 180) * longitude

    latitude_cos = np.cos(latitude_rads)

    cord_x = 0.5 * latitude_cos * np.sin(longitude_rads)
    cord_y = 0.5 * latitude_cos * np.cos(longitude_rads)
    cord_z = 0.5 * np.sin(latitude_rads)

    return cord_x, cord_y, cord_z


def calculate_haversine_distance(from_latitude,
                                 from_longitude,
                                 to_latitude,
                                 to_longitude,
                                 circuity=1.17,
                                 earth_radius=3959):

    '''

    :param from_latitude: List of origin latitudes
    :param from_longitude: List of origin longitudes
    :param to_latitude: List of destination latitudes
    :param to_longitude: List of destination longitudes
    :param circuity:
    :param earth_radius:
    :return: List of distances
    '''

    from_latitude = np.array(from_latitude)
    from_longitude = np.array(from_longitude)

    to_latitude = np.array(to_latitude)
    to_longitude = np.array(to_longitude)

    from_x, from_y, from_z = __get_rads(from_latitude, from_longitude)
    to_x, to_y, to_z = __get_rads(to_latitude, to_longitude)

    distance_x = from_x - to_x
    distance_y = from_y - to_y
    distance_z = from_z - to_z

    distance = np.arcsin(np.sqrt((distance_x * distance_x +
                                  distance_y * distance_y +
                                  distance_z * distance_z)))

    distance = distance * 2 * circuity * earth_radius

    return distance
