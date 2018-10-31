import pandas as pd
import holoviews as hv
import matplotlib.pyplot as plt

hv.extension('bokeh', width=90)


def plot_heatmap(feature_count_table, feature_count_start_column, y_label_, output_file):
    table = pd.read_table(feature_count_table, sep=",")
    table.set_index('Gene', inplace=True)
    value_matrix = _extract_value_matrix(table, feature_count_start_column)
    heatmaps(value_matrix, y_label_, output_file)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):]


def heatmaps(value_matrix, y_label_, output_file):
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.imshow(value_matrix, cmap="Greens")
    fig.colorbar(im, ax=ax)
    ax.set_xticks(range(len(value_matrix.columns)))
    ax.set_yticks(range(len(value_matrix.index)))
    ax.set_xticklabels(range(1, 21))
    ax.set_yticklabels(value_matrix.index)
    ax.set_xlabel("Fractions", fontsize=18)
    ax.set_ylabel(y_label_, fontsize=18)
    plt.savefig(output_file)
    plt.show()
