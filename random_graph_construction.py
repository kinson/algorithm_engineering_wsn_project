import numpy
import os
from operator import itemgetter

def get_n_points_on_square(n):
    """Return n uniformly distributed points within a square as a list of tuples."""
    points = numpy.random.uniform(0, 1, (n, 2))
    return [(p[0], p[1]) for p in points]

def sort_points(points):
    """Return ndarray of points sorted."""
    return sorted(points, key=itemgetter(0, 1))

if __name__ == "__main__":
  points = get_n_points_on_square(5)
  print(points)
  points = sort_points(points)
  print(points)
