import math
import numpy as np


def __distance_calc(origin_latitude,
                    origin_longitude,
                    destination_latitude,
                    destination_longitude,
                    circuity=1.17):

    ##Pull together origin_info
    origin_latitude = origin_latitude
    origin_longitude = origin_longitude

    origin_latitude_in_rads = (math.pi / 180) * origin_latitude
    origin_longitude_in_rads = (math.pi / 180) * origin_longitude

    orig_lat_cos = np.cos(origin_latitude_in_rads)

    origin_x = 0.5 * orig_lat_cos * np.sin(origin_longitude_in_rads)
    origin_y = 0.5 * orig_lat_cos * np.cos(origin_longitude_in_rads)
    origin_z = 0.5 * np.sin(origin_latitude_in_rads)

    ##Pull together destination_info
    destination_latitude = np.array(destination_latitude)
    destination_longitude = np.array(destination_longitude)

    destination_latitude_in_rads = (math.pi / 180) * destination_latitude
    destination_longitude_in_rads = (math.pi / 180) * destination_longitude

    dest_lat_cos = np.cos(destination_latitude_in_rads)

    destination_x = 0.5 * dest_lat_cos * np.sin(destination_longitude_in_rads)
    destination_y = 0.5 * dest_lat_cos * np.cos(destination_longitude_in_rads)
    destination_z = 0.5 * np.sin(destination_latitude_in_rads)

    ###Calculate Haversine distance for any group set of
    ###origin/destinations

    ##Now calculate the actual distance
    distance_x = origin_x - destination_x
    distance_y = origin_y - destination_y
    distance_z = origin_z - destination_z

    earth_radius = 3959

    ##Finally calculate the final distance
    distance = 2 * circuity * earth_radius * np.arcsin(np.sqrt((distance_x * distance_x +
                                                                distance_y * distance_y +
                                                                distance_z * distance_z)))

    return distance


def get_santa_haversine_distance(lat1, lon1, lat2, lon2):

    '''
        purpose: calculated the haversine distance with two coordinates.
                this function also includes a US reroute around the great lakes
                Western points will be rerouted through northern Illinois into Michigan
                and eastern points through northern Ohio

        inputs: floats for lat/long value pairs, string for id1 and id2

        returns: distance in miles as pd.DataFrame
    '''

    origin_latitude = np.array(lat1)
    origin_longitude = np.array(lon1)
    destination_latitude = np.array(lat2)
    destination_longitude = np.array(lon2)
    distances = np.repeat(-1.0, len(lat1))

    ## Now that we have the base haversine function, we want to caclculate the
    ## distance unless we have to reroute
    ## Start by splitting out the reroutes from the straight runs

    ##For reroutes through Shelby, IL (41.202074,-87.292187) we want everything
    ##north of 41.61447 and west of -87.292187
    ##For reroutes through Fremont, OH (41.366028,-83.120128) we want
    ##everything north of 41.74017 and east of -82.43449
    ##For the michigan location we will take everything north of 41.583367 and
    ##between -86.406281 and -82.943391
    ##TODO: Functionize the location groupings to make the code cleaner

    cross_lake = ((origin_latitude > 41.617447) &
                  (origin_longitude < -87.292187) &
                  (destination_latitude > 41.617447) &
                  (destination_longitude > -87.292187)) | \
                  ((destination_latitude > 41.617447) &
                   (destination_longitude < -87.292187) &
                   (origin_latitude > 41.617447) &
                   (origin_longitude > -87.292187))

    cross_canada = ((origin_latitude > 41.74017) &
                    (origin_longitude < -82.434449) &
                    (destination_latitude > 41.74017) &
                    (destination_longitude > -82.434449)) | \
                    ((destination_latitude > 41.74017) &
                     (destination_longitude < -82.434449) &
                     (origin_latitude > 41.74017) &
                     (origin_longitude > -82.434449))


    ##Now calculate the distances based on which matrix each location
    ##combination falls into

    ##Standard distances calculated by simply using the dist_calc function

    distances[(~cross_lake) & (~cross_canada)] = __distance_calc(\
        origin_latitude[(~cross_lake) & (~cross_canada)],\
        origin_longitude[(~cross_lake) & (~cross_canada)],\
        destination_latitude[(~cross_lake) & (~cross_canada)],\
        destination_longitude[(~cross_lake) & (~cross_canada)])

    ##Reroute IL by calculation from origin to shelby, IL and then from shelby,
    ##IL to destination

    reroute_illinois_distances = np.sum(cross_lake)
    distances[cross_lake] = \
          __distance_calc(origin_latitude[cross_lake],
                          origin_longitude[cross_lake],
                          np.repeat(41.202074, reroute_illinois_distances),
                          np.repeat(-87.292187, reroute_illinois_distances)) \
        + __distance_calc(np.repeat(41.202074, reroute_illinois_distances),
                          np.repeat(-87.292187, reroute_illinois_distances),
                          destination_latitude[cross_lake],
                          destination_longitude[cross_lake])

    ##Reroute IL by calculation from origin to fremont, OH and then from
    ##fremont, OH to destination

    reroute_ohio_distances = np.sum((~cross_lake) & (cross_canada))
    distances[(~cross_lake) & (cross_canada)] = \
          __distance_calc(origin_latitude[(~cross_lake) & (cross_canada)],
                          origin_longitude[(~cross_lake) & (cross_canada)],
                          np.repeat(41.366028, reroute_ohio_distances),
                          np.repeat(-83.120128, reroute_ohio_distances)) \
        + __distance_calc(np.repeat(41.366028, reroute_ohio_distances),
                          np.repeat(-83.120128, reroute_ohio_distances),
                          destination_latitude[(~cross_lake) & (cross_canada)],
                          destination_longitude[(~cross_lake) & (cross_canada)])

    return distances
