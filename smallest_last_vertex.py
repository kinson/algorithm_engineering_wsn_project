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
    """Return the next lowest degree vertex from the vertex buckets along with the buckets without the removed vertex."""
    for i in range(max_bucket + 1):
        if i in vertex_buckets and len(vertex_buckets[i]):
            popped_vertex = vertex_buckets[i].pop(0)
            return (popped_vertex, vertex_buckets)

def get_neighbors_and_bump_degrees(vertex_data, aux_dict, buckets):
    """Iterate over the neighbors to the vertex being removed. Bump their degrees down if they are greater than 0.
    Shift the neighbors down in the vertices bucket if they exist, otherwise they have already been removed, so continue
    to next neighbor. Return the buckets and auxillary degree dictionary back."""
    new_bucket = -1
    for neighbor in vertex_data['connected_points']:
        new_bucket = aux_dict[neighbor] - 1 if aux_dict[neighbor] > 0 else 0
        aux_dict[neighbor] = new_bucket

        if new_bucket + 1 in neighbor and neighbor in buckets[new_bucket + 1]:
            buckets[new_bucket + 1].remove(neighbor)
        else:
            continue

        if new_bucket in buckets:
            buckets[new_bucket].append(neighbor)
        else:
            buckets[new_bucket] = [neighbor]

    return (buckets, aux_dict)

def populate_aux_dict(adj_list):
    """Return an auxillary dictionary to keep track of the degree of each vertex."""
    aux_dict = {}
    for a, b in adj_list.items():
        d = b['degree']
        aux_dict[a] = d
    return aux_dict

def get_smallest_vertex_ordering(adj_list):
    """Return a list of vertices in ascending order of their degrees."""
    vertex_buckets, max_bucket = generate_buckets_of_vertices(adj_list)
    vertices_in_order_of_degree = []
    aux_vertex_degrees = populate_aux_dict(adj_list)
    total_len = len(adj_list)
    for i in range(len(adj_list)):
        #get the vertex with the minimum degree
        min_vert, vertex_buckets = find_lowest_degree_vertex(vertex_buckets, max_bucket)
        #print (min_vert, vertex_buckets)
        vertices_in_order_of_degree.append(min_vert)
        #get all neighbors (and their degrees) of min vertex
        vertex_data = adj_list[min_vert]
        vertex_buckets, aux_vertex_degrees = get_neighbors_and_bump_degrees(vertex_data, aux_vertex_degrees, vertex_buckets)
    return vertices_in_order_of_degree


def get_used_neighbor_colors(v, adj_list):
    """Given a vertex in the adjency list, return the colors already used by its neighbors."""
    colors_used = []
    neighbors = adj_list[v]['connected_points']
    for neighbor in neighbors:
        n_color = adj_list[neighbor]['color']
        if n_color != 0 and n_color not in colors_used:
            colors_used.append(n_color)
    return colors_used

#HAVEN'T IMPLEMENTED YET
def color_vertices(smallest_first_vertices, adj_list):
    """Return the adjacency list of vertices with colors associated with them along with the number of colors used."""
    colors = [1]
    for v in smallest_first_vertices:
        colors_used = get_used_neighbor_colors(v, adj_list)
        colors_left = [c for c in colors if c not in colors_used]
        if len(colors_left):
            adj_list[v]['color'] = colors_left[0]
        else:
            new_color = colors[-1] + 1
            colors.append(new_color)
            adj_list[v]['color'] = new_color
    return adj_list, colors[-1]




if __name__ == '__main__':
    a_list = get_adjacency_list(64000, 64, 'square')
    print("part one done")
    smallest_ordered_vertices = get_smallest_vertex_ordering(a_list)
    print("part two done")
    a_list_colored, num_colors = color_vertices(smallest_ordered_vertices, a_list)
    print("part three done")

    print(num_colors)
