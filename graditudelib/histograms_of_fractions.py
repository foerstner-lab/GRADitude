import matplotlib.pyplot as plt
import pandas as pd


def plot_histograms(feature_count_table,
                    feature_count_start_column,
                    feature_count_end_column):

    feature_count_table_df = pd.read_table(feature_count_table)

    feature_count_table_df_value = _extract_value_matrix(
        feature_count_table_df,
        feature_count_start_column,
        feature_count_end_column
    )

    _plot_histogram_pdf(feature_count_table_df_value)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column,
                          feature_count_end_column):

    return feature_count_table_df.iloc[
        :,
        int(feature_count_start_column):
        int(feature_count_end_column) + 1
    ]


def _plot_histogram_pdf(feature_count_table_df_value):

    for column in feature_count_table_df_value:

        plt.figure()

        plt.hist(
            feature_count_table_df_value[column].values
        )

        plt.title(column)

        plt.savefig(f"{column}.pdf")

        plt.close()