import pandas as pd
from sklearn.manifold import TSNE
import numpy as np
from bokeh.plotting import figure, output_file, save, ColumnDataSource
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models import WheelZoomTool, TapTool, OpenURL
import bokeh.palettes


def t_sne(feature_count_table, feature_count_start_column,
          perplexity, srna_list_files, output_file_colorized_by_clusters, output_file_colorized_by_rna_class,
          output_colored_by_lists):
    feature_count_table_df = pd.read_table(feature_count_table)
    srnas_and_list_names = read_srna_lists(srna_list_files)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column)
    t_sne_results = perform_t_sne(value_matrix, perplexity)
    plot_t_sne_using_clustering(feature_count_table_df, t_sne_results,
                                output_file_colorized_by_clusters)
    plot_using_only_rna_colors(feature_count_table_df, t_sne_results, output_file_colorized_by_rna_class)
    plot_t_sne_colored_by_lists(feature_count_table_df, t_sne_results, output_colored_by_lists, srnas_and_list_names)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):-1]


def perform_t_sne(normalized_values, perplexity):
    model = TSNE(n_components=2, random_state=0, perplexity=perplexity)
    np.set_printoptions(suppress=True)
    tsne_result = model.fit_transform(normalized_values)
    return tsne_result


def plot_using_only_rna_colors(read_counting_table, tsne_result, output_file_colorized_by_rna_class):
    read_counting_table["t-SNE-component_1"] = [pos[0] for pos in tsne_result]
    read_counting_table["t-SNE-component_2"] = [pos[1] for pos in tsne_result]

    read_counting_table["Attributes_split"] = read_counting_table[
        "Attributes"].apply(
        lambda attr: dict(
            [key_value_pair.split("=") for
             key_value_pair in attr.split(";")]))

    color = read_counting_table.apply(
        _color, axis=1)
    label = read_counting_table.apply(
        _label, axis=1)

    hower_data = dict(
        x=read_counting_table["t-SNE-component_1"],
        y=read_counting_table["t-SNE-component_2"],
        feature=read_counting_table["Feature"],
        color=color,
        label=label)

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

    p.circle("x", "y", source=source, size=5, alpha=0.7, color='color', legend='label')

    url = "http://www.uniprot.org/uniprot/@protein_id"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Component 1"
    p.yaxis.axis_label = "Component 2"

    output_file(output_file_colorized_by_rna_class)
    save(p)


def _color(row):
    color = {"CDS": "#BDBDBD", "ncRNA": "#f0f9e8", "tRNA": "#EBB000",
             "rRNA": "#8080FF", "tmRNA": "#3D3D3D", "5UTR": "9F000F",
             "3UTR": "0000AF", "pseudogenic_tRNA": "C2EFFF"
             }[row["Feature"]]
    return color


def _label(row):
    label = {"CDS": "#CDS", "ncRNA": "ncRNA", "tRNA": "tRNA",
             "rRNA": "rRNA", "tmRNA": "tmRNA", "5UTR": "5UTR",
             "3UTR": "3UTR"
             }[row["Feature"]]
    return label


def plot_t_sne_using_clustering(read_counting_table, tsne_result, output_file_colorized_by_clusters):
    read_counting_table["t-SNE-component_1"] = [pos[0] for pos in tsne_result]
    read_counting_table["t-SNE-component_2"] = [pos[1] for pos in tsne_result]

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


def read_srna_lists(srna_list_files):
    srnas_and_list_names = {}
    for index, srna_list_file in enumerate(srna_list_files):
        list_name = "sRNA_cluster_{}".format(index + 1)
        for line in open(srna_list_file):
            srnas_and_list_names[line.strip()] = list_name
    return srnas_and_list_names


def plot_t_sne_colored_by_lists(read_counting_table, tsne_result,
                                output_file_list, srnas_and_list_names):
    read_counting_table["t-SNE-component_1"] = [pos[0] for pos in tsne_result]
    read_counting_table["t-SNE-component_2"] = [pos[1] for pos in tsne_result]

    read_counting_table["Attributes_split"] = read_counting_table[
        "Attributes"].apply(
        lambda attr: dict(
            [key_value_pair.split("=") for
             key_value_pair in attr.split(";")]))

    color = read_counting_table.apply(
        _color_1, args=(srnas_and_list_names,), axis=1)
    label = read_counting_table.apply(
        _label_1, args=(srnas_and_list_names,), axis=1)

    hower_data = dict(
        x=read_counting_table["t-SNE-component_1"],
        y=read_counting_table["t-SNE-component_2"],
        feature=read_counting_table["Feature"],
        color=color,
        label=label)

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

    p.circle("x", "y", source=source, size=5, alpha=0.7, color="color", legend='label')

    url = "http://www.uniprot.org/uniprot/@protein_id"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Component 1"
    p.yaxis.axis_label = "Component 2"

    output_file(output_file_list)
    save(p)


def _color_1(row, srnas_and_list_names):
    color = {"CDS": "#BDBDBD", "ncRNA": "#a6cee3", "tRNA": "#EBB000",
             "rRNA": "#8080FF", "tmRNA": "#3D3D3D"}[row["Feature"]]
    sRNA_cluster_color = {"sRNA_cluster_1": "#1f78b4",
                          "sRNA_cluster_2": "#b2df8a",
                          "sRNA_cluster_3": "#33a02c",
                          "sRNA_cluster_4": "#fb9a99"}
    for feature in ["Gene"]:
        if row[feature] in srnas_and_list_names:
            color = sRNA_cluster_color[
                srnas_and_list_names[row[feature]]]
    return color


def _label_1(row, srnas_and_list_names):
    label = {"ncRNA": "ncRNA"}[row["Feature"]]
    srna_cluster_label = {
        "sRNA_cluster_1": "classic_CsrA",
        "sRNA_cluster_2": "unique_Hfq",
        "sRNA_cluster_3": "unique_ProQ",
        "sRNA_cluster_4": "Hfq_and_ProQ"}
    for feature in ["Gene"]:
        if row[feature] in srnas_and_list_names:
            label = srna_cluster_label[
                srnas_and_list_names[row[feature]]]
    return label
