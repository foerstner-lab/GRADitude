import networkx as nx
import pandas as pd
from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool, ColumnDataSource
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes
from bokeh.palettes import Spectral4


def main():
    correlated_table = pd.read_table('../output/correlated_table.csv')
    correlated_table.set_index('Protein.IDs', inplace=True)
    plot_graph(correlated_table)


def do_plot_graph(nodes, edges, colors, descr):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    plot = Plot(plot_width=400, plot_height=400, x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
    plot.title.text = descr

    plot.add_tools(HoverTool(tooltips=None), TapTool(), BoxSelectTool())

    graph_renderer = from_networkx(G, nx.fruchterman_reingold_layout, scale=1)

    graph_renderer.node_renderer.data_source = ColumnDataSource({'index': nodes, 'fill_color': colors})
    graph_renderer.node_renderer.glyph = Circle(size=15, fill_color="fill_color")

    graph_renderer.node_renderer.selection_glyph = Circle(size=15, fill_color=Spectral4[2])
    graph_renderer.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])

    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = EdgesAndLinkedNodes()

    plot.renderers.append(graph_renderer)

    output_file("interactive_graphs.html")
    show(plot)


def plot_graph(correlated_table):
    descr = "Graph Interaction Demonstration"
    nodes = [*correlated_table.index, *correlated_table.columns]

    edges = []
    for index in correlated_table.index:
        for column in correlated_table.columns:
            weight = correlated_table.loc[index, column]
            if weight >= .4:
                edges.append((index, column))

    colors = [Spectral4[0]] * len(correlated_table.index) + [Spectral4[3]] * len(correlated_table.columns)

    do_plot_graph(nodes, edges, colors, descr)


main()
