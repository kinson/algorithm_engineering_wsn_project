from smallest_last_vertex import get_smallest_vertex_ordering
from smallest_last_vertex import color_vertices
from backbone_selection import get_colors_with_counts
from backbone_selection import get_four_largest_color_classes
from backbone_selection import vertices_for_color
from backbone_selection import find_largest_backbone


adj_list = {
  1: {'connected_points': [2, 10], 'degree': 2, 'color': 0},
  2: {'connected_points': [1, 7, 8], 'degree': 3, 'color': 0},
  3: {'connected_points': [4, 7], 'degree': 2, 'color': 0},
  4: {'connected_points': [3, 6], 'degree': 2, 'color': 0},
  5: {'connected_points': [6], 'degree': 1, 'color': 0},
  6: {'connected_points': [4, 5, 8], 'degree': 3, 'color': 0},
  7: {'connected_points': [2, 3, 8], 'degree': 3, 'color': 0},
  8: {'connected_points': [2, 6, 7, 9, 10], 'degree': 5, 'color': 0},
  9: {'connected_points': [8, 10], 'degree': 2, 'color': 0},
  10: {'connected_points': [1, 8, 9], 'degree': 3, 'color': 0}
}


if __name__ == "__main__":
  print("beginning test harness for backbone construction")
  print(adj_list)
  smallest_ordered_vertices = get_smallest_vertex_ordering(adj_list)
  print(smallest_ordered_vertices)
  adj_list_colored, num_colors = color_vertices(smallest_ordered_vertices, adj_list)
  color_counts = get_colors_with_counts(adj_list)
  largest_colors = get_four_largest_color_classes(color_counts)
  for c in largest_colors:
      print(c, color_counts[c])

  #get curried function for finding vertices
  curried_vertices_for_colors = vertices_for_color(adj_list)
  largest_backbone = find_largest_backbone(largest_colors, curried_vertices_for_colors)
  print(largest_backbone)
