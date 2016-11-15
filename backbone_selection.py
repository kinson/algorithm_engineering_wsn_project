import math
import operator
from random_graph_construction import get_adjacency_list
from smallest_last_vertex import get_smallest_vertex_ordering
from smallest_last_vertex import color_vertices


def get_colors_with_counts(a_list):
    colors = {}
    for key, a in a_list.items():
        color = a['color']
        if color in colors:
            colors[color] += 1
        else:
            colors[color] = 1
    return colors

def get_four_largest_color_classes(color_counts):
    return sorted(color_counts.keys(), key=(lambda k: color_counts[k]), reverse=True)[0:4]

if __name__ == "__main__":
    a_list = get_adjacency_list(32000, 64, 'square')
    print("part one done")
    smallest_ordered_vertices = get_smallest_vertex_ordering(a_list)
    print("part two done")
    a_list_colored, num_colors = color_vertices(smallest_ordered_vertices, a_list)
    print("part three done")
    color_counts = get_colors_with_counts(a_list)
    largest_colors = get_four_largest_color_classes(color_counts)
    for c in largest_colors:
        print(c, color_counts[c])
