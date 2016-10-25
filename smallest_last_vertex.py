import numpy
import os
import math
from random_graph_construction import get_adjacency_list


def remove_edges_to_all_nodes(point, adj_list):
    """Return adj list moving edges to the given point from connected_points to disconnected_points."""
    for adj in adj_list:
        if point in adj['connected_points']:
            adj['connected_points'].remove(point)
            adj['disconnected_points'].append(point)

    return adj_list

def find_smallest_vertex(adj_list):
    """Return vertex in adjacency list with smallest degree, the adjacency list with the vertex removed
    from all other points' connected_points list and moved to disconnected_points list."""
    smallest_degree = 10000
    smallest_disconnect = 10000
    smallest_vertex = {}
    for node in adj_list:
        if len(node['connected_points']) < smallest_degree:
            smallest_degree = len(node['connected_points'])
            smallest_disconnect = len(node['disconnected_points'])
            smallest_vertex = node
    adj_list.remove(smallest_vertex)
    new_adj_list = remove_edges_to_all_nodes(smallest_vertex['origin_point'], adj_list)
    # print(smallest_degree, smallest_disconnect)
    return (smallest_vertex, new_adj_list)

def get_smallest_vertex_ordering(adj_list):
    smallest_vertex_list = []
    for i in range(len(adj_list)):
        res = find_smallest_vertex(adj_list)
        smallest_vertex_list.append(res[0]) # append the resulting vertex to the list
        adj_list = res[1] # assign the resulting adj list to adj list for repitition
    return smallest_vertex_list


if __name__ == '__main__':

    a_list = get_adjacency_list(10, 3, 'square')
    # for a in a_list:
    #     print(a)

    smallest_ordered_vertices = get_smallest_vertex_ordering(a_list)
    for v in smallest_ordered_vertices:
        print(v)
    # new_list = find_smallest_vertex(a_list)
    # print('thing 2', new_list[0])
    # for l in new_list[1]:
    #     print(l)
