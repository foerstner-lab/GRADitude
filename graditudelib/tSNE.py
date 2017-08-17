#!/usr/bin/env python
import pandas as pd
from sklearn.manifold import TSNE
import numpy as np
from bokeh.plotting import figure, save, ColumnDataSource
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models import WheelZoomTool, TapTool, OpenURL
import bokeh.palettes


def t_sne_analysis(feature_count_table, feature_count_start_column,
                   pseudo_count, scaling_method, output_format):
    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column)
    normalized_values = normalize_values(
        value_matrix, scaling_method, pseudo_count)
    t_sne_results = perform_t_sne(normalized_values)
    plot(feature_count_table_df, t_sne_results)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):]


def normalize_values(values_matrix, scaling_method, pseudo_count):
    if scaling_method == "no_normalization":
        normalized_values = values_matrix
    elif scaling_method == "log2":
        normalized_values = values_matrix.applymap(
            lambda val: val + pseudo_count).applymap(np.log2)
    elif scaling_method == "log10":
        normalized_values = values_matrix.applymap(
            lambda val: val + pseudo_count).applymap(np.log10)
    elif scaling_method == "normalized_to_max":
        row_max_values = values_matrix.max(axis=1)
        normalized_values = values_matrix.divide(
            row_max_values, axis=0)
    elif scaling_method == "normalized_to_range":
        row_max_values = values_matrix.max(axis=1)
        row_min_values = values_matrix.min(axis=1)
        normalized_values = values_matrix.subtract(
            row_min_values, axis=0).divide(row_max_values, axis=0)
    else:
        print("Normalization method not known")
    return normalized_values


def perform_t_sne(normalized_values):
    model = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    tsne_result = model.fit_transform(normalized_values)
    return tsne_result

    
def plot(read_counting_table, tsne_result):
    read_counting_table["t-SNE-component_1"] = [pos[0] for pos in tsne_result]
    read_counting_table["t-SNE-component_2"] = [pos[1] for pos in tsne_result]

    read_counting_table["Attributes_split"] = \
        read_counting_table["Attributes"].apply(lambda attr: dict(
            [key_value_pair.split("=")
             for key_value_pair in attr.split(";")]))

    hower_data = dict(
        x=read_counting_table["t-SNE-component_1"],
        y=read_counting_table["t-SNE-component_2"],
        feature=read_counting_table["Feature"],
        cluster_label=read_counting_table["Cluster_label"])

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

    default_color = "#4271FF"
    # highlight_color = "#FF9C38"
    color = default_color

    # color = read_counting_table.apply(
    #     _color, args=(srnas_and_list_names,), axis=1)

    color_palette = bokeh.palettes.viridis(
        len(read_counting_table["Cluster_label"].unique()))
    color = read_counting_table["Cluster_label"].apply(
        lambda lable: color_palette[lable])

    p.circle("x", "y", source=source, size=5, alpha=0.7, color=color)

    url = "http://www.uniprot.org/uniprot/@protein_id"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Component 1"
    p.yaxis.axis_label = "Component 2"

    save(p)


def _color(row, srnas_and_list_names):
    color = {"CDS": "#BDBDBD", "ncRNA": "#FF4D4D", "tRNA": "#EBB000",
             "rRNA": "#8080FF", "tmRNA": "#3D3D3D"}[row["Feature"]]
    sRNA_cluster_color = {"sRNA_cluster_1": "#33CCFF",
                          "sRNA_cluster_2": "#000000",
                          "sRNA_cluster_3": "#D600D6"}
    for feature in ["ID", "Name", "gene"]:
        if row[feature] in srnas_and_list_names:
            color = sRNA_cluster_color[
                srnas_and_list_names[row[feature]]]
    return color
