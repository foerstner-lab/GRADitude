import pandas as pd
from sklearn.manifold import TSNE
import numpy as np
from bokeh.plotting import figure, output_file, save, ColumnDataSource
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models import WheelZoomTool, TapTool, OpenURL
import bokeh.palettes


def t_sne(feature_count_table, feature_count_start_column,
          perplexity, srna_list_files, cluster_names, output_file_colorized_by_clusters,
          output_file_colorized_by_rna_class,
          output_colored_by_lists):
    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column)
    t_sne_results = perform_t_sne(value_matrix, perplexity)
    plot_t_sne_using_clustering(feature_count_table_df, t_sne_results,
                                output_file_colorized_by_clusters)
    plot_using_only_rna_colors(feature_count_table_df, t_sne_results, output_file_colorized_by_rna_class)

    if srna_list_files:
        srnas_and_list_names = read_srna_lists(srna_list_files)
        plot_t_sne_colored_by_lists(feature_count_table_df, t_sne_results, output_colored_by_lists,
                                    srnas_and_list_names, cluster_names)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):-1]


def perform_t_sne(normalized_values, perplexity):
    model = TSNE(n_components=2, random_state=0, perplexity=perplexity)
    np.set_printoptions(suppress=True)
    tsne_result = model.fit_transform(normalized_values)
    return tsne_result


def plot_t_sne_using_clustering(read_counting_table, tsne_result, output_file_colorized_by_clusters):
    read_counting_table["t-SNE-component_1"] = [pos[0] for pos in tsne_result]
    read_counting_table["t-SNE-component_2"] = [pos[1] for pos in tsne_result]

    read_counting_table["Attributes_split"] = \
        read_counting_table["Attributes"].apply(lambda attr: dict(
            [key_value_pair.split("=")
             for key_value_pair in attr.split(";")]))

    color_palette = bokeh.palettes.Set2[(
        len(read_counting_table["Cluster_label"].unique()))]
    color = read_counting_table["Cluster_label"].apply(
        lambda lable: color_palette[lable])
    label = read_counting_table.apply(
        _label_clustering, axis=1)

    hower_data = dict(
        x=read_counting_table["t-SNE-component_1"],
        y=read_counting_table["t-SNE-component_2"],
        feature=read_counting_table["Feature"],
        gene=read_counting_table['Gene'],
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
        ("Feature", "@feature")])

    p = figure(plot_width=900, plot_height=900,
               tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                      WheelZoomTool(), "tap"],
               title="Grad-Seq t-SNE RNA-Seq", logo=None)

    p.circle("x", "y", source=source, size=7, alpha=1, color='color', legend="label", line_color="grey")
    p.yaxis.axis_label_text_font_size = "15pt"
    p.xaxis.axis_label_text_font_size = "15pt"
    p.title.text_font_size = '15pt'
    url = "https://ecocyc.org/ECOLI/search-query?type=GENE&gname=@gene"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Dimension 1"
    p.yaxis.axis_label = "Dimension 2"

    output_file(output_file_colorized_by_clusters)
    save(p)


def _label_clustering(row):
    __label = {0: "cluster1", 1: "cluster2", 2: "cluster3",
               3: "cluster4", 4: "cluster5", 5: "cluster6",
               6: "cluster7", 7: "cluster8"}[row["Cluster_label"]]
    return __label


def plot_using_only_rna_colors(read_counting_table, t_sne_result, output_file_colorized_by_rna_class):
    read_counting_table["t-SNE-component_1"] = [pos[0] for pos in t_sne_result]
    read_counting_table["t-SNE-component_2"] = [pos[1] for pos in t_sne_result]

    read_counting_table["Attributes_split"] = read_counting_table[
        "Attributes"].apply(
        lambda attr: dict(
            [key_value_pair.split("=") for
             key_value_pair in attr.split(";")]))

    feature_unique_values = read_counting_table["Feature"].unique()
    color_palette = bokeh.palettes.Set2[(len(feature_unique_values))]
    palette_map = {}
    for index in range(0, len(feature_unique_values)):
        palette_map[feature_unique_values[index]] = color_palette[index]
    color = read_counting_table["Feature"].apply(
        lambda lable: palette_map[lable])
    # color = read_counting_table.apply(
    #     color_palette, axis=1)
    label = read_counting_table.apply(
        _label, axis=1)

    hower_data = dict(
        x=read_counting_table["t-SNE-component_1"],
        y=read_counting_table["t-SNE-component_2"],
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

    p = figure(plot_width=900, plot_height=900,
               tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                      WheelZoomTool(), "tap"],
               title="Grad-Seq t-SNE RNA-Seq", logo=None)

    p.circle("x", "y", source=source, size=7, alpha=1, color='color', legend='label', line_color="grey")
    p.yaxis.axis_label_text_font_size = "15pt"
    p.xaxis.axis_label_text_font_size = "15pt"
    p.title.text_font_size = '15pt'

    url = "http://www.uniprot.org/uniprot/@protein_id"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Dimension 1"
    p.yaxis.axis_label = "Dimension 2"

    output_file(output_file_colorized_by_rna_class)
    save(p)


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


def plot_t_sne_colored_by_lists(read_counting_table, tsne_result,
                                output_file_list, srnas_and_list_names, cluster_names):
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
        _label_1, args=(srnas_and_list_names, cluster_names), axis=1)

    hower_data = dict(
        x=read_counting_table["t-SNE-component_1"],
        y=read_counting_table["t-SNE-component_2"],
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

    p = figure(plot_width=900, plot_height=900,
               tools=[hover, BoxZoomTool(), ResetTool(), PanTool(),
                      WheelZoomTool(), "tap"],
               title="Grad-Seq t-SNE RNA-Seq", logo=None)

    p.circle("x", "y", source=source, size=5, alpha=2, color="color", legend='label')
    p.yaxis.axis_label_text_font_size = "15pt"
    p.xaxis.axis_label_text_font_size = "15pt"
    p.title.text_font_size = '15pt'

    url = "http://www.uniprot.org/uniprot/@protein_id"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Dimension 1"
    p.yaxis.axis_label = "Dimension 2"

    output_file(output_file_list)
    save(p)


def _color_1(row, srnas_and_list_names):
    color = {"CDS": "#f5f5f5", "ncRNA": "#c7eae5", "tRNA": "#80cdc1",
             "rRNA": "#35978f", "sRNA": "#bf812d"
             }[row["Feature"]]
    srna_cluster_color = {"sRNA_cluster_1": "#FF4D4D",
                          "sRNA_cluster_2": "#EBB000",
                          "sRNA_cluster_3": "#8080FF",
                          "sRNA_cluster_4": "#3D3D3D"}
    for feature in ["Gene"]:
        if row[feature] in srnas_and_list_names:
            color = srna_cluster_color[
                srnas_and_list_names[row[feature]]]
    return color


def _label_1(row, srnas_and_list_names, cluster_names):
    label = {"ncRNA": "other ncRNAs", "sRNA": "other ncRNAs", "CDS": "CDS", "tRNA": "tRNA",
             "rRNA": "rRNA"}[row["Feature"]]
    srna_cluster_label = {}
    for index in range(0, len(cluster_names)):
        srna_cluster_label["sRNA_cluster_" + str(index + 1)] = cluster_names[index]

    for feature in ["Gene"]:
        if row[feature] in srnas_and_list_names:
            label = srna_cluster_label[
                srnas_and_list_names[row[feature]]]
    return label
