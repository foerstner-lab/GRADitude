import pandas as pd
import holoviews as hv
import matplotlib.pyplot as plt

hv.extension('bokeh', width=90)


def plot_heatmap(feature_count_table, feature_count_start_column,
                 feature_count_end_column, y_label_, output_file):
    table = pd.read_table(feature_count_table, sep="\t")
    table.set_index('Gene', inplace=True)
    value_matrix = _extract_value_matrix(table, feature_count_start_column,
                                         feature_count_end_column)
    heatmaps(value_matrix, y_label_, output_file)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column, feature_count_end_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column) - 1:feature_count_end_column - 1]


def heatmaps(value_matrix, y_label_, output_file):
    fig, axes_x = plt.subplots(figsize=(100, 100))
    imshow_ = axes_x.imshow(value_matrix, cmap="Greens")
    fig.colorbar(imshow_, ax=axes_x)
    axes_x.set_xticks(range(len(value_matrix.columns)))
    axes_x.set_yticks(range(len(value_matrix.index)))
    axes_x.set_xticklabels(range(1, 21))
    axes_x.set_yticklabels(value_matrix.index)
    axes_x.set_xlabel("Fractions", fontsize=18)
    axes_x.set_ylabel(y_label_, fontsize=10)
    plt.savefig(output_file)
    plt.show()
