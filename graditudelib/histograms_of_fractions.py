import matplotlib.pyplot as plt
import pandas as pd


def plot_histograms(feature_count_table,
                    feature_count_start_column):
    feature_count_table_df = pd.read_table(feature_count_table)
    feature_count_table_df_value = _extract_value_matrix(feature_count_table_df, feature_count_start_column)
    _plot_histogram_pdf(feature_count_table_df_value)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):]


def _plot_histogram_pdf(counting_value_list):
    counting_value_list.plot.hist(bins=50, legend=False)
    plt.show()
