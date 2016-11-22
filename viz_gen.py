import plotly.plotly as py
import plotly.graph_objs as go

from random_graph_construction import get_adjacency_list

c_mark = {}

benchmarks = [
    # { 'n': 1000,  'd': 32,  'shape': 'square' },
    # { 'n': 4000,  'd': 64,  'shape': 'square' },
    # { 'n': 16000, 'd': 64,  'shape': 'square' },
    # { 'n': 64000, 'd': 64,  'shape': 'square' },
    # { 'n': 64000, 'd': 128, 'shape': 'square' },
    { 'n': 4000,  'd': 64,  'shape': 'disk' },
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
      degree_dist_url = generate_degree_dist(a_list)
      print(degree_dist_url)

      #RCG display (scatter plot), include min/max vertex if possible (note: only for n <= 16000)
      vertex_scatter = generate_vertices_plot(a_list)
      print(vertex_scatter)
      #sequential coloring graph (degree of node when deleted, original degree)

      #color class size graph distribution

      #table of info relating to graph

      #backbone info (largest backbone)
