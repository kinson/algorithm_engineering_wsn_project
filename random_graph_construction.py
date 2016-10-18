import numpy
import os
from operator import itemgetter
import matplotlib.pyplot as plt

def get_n_points_on_square(n):
    """Return n uniformly distributed points within a square as a list of lists."""
    return numpy.random.uniform(0, 1, (n, 2))

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

def transform_lists_to_tuples(t):
    """Return list of tuples from list of lists."""
    return [(p[0], p[1]) for p in points]

def sort_points(points):
    """Return ndarray of points sorted."""
    return sorted(points, key=itemgetter(0, 1))

if __name__ == "__main__":
  points = get_n_points_on_square(16000)
  plot_points(points)
