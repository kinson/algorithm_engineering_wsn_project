import plotly.plotly as py
import plotly.graph_objs as go

from random_graph_construction import get_adjacency_list
from smallest_last_vertex import get_smallest_vertex_ordering
from smallest_last_vertex import color_vertices
from backbone_selection import select_backbone

c_mark = {}

benchmarks = [
    # { 'n': 1000,  'd': 32,  'shape': 'square' },
    # { 'n': 4000,  'd': 64,  'shape': 'square' },
    { 'n': 16000, 'd': 64,  'shape': 'square' },
    # { 'n': 64000, 'd': 64,  'shape': 'square' },
    # { 'n': 64000, 'd': 128, 'shape': 'square' },
    # { 'n': 4000,  'd': 64,  'shape': 'disk' },
    # { 'n': 4000,  'd': 128, 'shape': 'disk' },
]

def populate_c_mark(shape, n, d):
    c_mark.clear()
    c_mark['shape'] = shape
    c_mark['n'] = n
    c_mark['d'] = d
    c_mark['tag'] = shape + '-' + str(n) + 'n-' + str(d) + 'd'

def generate_degree_dist(a_list):
    degrees = {}
    for k, a in a_list.items():
        d = a['degree']
        if d in degrees:
            degrees[d] += 1
        else:
            degrees[d] = 1

    c_mark['degree_dist'] = degrees

    data = [go.Bar(
            x=list(degrees.keys()),
            y=list(degrees.values())
    )]

    layout = go.Layout(
      title="Distribution of Node Degrees",
      xaxis=dict(title='Degree'),
      yaxis=dict(title='Number of Nodes')
    )
    fig = go.Figure(data = data, layout = layout)
    return py.plot(fig, filename='degree-dist-bar-'+c_mark['tag'])

def generate_vertices_plot(a_list):
    points = list(a_list.keys())
    x_points = list(map(lambda x: x[0], points))
    y_points = list(map(lambda x: x[1], points))

    trace = go.Scatter(
      x = x_points,
      y = y_points,
      mode = 'markers'
    )

    data = [trace]

    layout = go.Layout(
      title="Vertex Positioing",
    )

    fig = go.Figure(data = data, layout = layout)
    return py.plot(fig, filename='vertex-scatter-'+c_mark['tag'])

def generate_sequential_coloring_plot(smallest_vertex_ordering, deleted_degrees, a_list):
    o_degrees = []
    graph_x_axis = list(range(1, len(deleted_degrees) + 1))
    for i in range(len(smallest_vertex_ordering)):
        point = smallest_vertex_ordering[i]
        point_info = a_list[point]
        o_degrees.append(point_info['degree'])

    trace1 = go.Scatter(
      x = graph_x_axis,
      y = o_degrees,
      name= "Original Degree"
    )

    trace2 = go.Scatter(
      x = graph_x_axis,
      y = deleted_degrees,
      name = "Degree When Deleted"
    )

    data = [trace1, trace2]

    layout = go.Layout(
      title="Sequential Coloring Plot",
      xaxis=dict(
        title='Smallest Last Vertex Ordering',
        ),
      yaxis=dict(
        title='Vertex Degree'
      )
    )

    fig = go.Figure(data = data, layout = layout)
    return py.plot(fig, filename='sequential-scatter-'+c_mark['tag'])

def generate_color_class_size_plot(a_list, max_color):
    color_sizes = [0] * max_color
    x_axis = list(range(1, max_color + 1))

    for key, point in a_list.items():
        c = point['color']
        color_sizes[c - 1] += 1

    trace = go.Bar(
      x = x_axis,
      y = color_sizes
    )

    data = [trace]

    layout = go.Layout(
      title="Color Class Size Bar Chart",
      xaxis=dict(
        title='Color Class'
      ),
      yaxis=dict(
        title='Number of Vertices'
      )
    )

    fig = go.Figure(data = data, layout = layout)
    return py.plot(fig, filename='color-size-bar-'+c_mark['tag'])


def get_edges_for_bipartite(a_list, component):
    edges = []
    for c in component:
        point_in_a_list = a_list[c]
        for neighbor in point_in_a_list['connected_points']:
            if neighbor in component:
                edges.append((c, neighbor))

    return edges

def generate_backbone_network(nodes, edges, color_a):
    edge_trace = go.Scatter(
      x=[],
      y=[],
      line=go.Line(width=0.5,color='#888'),
      hoverinfo='none',
      mode='lines'
    )

    for edge in edges:
        p1, p2 = edge[0], edge[1]
        edge_trace['x'] += [p1[0], p2[0], None]
        edge_trace['y'] += [p1[1], p2[1], None]

    node_trace = go.Scatter(
      x=[],
      y=[],
      text=[],
      mode='markers',
      hoverinfo='text',
      marker=go.Marker(
        showscale=True,
        colorscale='YIGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
          thickness=15,
          title='Node Connections',
          xanchor='left',
          titleside='right'
        ),
        line=dict(width=2)
      ),
    )


    for node in nodes:
        node_trace['x'].append(node[0])
        node_trace['y'].append(node[1])
        color = '#FAA43A' if a_list[node]['color'] == color_a else '5DA5DA'
        node_trace['marker']['color'].append(color)

    fig = go.Figure(data=go.Data([edge_trace, node_trace]),
      layout=go.Layout(
        title='<br>Backbone Network',
        titlefont=dict(size=16),
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        xaxis=go.XAxis(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=go.YAxis(showgrid=False, zeroline=False, showticklabels=False)
      )
    )

    return py.plot(fig, filename='backbone-network-'+c_mark['tag'])


if __name__ == "__main__":
  print("starting part one generation")

  for mark in benchmarks:
      num_nodes    = mark['n']
      avg_degree   = mark['d']
      distribution = mark['shape']

      #get an a_list to work with
      a_list = get_adjacency_list(num_nodes, avg_degree, distribution)
      populate_c_mark(distribution, num_nodes, avg_degree)

      #for each benchmark, generate the following graphics
      #degree distribution (as bar graph)
      ##degree_dist_url = generate_degree_dist(a_list)
      ##print(degree_dist_url)

      #RCG display (scatter plot), include min/max vertex if possible (note: only for n <= 16000)
      ##vertex_scatter = generate_vertices_plot(a_list)
      ##print(vertex_scatter)

      #do smallest last vertex ordering
      smallest_last_ordering, deleted_degrees = get_smallest_vertex_ordering(a_list)
      print("finished smallest last vertex")

      #sequential coloring graph (degree of node when deleted, original degree)
      ##sequential_scatter = generate_sequential_coloring_plot(smallest_last_ordering, deleted_degrees, a_list)

      #get color clases
      a_list, num_colors = color_vertices(smallest_last_ordering, a_list)
      print("finished coloring vertices")

      #color class size graph distribution
      ##color_class_bar = generate_color_class_size_plot(a_list, num_colors)

      #table of info relating to graph


      #backbone info (largest backbone)
      largest_backbone_size, largest_backbone = select_backbone(a_list, smallest_last_ordering)
      print(largest_backbone_size)
      edges_for_bipartite = get_edges_for_bipartite(a_list, largest_backbone)

      color_a = a_list[largest_backbone[0]]['color']
      backbone_network = generate_backbone_network(largest_backbone, edges_for_bipartite, color_a)
