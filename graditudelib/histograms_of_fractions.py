import matplotlib.pyplot as plt
import pandas as pd


def plot_histograms(feature_count_table,
                    feature_count_start_column):
    feature_count_table_df = pd.read_table(feature_count_table)
    feature_count_table_df_value = _extract_value_matrix(feature_count_table_df,
                                                         feature_count_start_column)
    _plot_histogram_pdf(feature_count_table_df_value)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):]


def _plot_histogram_pdf(feature_count_table_df_value):
    i = 0
    for column in feature_count_table_df_value:
        i = i + 1
        plt.figure(i)
        plt.hist(feature_count_table_df_value[column].values)
        # plt.show()
        plt.savefig(column)
