import pandas as pd
from sklearn.manifold import TSNE
import numpy as np
from bokeh.plotting import figure, output_file, save, ColumnDataSource
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models import WheelZoomTool, TapTool, OpenURL
import bokeh.palettes


def t_sne(feature_count_table, feature_count_start_column,
          perplexity, s_rna_list_files, output_file_colorized_by_clusters, output_file_colorized_by_rna_class,
          output_file_colorized_by_rna_class_and_list):
    feature_count_table_df = pd.read_table(feature_count_table)
    s_rnas_and_list_names = read_srna_lists(s_rna_list_files)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column)
    t_sne_results = perform_t_sne(value_matrix, perplexity)
    plot_t_sne_using_rna_classes_and_jens_list(feature_count_table_df, t_sne_results,
                                               output_file_colorized_by_rna_class_and_list, s_rnas_and_list_names)
    plot_t_sne_using_clustering(feature_count_table_df, t_sne_results,
                                output_file_colorized_by_clusters)
    plot_using_only_rna_colors(feature_count_table_df, t_sne_results, output_file_colorized_by_rna_class)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):-1]


def perform_t_sne(normalized_values, perplexity):
    model = TSNE(n_components=2, random_state=0, perplexity=perplexity)
    np.set_printoptions(suppress=True)
    tsne_result = model.fit_transform(normalized_values)
    return tsne_result


def read_srna_lists(srna_list_files):
    srnas_and_list_names = {}
    for index, srna_list_file in enumerate(srna_list_files):
        list_name = "sRNA_cluster_{}".format(index + 1)
        for line in open(srna_list_file):
            srnas_and_list_names[line.strip()] = list_name
    return srnas_and_list_names


def plot_t_sne_using_rna_classes_and_jens_list(read_counting_table, tsne_result,
                                               output_file_colorized_by_rna_class_and_list,
                                               srnas_and_list_names):
    read_counting_table["t-SNE-component_1"] = [pos[0] for pos in tsne_result]
    read_counting_table["t-SNE-component_2"] = [pos[1] for pos in tsne_result]

    read_counting_table["Attributes_split"] = read_counting_table[
        "Attributes"].apply(
        lambda attr: dict(
            [key_value_pair.split("=") for
             key_value_pair in attr.split(";")]))

    hower_data = dict(
        x=read_counting_table["t-SNE-component_1"],
        y=read_counting_table["t-SNE-component_2"],
        feature=read_counting_table["Feature"])

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

    default_color = "#4271FF"
    # highlight_color = "#FF9C38"
    color = default_color

    color = read_counting_table.apply(
        _color_1, args=(srnas_and_list_names,), axis=1)

    p.circle("x", "y", source=source, size=5, alpha=0.7, color=color)

    url = "http://www.uniprot.org/uniprot/@protein_id"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Component 1"
    p.yaxis.axis_label = "Component 2"

    output_file(output_file_colorized_by_rna_class_and_list)


def _color_1(row, srnas_and_list_names):
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


def plot_using_only_rna_colors(read_counting_table, tsne_result, output_file_colorized_by_rna_class):
    read_counting_table["t-SNE-component_1"] = [pos[0] for pos in tsne_result]
    read_counting_table["t-SNE-component_2"] = [pos[1] for pos in tsne_result]

    read_counting_table["Attributes_split"] = read_counting_table[
        "Attributes"].apply(
        lambda attr: dict(
            [key_value_pair.split("=") for
             key_value_pair in attr.split(";")]))

    hower_data = dict(
        x=read_counting_table["t-SNE-component_1"],
        y=read_counting_table["t-SNE-component_2"],
        feature=read_counting_table["Feature"])

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

    default_color = "#4271FF"
    # highlight_color = "#FF9C38"
    color = default_color
    color = read_counting_table.apply(
        _color, axis=1)

    p.circle("x", "y", source=source, size=5, alpha=0.7, color=color)

    url = "http://www.uniprot.org/uniprot/@protein_id"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Component 1"
    p.yaxis.axis_label = "Component 2"

    output_file(output_file_colorized_by_rna_class)


def _color(row):
    color = {"CDS": "#BDBDBD", "ncRNA": "#FF4D4D", "tRNA": "#EBB000",
             "rRNA": "#8080FF", "tmRNA": "#3D3D3D"}[row["Feature"]]
    return color


def plot_t_sne_using_clustering(read_counting_table, tsne_result, output_file_colorized_by_clusters):
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

    output_file(output_file_colorized_by_clusters)

