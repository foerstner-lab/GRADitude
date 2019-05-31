import numpy as np
import networkx as nx
import pandas as pd
from bokeh.io import show, output_file
from bokeh.models import Range1d, MultiLine, Circle, HoverTool, TapTool, ColumnDataSource, \
    BoxZoomTool, ResetTool, PanTool, WheelZoomTool, OpenURL
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges
from bokeh.palettes import Spectral4
from bokeh.plotting import figure


def plot_network_graph_rna_protein(feature_count_table, index_table, threshold, max_size, output_plot):
    correlated_table = pd.read_csv(feature_count_table, sep='\t')
    correlated_table.set_index(index_table, inplace=True)
    plot_graph(correlated_table, threshold, max_size, output_plot)


def do_plot_graph(nodes, edges, colors, sizes, description, output_plot):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    hover = HoverTool(tooltips=[
        ("name", "@index")])

    plot = figure(plot_width=900, plot_height=900, x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1),
                  tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                         WheelZoomTool(), "tap"],
                  title=output_plot)
    plot.toolbar.logo = None

    plot.title.text = description

    url_protein = "https://www.ncbi.nlm.nih.gov/gene/?term=@index"
    taptool = plot.select(type=TapTool)
    taptool.callback = OpenURL(url=url_protein)

    graph_renderer = from_networkx(G, nx.fruchterman_reingold_layout, scale=1)

    source = ColumnDataSource({'index': nodes, 'fill_color': colors, 'size': sizes})
    graph_renderer.node_renderer.data_source = source
    graph_renderer.node_renderer.glyph = Circle(size="size", fill_color="fill_color", line_width=0,
                                                line_color="fill_color")

    graph_renderer.node_renderer.selection_glyph = Circle(size="size", fill_color=Spectral4[2], line_width=0,
                                                          line_color=Spectral4[1])
    graph_renderer.node_renderer.hover_glyph = Circle(size="size", fill_color=Spectral4[1], line_width=0,
                                                      line_color=Spectral4[1])

    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=1, line_width=0.2)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=1)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=1)

    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = NodesAndLinkedEdges()

    plot.renderers.append(graph_renderer)

    output_file(output_plot)


def plot_graph(correlated_table, threshold, max_size, output_plot):
    description = "Network graph rna-protein"
    nodes = [*correlated_table.index, *correlated_table.columns]

    edges = []
    for index in correlated_table.index:
        for column in correlated_table.columns:
            weight = correlated_table.loc[index, column]
            if weight >= threshold:
                edges.append((index, column))

    colors = [Spectral4[0]] * len(correlated_table.index) + [Spectral4[3]] * len(correlated_table.columns)

    sizes = []

    for index in correlated_table.index:
        s = correlated_table.loc[index]
        size = np.sqrt(s[s >= threshold].sum())
        sizes.append(size)

    for column in correlated_table.columns:
        s = correlated_table.loc[:, column]
        size = np.sqrt(s[s >= threshold].sum())
        sizes.append(size)

    scaled_sizes = [float(i) / max(sizes) * max_size for i in sizes]

    do_plot_graph(nodes, edges, colors, scaled_sizes, description, output_plot)
