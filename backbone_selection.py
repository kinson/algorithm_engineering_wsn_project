import math
import operator
import itertools
from random_graph_construction import get_adjacency_list
from smallest_last_vertex import get_smallest_vertex_ordering
from smallest_last_vertex import color_vertices


def get_colors_with_counts(a_list):
    """Return a dictionary with the colors as keys and their frequencies as the values."""
    colors = {}
    for key, a in a_list.items():
        color = a['color']
        if color in colors:
            colors[color] += 1
        else:
            colors[color] = 1
    return colors

def get_four_largest_color_classes(color_counts):
    """Return the four largest color classes from dictionary of color => frequency."""
    return sorted(color_counts.keys(), key=(lambda k: color_counts[k]), reverse=True)[0:4]

def vertices_for_color(a_list):
    """Return a function that returns a dictionary filtered by color for a given adjacency list."""
    def fn(color_a, color_b):
        return {k: v for k, v in a_list.items() if v['color'] == color_a or v['color'] == color_b}
    return fn

def list_of_adjacent_vertices(neighbors, bipartite_points):
    """Return list of verticies that are in the biparatite graph made from colors."""
    return [p for p in neighbors if p in bipartite_points]

def get_largest_component(color_a, color_b, v_by_colors):
    """Given two adjacency lists of verticies in different color classes, return the largest
    component of the bipartite graph."""
    colors_combined = v_by_colors(color_a, color_b)
    all_points = list(colors_combined.keys())
    stack = []
    current_component = 0
    component_sizes = {}
    while len(all_points):
        if not len(stack):
            #print("putting node on EMPTY stack")
            next_node = all_points[-1]
            current_component += 1
            component_sizes[current_component] = 0
            stack.append(next_node)
        else:
            #print("in component", current_component, " with size", component_sizes[current_component])
            top_stack = stack[-1]
            neighbors = colors_combined[top_stack]['connected_points']
            bipartite_neighbors = list_of_adjacent_vertices(neighbors, all_points)
            if len(bipartite_neighbors):
                #print("\tfound" , len(bipartite_neighbors) , "neighbors to add to stack", top_stack)
                stack.extend(bipartite_neighbors)
            else:
                #print("\tfound no neighbors (leaf node)", top_stack)
                #add one to component size
                component_sizes[current_component] += 1
                #pop node off stack
                stack.pop()
            if top_stack in all_points:
                all_points.remove(top_stack)

    component_sizes = sorted(component_sizes.items(), key=(lambda k: k[1]), reverse=True)[0]

    return component_sizes

def find_largest_backbone(colors, curried_vertices_for_colors):
    """Given the four largest color classes, find the largest bipartite component generated
    by combining any two of the color classes. Return the colors."""
    max = -1
    for subset in itertools.combinations(colors, 2):
        a, b = subset[0] - 1, subset[1] - 1
        largest_component = get_largest_component(colors[a], colors[b], curried_vertices_for_colors)
        print(largest_component)
        if largest_component[1] > max:
            max = largest_component[1]
    return max

if __name__ == "__main__":
    a_list = get_adjacency_list(64000, 64, 'square')
    print("part one done")
    smallest_ordered_vertices = get_smallest_vertex_ordering(a_list)
    print("part two done")
    a_list_colored, num_colors = color_vertices(smallest_ordered_vertices, a_list)
    print("part three done")
    color_counts = get_colors_with_counts(a_list)
    largest_colors = get_four_largest_color_classes(color_counts)
    for c in largest_colors:
        print(c, color_counts[c])

    #get curried function for finding vertices
    curried_vertices_for_colors = vertices_for_color(a_list)
    largest_backbone = find_largest_backbone(largest_colors, curried_vertices_for_colors)
    print(largest_backbone)
