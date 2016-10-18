import numpy
import os
import math
from operator import itemgetter
import matplotlib.pyplot as plt

# get n distributed points in square
def get_n_points_on_square(n):
    """Return n uniformly distributed points within a square as a list of lists."""
    return numpy.random.uniform(0, 1, (n, 2))

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
    plt.axis([0, 1, 0, 1])
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

def get_bucket_size(connection_radius):
    """Return the side lengths of the squares that will be used as buckets for
    determining point connections. Get the side length for a square inscribed in
    a circle of a given radius.


    Formula for calculating side length: L = sqrt( (2*r)^2 / 2 )
    """
    return math.sqrt( (2*connection_radius)**2 / 2 )

#determine bucket dimensions from side length and instantiate buckets
def get_bucket_dimensions(side_length):
    """Return number of buckets in the x and y dimensions to put points into using the
    bucket size. Use the floor of this number to determine the number of buckets."""
    return math.floor(1/side_length)

def create_buckets_for_points(num_buckets):
    """Return list of lists of lists to put points into (as buckets)."""
    br = range(num_buckets)
    return [ [ [] for i in br ] for j in br]


if __name__ == "__main__":
    n_points = 1000
    a_degree = 32
    shape = 'square'

    # get the points
    points = get_n_points_on_square(n_points)
    #plot the points
    #plot_points(points)
    #get the radius of connection and print them
    radius = get_unit_square_connection_radius(n_points, a_degree)
    print("average radius: ", radius)
    #get the bucket side length and print it
    b_length = get_bucket_size(radius)
    print("side lengths for buckets: ", b_length)
    #get number of buckets in each direction
    buckets = create_buckets_for_points(get_bucket_dimensions(b_length))
