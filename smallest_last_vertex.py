import numpy
import os
import math
from random_graph_construction import get_adjacency_list

def generate_buckets_of_vertices(adj_list):
    """Return a dictionary with buckets of vertices placed based on their degree."""
    buckets = {}
    max_degree = 0
    for vertex, dict in adj_list.items():
        vertex_degree = len(dict['connected_points'])
        if vertex_degree > max_degree:
            max_degree = vertex_degree
        if vertex_degree in buckets:
            buckets[vertex_degree].append(vertex)
        else:
            buckets[vertex_degree] = [vertex]
    return (buckets, max_degree)

def find_lowest_degree_vertex(vertex_buckets, max_bucket):
    for i in range(max_bucket):
        if i in vertex_buckets and len(vertex_buckets[i]):
            popped_vertex = vertex_buckets[i].pop(0)
            return (popped_vertex, vertex_buckets)

def get_neighbors_and_degrees(vertex, adj_list, aux_dict):
    """Return a list of neighbors for a given vertex with their degree once the vertex is gone (degree - 1)."""
    vertex_data = adj_list[vertex]
    neighbors = {}
    for neighbor in vertex_data['connected_points']:
        if neighbor in aux_dict:
            neighbors[neighbor] = aux_dict[neighbor] - 1
        else:
            neighbors[neighbor] = adj_list[neighbor]['degree'] - 1
        aux_dict[neighbor] = neighbors[neighbor] #update aux_dict
    return (neighbors, aux_dict)

def shift_neighbors_down_bucket(buckets, neighbors):
    """Return buckets with members of neighbors shifted down by one."""
    for neighbor, bucket in neighbors.items():
        if neighbor in buckets[bucket + 1]:
            buckets[bucket + 1].remove(neighbor)
        if bucket in buckets:
            buckets[bucket].append(neighbor)
        else:
            buckets[bucket] = [neighbor]
    return buckets

def get_smallest_vertex_ordering(adj_list):
    """Return a list of vertices in ascending order of their degrees."""
    vertex_buckets, max_bucket = generate_buckets_of_vertices(adj_list)
    vertices_in_order_of_degree = []
    aux_vertex_degrees = {}
    for i in range(len(adj_list)):
        #get the vertex with the minimum degree
        min_vert, vertex_buckets = find_lowest_degree_vertex(vertex_buckets, max_bucket)
        #print (min_vert, vertex_buckets)
        vertices_in_order_of_degree.append(min_vert)
        #get all neighbors (and their degrees) of min vertex
        neighbors, aux_vertex_degrees = get_neighbors_and_degrees(min_vert, adj_list, aux_vertex_degrees)

        #bump all neighbors down by a degree in buckets
        vertex_buckets = shift_neighbors_down_bucket(vertex_buckets, neighbors)
        # print(min_vert)
        # print(neighbors)
        # print(vertex_buckets)
        # print()
    return vertices_in_order_of_degree


#HAVEN'T IMPLEMENTED YET

def color_vertices(smallest_first_vertices):
    """Return the list of vertices with colors associated with them."""
    colors = [1]
    for v in smallest_first_vertices:
        pass



if __name__ == '__main__':

    a_list = get_adjacency_list(10, 3, 'square')
    print(a_list)
    smallest_ordered_vertices = get_smallest_vertex_ordering(a_list)
    print(smallest_ordered_vertices)
