#!/usr/bin/env python

import argparse
import pandas as pd
import sys
from sklearn.manifold import TSNE
import numpy as np
from bokeh.plotting import figure, output_file, save, ColumnDataSource
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, PanTool
from bokeh.models import WheelZoomTool, TapTool, OpenURL


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    parser.add_argument("normalization_method")

    # TMP! CAN HANDLE CURRENTLY 3 FILES:
    parser.add_argument("snra_list_files", nargs="+")

    args = parser.parse_args()

    read_counting_table = pd.read_table(args.input_file)
    srnas_and_list_names = read_srna_lists(args.snra_list_files)

    normalized_values = normalize_values(
        read_counting_table, args.normalization_method)
    tsne_result = perform_t_sne(normalized_values)
    plot(read_counting_table, tsne_result, args.output_file,
         srnas_and_list_names)

    
def normalize_values(read_counting_table, normalization_method):
    pseudocount = 1.0
    read_countings_values_only = read_counting_table[list(filter(
        lambda col: col.startswith("Grad_47"), read_counting_table.columns))]
    # print(read_countings_values_only)
    if normalization_method == "no_normalization":
        normalized_values = read_countings_values_only
    elif normalization_method == "log2":
        normalized_values = read_countings_values_only.applymap(
            lambda val: val + pseudocount).applymap(np.log2)
    elif normalization_method == "log10":
        normalized_values = read_countings_values_only.applymap(
            lambda val: val + pseudocount).applymap(np.log10)
    elif normalization_method == "normalized_to_max":
        row_max_values = read_countings_values_only.max(axis=1)
        normalized_values = read_countings_values_only.divide(
            row_max_values, axis=0)
    elif normalization_method == "normalized_to_range":
        row_max_values = read_countings_values_only.max(axis=1)
        row_min_values = read_countings_values_only.min(axis=1)
        normalized_values = read_countings_values_only.subtract(
            row_min_values, axis=0).divide(row_max_values, axis=0)
    else:
        print("Normalization method not known")
        sys.exit(1)
    return normalized_values


def perform_t_sne(normalized_values):
    model = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    tsne_result = model.fit_transform(normalized_values)
    return tsne_result


def read_srna_lists(srna_list_files):
    srnas_and_list_names = {}
    for index, srna_list_file in enumerate(srna_list_files):
        list_name = "sRNA_cluster_{}".format(index+1)
        for line in open(srna_list_file):
            srnas_and_list_names[line.strip()] = list_name
    return srnas_and_list_names

    
def plot(read_counting_table, tsne_result, output_file_path,
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
        _color, args=(srnas_and_list_names,), axis=1)

    p.circle("x", "y", source=source, size=5, alpha=0.7, color=color)

    url = "http://www.uniprot.org/uniprot/@protein_id"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    p.xaxis.axis_label = "Component 1"
    p.yaxis.axis_label = "Component 2"

    output_file(output_file_path)
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


if __name__ == "__main__":
    main()
