import pandas as pd
import umap
import bokeh.palettes
from bokeh.plotting import figure, output_file, save, ColumnDataSource
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models import WheelZoomTool, TapTool, OpenURL


def umap_(feature_count_table, feature_count_start_column,
          feature_count_end_column, srna_list_files, cluster_names,
          n_neighbors, min_dist,
          url_link, output_file_colorized_by_clusters,
          output_file_colorized_by_rna_class,
          output_colored_by_lists):
    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column,
                                         feature_count_end_column)
    umap_results = perform_umap(value_matrix, n_neighbors, min_dist)
    plot_t_sne_using_clustering(feature_count_table_df, umap_results,
                                output_file_colorized_by_clusters, url_link)
    plot_using_only_rna_colors(feature_count_table_df, umap_results,
                               output_file_colorized_by_rna_class,
                               url_link)

    if srna_list_files:
        srnas_and_list_names = read_srna_lists(srna_list_files)
        plot_t_sne_colored_by_lists(feature_count_table_df,
                                    umap_results, output_colored_by_lists,
                                    srnas_and_list_names,
                                    cluster_names, url_link)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column,
                          feature_count_end_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):feature_count_end_column]


def perform_umap(normalized_values, n_neighbors, min_dist):
    reducer = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist)
    umap_results = reducer.fit_transform(normalized_values)
    return umap_results


def plot_t_sne_using_clustering(read_counting_table, umap_results,
                                output_file_colorized_by_clusters,
                                url_link):
    read_counting_table["UMAP-component_1"] = [pos[0] for pos in umap_results]
    read_counting_table["UMAP-component_2"] = [pos[1] for pos in umap_results]

    read_counting_table["Attributes_split"] = \
        read_counting_table["Attributes"].apply(lambda attr: dict(
            [key_value_pair.split("=")
             for key_value_pair in attr.split(";")]))

    color_palette = bokeh.palettes.Colorblind[(
        len(read_counting_table["Cluster_label"].unique()))]
    color = read_counting_table["Cluster_label"].apply(
        lambda lable: color_palette[lable])
    label = read_counting_table.apply(
        _label_clustering, axis=1)

    hower_data = dict(
        x=read_counting_table["UMAP-component_1"],
        y=read_counting_table["UMAP-component_2"],
        feature=read_counting_table["Feature"],
        gene=read_counting_table['Gene'],
        cluster_label=read_counting_table["Cluster_label"],
        color=color,
        label=label)

    for feature in ["ID", "Parent", "Dbxref", "Note", "function",
                    "gbkey", "product", "sRNA_type"]:
        read_counting_table[feature] = read_counting_table[
            "Attributes_split"].apply(
            lambda attributes: attributes.get(feature, "-"))
        hower_data[feature] = read_counting_table[feature]

    source = ColumnDataSource(hower_data)

    hover = HoverTool(tooltips=[
        ("Gene", "@gene"),
        ("ID", "@ID"),
        ("Feature", "@feature"),
        ("Cluster label", "@cluster_label")])

    plot = figure(plot_width=900, plot_height=900,
                  tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                         WheelZoomTool(), "tap"],
                  title="Grad-Seq UMAP-RNA-Seq")

    plot.circle("x", "y", source=source, size=7, alpha=3, color='color',
                legend="label", line_color="black")
    plot.yaxis.axis_label_text_font_size = "15pt"
    plot.xaxis.axis_label_text_font_size = "15pt"
    plot.title.text_font_size = '15pt'
    url = url_link
    taptool = plot.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    plot.xaxis.axis_label = "Dimension 1"
    plot.yaxis.axis_label = "Dimension 2"

    output_file(output_file_colorized_by_clusters)
    save(plot)


def _label_clustering(row):
    __label = {0: "cluster1", 1: "cluster2", 2: "cluster3",
               3: "cluster4", 4: "cluster5", 5: "cluster6",
               6: "cluster7", 7: "cluster8"}[row["Cluster_label"]]
    return __label


def create_palette_map(read_counting_table):
    feature_unique_values = read_counting_table["Feature"].unique()
    colors = len(feature_unique_values)

    if colors < 3:
        color_palette = ["#0000ff", "#ffff00"]
    else:
        color_palette = bokeh.palettes.Colorblind[colors]

    palette_map = {}
    for index in range(0, len(feature_unique_values)):
        palette_map[feature_unique_values[index]] = color_palette[index]
    return palette_map


def plot_using_only_rna_colors(read_counting_table, umap_results,
                               output_file_colorized_by_rna_class,
                               url_link):
    read_counting_table["UMAP-component_1"] = [pos[0] for pos in umap_results]
    read_counting_table["UMAP-component_2"] = [pos[1] for pos in umap_results]

    read_counting_table["Attributes_split"] = read_counting_table[
        "Attributes"].apply(
        lambda attr: dict(
            [key_value_pair.split("=") for
             key_value_pair in attr.split(";")]))

    palette_map = create_palette_map(read_counting_table)
    color = read_counting_table["Feature"].apply(
        lambda lable: palette_map[lable])
    label = read_counting_table.apply(
        _label, axis=1)

    hower_data = dict(
        x=read_counting_table["UMAP-component_1"],
        y=read_counting_table["UMAP-component_2"],
        feature=read_counting_table["Feature"],
        gene=read_counting_table["Gene"],
        color=color,
        label=label)

    for feature in ["product", "ID", "type", "ncrna_class",
                    "sRNA_type", "Name", "pseudo"]:
        read_counting_table[feature] = read_counting_table[
            "Attributes_split"].apply(
            lambda attributes: attributes.get(feature, "-"))
        hower_data[feature] = read_counting_table[feature]

    source = ColumnDataSource(hower_data)

    hover = HoverTool(tooltips=[
        ("Gene", "@gene"),
        ("ID", "@ID"),
        ("Feature", "@feature")])

    plot = figure(plot_width=900, plot_height=900,
                  tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                         WheelZoomTool(), "tap"],
                  title="Grad-Seq UMAP-RNA-Seq")

    plot.circle("x", "y", source=source, size=7, alpha=3, color='color',
                legend='label', line_color="black")
    plot.yaxis.axis_label_text_font_size = "15pt"
    plot.xaxis.axis_label_text_font_size = "15pt"
    plot.title.text_font_size = '15pt'

    url = url_link
    taptool = plot.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    plot.xaxis.axis_label = "Dimension 1"
    plot.yaxis.axis_label = "Dimension 2"

    output_file(output_file_colorized_by_rna_class)
    save(plot)


def _label(row):
    label = {"CDS": "CDS", "ncRNA": "ncRNA", "tRNA": "tRNA",
             "rRNA": "rRNA", "tmRNA": "tmRNA", "5UTR": "5UTR",
             "3UTR": "3UTR", "sRNA": "sRNA"
             }[row["Feature"]]
    return label


def read_srna_lists(srna_list_files):
    srnas_and_list_names = {}
    for index, srna_list_file in enumerate(srna_list_files):
        list_name = "sRNA_cluster_{}".format(index + 1)
        for line in open(srna_list_file):
            srnas_and_list_names[line.strip()] = list_name
    return srnas_and_list_names


def plot_t_sne_colored_by_lists(read_counting_table, umap_results,
                                output_file_list, srnas_and_list_names,
                                cluster_names, url_link):
    read_counting_table["UMAP-component_1"] = [pos[0] for pos in umap_results]
    read_counting_table["UMAP-component_2"] = [pos[1] for pos in umap_results]

    read_counting_table["Attributes_split"] = read_counting_table[
        "Attributes"].apply(
        lambda attr: dict(
            [key_value_pair.split("=") for
             key_value_pair in attr.split(";")]))

    palette_map = create_palette_map(read_counting_table)
    color = read_counting_table.apply(
        _color_1, args=(srnas_and_list_names, palette_map), axis=1)
    label = read_counting_table.apply(
        _label_1, args=(srnas_and_list_names, cluster_names), axis=1)

    hower_data = dict(
        x=read_counting_table["UMAP-component_1"],
        y=read_counting_table["UMAP-component_2"],
        feature=read_counting_table["Feature"],
        gene=read_counting_table["Gene"],
        color=color,
        label=label)

    for feature in ["product", "ID", "type", "ncrna_class",
                    "sRNA_type", "Name", "pseudo"]:
        read_counting_table[feature] = read_counting_table[
            "Attributes_split"].apply(
            lambda attributes: attributes.get(feature, "-"))
        hower_data[feature] = read_counting_table[feature]

    source = ColumnDataSource(hower_data)

    hover = HoverTool(tooltips=[
        ("Gene", "@gene"),
        ("ID", "@ID"),
        ("Feature", "@feature")])

    plot = figure(plot_width=900, plot_height=900,
                  tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                         WheelZoomTool(), "tap"],
                  title="Grad-Seq UMAP-RNA-Seq")

    plot.circle("x", "y", source=source, size=7, alpha=3, color="color",
                legend='label', line_color="black")
    plot.yaxis.axis_label_text_font_size = "15pt"
    plot.xaxis.axis_label_text_font_size = "15pt"
    plot.title.text_font_size = '15pt'

    url = url_link
    taptool = plot.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    plot.xaxis.axis_label = "Dimension 1"
    plot.yaxis.axis_label = "Dimension 2"

    output_file(output_file_list)
    save(plot)


def _color_1(row, srnas_and_list_names, palette_map):
    color = palette_map[row["Feature"]]
    srna_cluster_color = {"sRNA_cluster_1": "#FF4D4D",
                          "sRNA_cluster_2": "#F0F3F4",
                          "sRNA_cluster_3": "#000000",
                          "sRNA_cluster_4": "#FFFF00"}
    for feature in ["Gene"]:
        if row[feature] in srnas_and_list_names:
            color = srna_cluster_color[
                srnas_and_list_names[row[feature]]]
    return color


def _label_1(row, srnas_and_list_names, cluster_names):
    label = {"ncRNA": "other ncRNAs", "sRNA": "other ncRNAs",
             "CDS": "CDS", "tRNA": "tRNA",
             "rRNA": "rRNA", "5'-UTR": "5'-UTR", "3'-UTR":
                 "3'-UTR"}[row["Feature"]]
    srna_cluster_label = {}
    for index in range(0, len(cluster_names)):
        srna_cluster_label["sRNA_cluster_" + str(index + 1)] = \
            cluster_names[index]

    for feature in ["Gene"]:
        if row[feature] in srnas_and_list_names:
            label = srna_cluster_label[
                srnas_and_list_names[row[feature]]]
    return label
