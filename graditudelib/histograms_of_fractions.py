import matplotlib.pyplot as plt
import pandas as pd
import math


def plot_histograms(feature_count_table,
                    feature_count_start_column,
                    feature_count_end_column, output_file):

    feature_count_table_df = pd.read_table(feature_count_table)

    feature_count_table_df_value = _extract_value_matrix(
        feature_count_table_df,
        feature_count_start_column,
        feature_count_end_column
    )

    _plot_histogram_pdf(feature_count_table_df_value, output_file)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column,
                          feature_count_end_column):

    return feature_count_table_df.iloc[
        :,
        int(feature_count_start_column):
        int(feature_count_end_column) + 1
    ]


def _plot_histogram_pdf(feature_count_table_df_value,
                        output_file):

    n_plots = len(feature_count_table_df_value.columns)

    n_cols = 4
    n_rows = math.ceil(n_plots / n_cols)

    fig, axes = plt.subplots(
        n_rows,
        n_cols,
        figsize=(4 * n_cols, 3 * n_rows)
    )

    axes = axes.flatten()

    for i, column in enumerate(feature_count_table_df_value):
        axes[i].hist(
            feature_count_table_df_value[column].values,
            bins=50
        )

        axes[i].set_title(column, fontsize=8)

    fig.supxlabel("Scaled abundance")
    fig.supylabel("Number of features")
    fig.suptitle(
        "Distribution of scaled abundance values across gradient fractions",
        fontsize=14
    )

    for j in range(i + 1, len(axes)):
        axes[j].axis("off")

    plt.tight_layout(rect=[0.02, 0.02, 1, 0.96])
    plt.savefig(output_file)
    plt.close()