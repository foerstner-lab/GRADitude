from sklearn.decomposition import PCA

import pandas as pd
from bokeh.plotting import figure, output_file, save, ColumnDataSource
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models import WheelZoomTool, TapTool, OpenURL
import numpy as np
import bokeh.palettes


def pca(feature_count_table, feature_count_start_column,
        output_file_colorized_by_clusters, output_file_colorized_by_rna_class):
    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column)
    pca_result = perform_pca(value_matrix)
    plot_t_sne_using_clustering(feature_count_table_df, pca_result,
                                output_file_colorized_by_clusters)
    plot_using_only_rna_colors(feature_count_table_df, pca_result, output_file_colorized_by_rna_class)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):-1]


def perform_pca(normalized_values):
    model = PCA(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    pca_result = model.fit_transform(normalized_values)
    return pca_result


def plot_t_sne_using_clustering(read_counting_table, pca_result, output_file_colorized_by_clusters):
    read_counting_table["t-SNE-component_1"] = [pos[0] for pos in pca_result]
    read_counting_table["t-SNE-component_2"] = [pos[1] for pos in pca_result]

    read_counting_table["Attributes_split"] = \
        read_counting_table["Attributes"].apply(lambda attr: dict(
            [key_value_pair.split("=")
             for key_value_pair in attr.split(";")]))

    color_palette = bokeh.palettes.viridis(
        len(read_counting_table["Cluster_label"].unique()))
    color = read_counting_table["Cluster_label"].apply(
        lambda lable: color_palette[lable])

    hower_data = dict(
        x=read_counting_table["t-SNE-component_1"],
        y=read_counting_table["t-SNE-component_2"],
        feature=read_counting_table["Feature"],
        cluster_label=read_counting_table["Cluster_label"],
        color=color)

    for feature in ["gene", "product", "ID", "type", "ncrna_class",
                    "sRNA_type", "Name", "pseudo"]:
        read_counting_table[feature] = \
            read_counting_table["Attributes_split"].apply(
                lambda attributes: attributes.get(feature, "-"))
        hower_data[feature] = read_counting_table[feature]

    source = ColumnDataSource(hower_data)

    hover = HoverTool(tooltips=[
        ("Gene", "@gene"),
        ("Product", "@product"),
        ("ID", "@ID"),
        ("Type", "@type"),
        ("Ncrna_class", "@ncrna_class"),
        ("sRNA_type", "@sRNA_type"),
        ("Name", "@Name"),
        ("Pseudo", "@pseudo"),
        ("Feature", "@feature"),
        ("Cluster label", "@cluster_label")])

    p = figure(plot_width=700, plot_height=700,
               tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                      WheelZoomTool(), "tap"],
               title="Grad-Seq t-SNE RNA-Seq", logo=None)

    p.circle("x", "y", source=source, size=5, alpha=0.7, color='color')

    url = "http://www.uniprot.org/uniprot/@protein_id"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Component 1"
    p.yaxis.axis_label = "Component 2"

    output_file(output_file_colorized_by_clusters)
    save(p)


def plot_using_only_rna_colors(read_counting_table, pca_result, output_file_colorized_by_rna_class):
    read_counting_table["t-SNE-component_1"] = [pos[0] for pos in pca_result]
    read_counting_table["t-SNE-component_2"] = [pos[1] for pos in pca_result]

    read_counting_table["Attributes_split"] = read_counting_table[
        "Attributes"].apply(
        lambda attr: dict(
            [key_value_pair.split("=") for
             key_value_pair in attr.split(";")]))

    default_color = "#4271FF"
    # highlight_color = "#FF9C38"
    color = default_color
    color = read_counting_table.apply(
        _color, axis=1)

    hower_data = dict(
        x=read_counting_table["t-SNE-component_1"],
        y=read_counting_table["t-SNE-component_2"],
        feature=read_counting_table["Feature"],
        color=color)

    for feature in ["gene", "product", "ID", "type", "ncrna_class",
                    "sRNA_type", "Name", "pseudo"]:
        read_counting_table[feature] = read_counting_table[
            "Attributes_split"].apply(
            lambda attributes: attributes.get(feature, "-"))
        hower_data[feature] = read_counting_table[feature]

    source = ColumnDataSource(hower_data)

    hover = HoverTool(tooltips=[
        ("Gene", "@gene"),
        ("Product", "@product"),
        ("ID", "@ID"),
        ("Type", "@type"),
        ("Ncrna_class", "@ncrna_class"),
        ("sRNA_type", "@sRNA_type"),
        ("Name", "@Name"),
        ("Pseudo", "@pseudo"),
        ("Feature", "@feature")])

    p = figure(plot_width=700, plot_height=700,
               tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                      WheelZoomTool(), "tap"],
               title="Grad-Seq t-SNE RNA-Seq", logo=None)

    p.circle("x", "y", source=source, size=5, alpha=0.7, color='color')

    url = "http://www.uniprot.org/uniprot/@protein_id"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Component 1"
    p.yaxis.axis_label = "Component 2"

    output_file(output_file_colorized_by_rna_class)
    save(p)


def _color(row):
    color = {"CDS": "#BDBDBD", "ncRNA": "#FF4D4D", "tRNA": "#EBB000",
             "rRNA": "#8080FF", "tmRNA": "#3D3D3D"}[row["Feature"]]
    return color
