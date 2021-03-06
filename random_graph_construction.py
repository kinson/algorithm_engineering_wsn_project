import numpy
import os
import math
from operator import itemgetter
import matplotlib.pyplot as plt

# get n distributed points in square
def get_n_points_on_square(n):
    """Return n uniformly distributed points within a square as a list of lists."""
    points = numpy.random.uniform(0, 1, (n, 2))
    return [ (p[0], p[1]) for p in points ]

def get_n_points_on_disk(n):
    """Return n uniformly distributed points within a disk as a list of lists."""
    r = numpy.random.uniform(0, 1, (n))
    r = list(map(lambda x: math.sqrt(x), r))
    theta = numpy.random.uniform(0, 2*math.pi, (n))
    theta = list(map(lambda x: [math.cos(x), math.sin(x)], theta))
    points = [[i*j[0], i*j[1]] for i, j in zip(r, theta)]

    return [ (p[0], p[1]) for p in points ]

# graph points on unit square
def get_x_y_list(points):
    """Return tuple of two lists with the x coordinates in one and the y coordinates in the other."""
    x_points = list(map(lambda x: x[0], points))
    y_points = list(map(lambda x: x[1], points))
    return (x_points, y_points)

def plot_points(points):
    """Create plot mapping points plane."""
    x_y_p = get_x_y_list(points)
    plt.plot(x_y_p[0], x_y_p[1], 'r.')
    plt.axis([-1, 1, -1, 1])
    plt.show()

# using number of points and avg degree, calculate connection radius
def get_unit_square_connection_radius(n_points, avg_degree):
    """Return max edge length to use for connecting graph.

    d = average degree
    n = number of points
    R = radius of connection

    Formula for calculating radius for unit square: R = sqrt( d / (n*pi) )
    """
    return math.sqrt( avg_degree / (n_points * math.pi) )

def get_unit_circle_connection_radius(n_points, avg_degree):
    """Return max edge length to use for connecting graph.

    d = average degree
    n = number of points
    R = radius of connection

    Formula for calculating radius for unit circle: R = sqrt( d / n )
    """
    return math.sqrt( avg_degree / n_points )

def get_bucket_size(connection_radius):
    """Return the side lengths of the squares that will be used as buckets for
    determining point connections. Get the side length for a square inscribed in
    a circle of a given radius.


    Formula for calculating side length: L = sqrt( (2*r)^2 / 2 )
    """
    return math.sqrt( (2*connection_radius)**2 / 2 )

# determine bucket dimensions from side length and instantiate buckets
def get_bucket_dimensions(side_length):
    """Return number of buckets in the x and y dimensions to put points into using the
    bucket size. Use the floor of this number to determine the number of buckets."""
    return math.ceil(1/side_length)

def create_buckets_for_points(num_buckets):
    """Return list of lists of lists to put points into (as buckets)."""
    br = range(num_buckets)
    return [ [ [] for i in br ] for j in br]

#fill buckets
def get_bucket_index(coord, b_size):
    """Return the bucket to place point in for given dimension."""
    return math.floor(coord/b_size)

def fill_buckets(points, buckets, b_size):
    """Return bucket structure with points filled in appropriate buckets."""
    for point in points:
        x_bucket = get_bucket_index(point[0], b_size)
        y_bucket = get_bucket_index(point[1], b_size)
        buckets[y_bucket][x_bucket].append((point[0], point[1]))
    return buckets

# create adjancency list based on buckets
def get_adjacent_buckets(cx, cy, buckets):
    """Return a list of the points in the buckets adjacent to the given bucket."""
    c_bucket = []
    b_length = len(buckets[0])

    if cx - 1 >= 0:
        c_bucket  += buckets[cy    ][cx - 1]
    if cx - 1 >= 0 and cy - 1 >= 0:
        c_bucket += buckets[cy - 1][cx - 1]
    if cy - 1 >= 0:
        c_bucket += buckets[cy - 1][cx]
    if cx + 1 < b_length and cy - 1 >= 0:
        c_bucket += buckets[cy - 1][cx + 1]
    if cx + 1 < b_length:
        c_bucket  += buckets[cy    ][cx + 1]
    if cx + 1 < b_length and cy + 1 < b_length:
        c_bucket += buckets[cy + 1][cx + 1]
    if cy + 1 < b_length:
        c_bucket  += buckets[cy + 1][cx    ]
    if cx - 1 >= 0 and cy + 1 < b_length:
        c_bucket += buckets[cy + 1][cx - 1]

    return c_bucket + buckets[cy][cx]

def point_close_enough_for_edge(o_point, d_point, r):
    """Return true if the distance between the two points is less than or equal to the radius,
    otherwise return false."""
    d = math.sqrt((d_point[0] - o_point[0])**2 + (d_point[1] - o_point[1])**2)
    return d <= r

def create_adjancency_list(points, buckets, radius, b_length):
    """Return a list of dictionarys that contain the origin point and the connected points from it."""
    adj_list = {}
    num_edges = 0
    max_degree = 0
    min_degree = 1000000
    sum_degrees = 0
    for point in points:
        point_dict = {
            #'origin_point' : point,
            'connected_points': [],
            'degree': 0,
            'color': 0
        }
        x_dex = get_bucket_index(point[0], b_length)
        y_dex = get_bucket_index(point[1], b_length)
        surrounding_points = get_adjacent_buckets(x_dex, y_dex, buckets)
        for potential_point in surrounding_points:
            if point_close_enough_for_edge(point, potential_point, radius) == True and point != potential_point:
                point_dict['connected_points'].append(potential_point)
                num_edges += 1

        degree = len(point_dict['connected_points'])
        point_dict['degree'] = degree
        if degree > max_degree:
            max_degree = degree
        elif degree < min_degree:
            min_degree = degree
        sum_degrees += degree
        adj_list[point] = point_dict
    return adj_list, num_edges/2, min_degree, max_degree, sum_degrees



def get_adjacency_list(n_points, avg_degree, shape):
    """Return adjacency list for given number of vertices, average degree on given shape.
    Also return a dictionary with meta data about the random graph."""

    #create meta data dictionary
    meta = {}

    # get the points
    if shape == 'square':
        points = get_n_points_on_square(n_points)
    elif shape == 'disk':
        points = get_n_points_on_disk(n_points)
    # get the radius of connection and print them
    if shape == 'square':
        radius = get_unit_square_connection_radius(n_points, avg_degree)
    elif shape == 'disk':
        radius = get_unit_circle_connection_radius(n_points, avg_degree)

    meta['r'] = radius
    # get the bucket side length and print it
    b_length = get_bucket_size(radius)
    # get number of buckets in each direction
    buckets = create_buckets_for_points(get_bucket_dimensions(b_length))
    # fill buckets
    buckets = fill_buckets(points, buckets, b_length)
    # return the adjency list
    adj_list, num_edges, min_degree, max_degree, sum_degrees = create_adjancency_list(points, buckets, radius, b_length)
    meta['edges'] = num_edges
    meta['min_degree'] = min_degree
    meta['max_degree'] = max_degree
    meta['real_average_degree'] = sum_degrees / n_points

    return adj_list, meta


if __name__ == "__main__":
    n_points = 64000
    a_degree = 64
    shape = 'square'

    adj_list = get_adjacency_list(n_points, a_degree, shape)

    # get the points
    # points = get_n_points_on_square(n_points, shape)
    # plot_points(points)
