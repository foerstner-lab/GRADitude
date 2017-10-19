import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show
from scipy import interpolate
import numpy as np


def plot_kinetics(feature_count_table,
                  gene_name, feature_count_start_column):
    feature_count_table_df = pd.read_table(feature_count_table)

    gene_row = _extract_gene_row(feature_count_table_df, gene_name)
    value_gene_row = _extract_value_gene_row(gene_row, feature_count_start_column).values.T.tolist()
    _plot_gene_png(value_gene_row, gene_name)
    _plot_gene_html(value_gene_row, gene_name)


def _extract_gene_row(feature_count_table_df, gene_name):
    return feature_count_table_df.loc[feature_count_table_df['Gene'] == gene_name]


def _extract_value_gene_row(gene_row, feature_count_start_column):
    return gene_row.iloc[:, feature_count_start_column:]


def _plot_gene_html(counting_value_list, gene_name):
    output_file(gene_name + '.html')
    plot_html = figure(title="GRAD-seq" +
                             '\n' + gene_name,
                       x_axis_label='Fraction number',
                       y_axis_label='Read counts')
    y_axis = range(0, 21)
    plot_html.line(y_axis, counting_value_list)
    show(plot_html)


def _plot_gene_png(counting_value_list, gene_name):
    flattened = [val for sublist in counting_value_list for val in sublist]
    flattened_series = pd.Series(flattened)
    x_axis = range(1, 22)
    interpolation = interpolate.interp1d(x_axis, flattened_series, kind="linear")
    x_int = np.linspace(x_axis[0], x_axis[-1], 20)
    y_int = interpolation(x_int)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x_axis, flattened_series, color='red', label='Unsmoothed curve')
    ax.plot(x_int, y_int, color="blue", label="Interpolated curve")
    plt.show()
    plt.savefig(gene_name + '.png')

