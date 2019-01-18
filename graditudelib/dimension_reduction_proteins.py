import pandas as pd
from sklearn.manifold import TSNE
import numpy as np
import umap
from bokeh.plotting import figure, output_file, save, ColumnDataSource
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models import WheelZoomTool, TapTool, OpenURL
from sklearn.decomposition import PCA
import bokeh.palettes


def dr_proteins(feature_count_table, feature_count_start_column,
                feature_count_end_column, dimension_reduction_algorithm,
                perplexity, n_neighbors, min_dist, output_colored_clusters):
    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column, feature_count_end_column)
    if dimension_reduction_algorithm == "t-SNE":
        t_sne_result = perform_t_sne(value_matrix, perplexity)
        plot_t_sne(value_matrix, t_sne_result, output_colored_clusters)
    elif dimension_reduction_algorithm == "PCA":
        pca_result = perform_pca(value_matrix)
        plot_pca(value_matrix, pca_result, output_colored_clusters)
    elif dimension_reduction_algorithm == "UMAP":
        umap_result = perform_umap(value_matrix, n_neighbors, min_dist)
        plot_umap(value_matrix, umap_result, output_colored_clusters)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column, feature_count_end_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):feature_count_end_column]


def perform_t_sne(normalized_values, perplexity):
    model = TSNE(n_components=2, random_state=0, perplexity=perplexity)
    np.set_printoptions(suppress=True)
    tsne_result = model.fit_transform(normalized_values)
    return tsne_result


def perform_pca(normalized_values):
    model = PCA(n_components=3, random_state=0)
    np.set_printoptions(suppress=True)
    pca_result = model.fit_transform(normalized_values)
    return pca_result


def perform_umap(normalized_values, n_neighbors, min_dist):
    reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist)
    umap_results = reducer.fit_transform(normalized_values)
    return umap_results


def plot_t_sne(read_counting_table, tsne_result, output_file_colorized_by_clusters):
    read_counting_table["t-SNE-component_1"] = [pos[0] for pos in tsne_result]
    read_counting_table["t-SNE-component_2"] = [pos[1] for pos in tsne_result]

    color_palette = bokeh.palettes.viridis(
        len(read_counting_table["Cluster_label"].unique()))
    color = read_counting_table["Cluster_label"].apply(
        lambda lable: color_palette[lable])

    hower_data = dict(
        x=read_counting_table["t-SNE-component_1"],
        y=read_counting_table["t-SNE-component_2"],
        feature=read_counting_table["Protein.names"],
        id=read_counting_table["Protein.IDs"],
        cluster_label=read_counting_table["Cluster_label"],
        color=color)

    source = ColumnDataSource(hower_data)

    hover = HoverTool(tooltips=[
        ("Protein.names", "@feature"),
        ("Protein.IDs", "@id")])

    p = figure(plot_width=700, plot_height=700,
               tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                      WheelZoomTool(), "tap"],
               title="Grad-Seq t-SNE RNA-Seq", logo=None)

    p.circle("x", "y", source=source, size=5, alpha=0.7, color='color')

    url = "http://www.uniprot.org/uniprot/@id"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Dimension 1"
    p.yaxis.axis_label = "Dimension 2"

    output_file(output_file_colorized_by_clusters)
    save(p)


def plot_pca(read_counting_table, pca_result, output_file_colorized_by_clusters):
    read_counting_table["PCA-component_1"] = [pos[0] for pos in pca_result]
    read_counting_table["PCA-component_2"] = [pos[1] for pos in pca_result]

    color_palette = bokeh.palettes.viridis(
        len(read_counting_table["Cluster_label"].unique()))
    color = read_counting_table["Cluster_label"].apply(
        lambda lable: color_palette[lable])

    hower_data = dict(
        x=read_counting_table["PCA-component_1"],
        y=read_counting_table["PCA-component_2"],
        feature=read_counting_table["Protein.names"],
        id=read_counting_table["Protein.IDs"],
        cluster_label=read_counting_table["Cluster_label"],
        color=color)

    source = ColumnDataSource(hower_data)

    hover = HoverTool(tooltips=[
        ("Protein.names", "@feature"),
        ("Protein.IDs", "@id")])

    p = figure(plot_width=700, plot_height=700,
               tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                      WheelZoomTool(), "tap"],
               title="Grad-Seq PCA RNA-Seq", logo=None)

    p.circle("x", "y", source=source, size=5, alpha=0.7, color='color')

    url = "http://www.uniprot.org/uniprot/@id"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Component 1"
    p.yaxis.axis_label = "Component 2"

    output_file(output_file_colorized_by_clusters)
    save(p)


def plot_umap(read_counting_table, umap_result, output_file_colorized_by_clusters):
    read_counting_table["UMAP-component_1"] = [pos[0] for pos in umap_result]
    read_counting_table["UMAP-component_2"] = [pos[1] for pos in umap_result]

    color_palette = bokeh.palettes.viridis(
        len(read_counting_table["Cluster_label"].unique()))
    color = read_counting_table["Cluster_label"].apply(
        lambda lable: color_palette[lable])

    hower_data = dict(
        x=read_counting_table["UMAP-component_1"],
        y=read_counting_table["UMAP-component_2"],
        feature=read_counting_table["Protein.names"],
        id=read_counting_table["Protein.IDs"],
        cluster_label=read_counting_table["Cluster_label"],
        color=color)

    source = ColumnDataSource(hower_data)

    hover = HoverTool(tooltips=[
        ("Protein.names", "@feature"),
        ("Protein.IDs", "@id")])

    p = figure(plot_width=700, plot_height=700,
               tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                      WheelZoomTool(), "tap"],
               title="Grad-Seq t-SNE UMAP-Seq", logo=None)

    p.circle("x", "y", source=source, size=5, alpha=0.7, color='color')

    url = "http://www.uniprot.org/uniprot/@id"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Dimension 1"
    p.yaxis.axis_label = "Dimension 2"

    output_file(output_file_colorized_by_clusters)
    save(p)
