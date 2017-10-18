import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def correlation(
        feature_count_table, feature_count_start_column):
    feature_count_table_df = pd.read_table(feature_count_table, sep='\t')
    feature_count_table_df_value = _extract_value_matrix(feature_count_table_df, feature_count_start_column)
    feature_count_table_df_value.set_index(['Gene'], inplace=True)
    corr_hist(feature_count_table_df_value)
    corr_heatmap(feature_count_table_df_value)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):]


def corr_hist(feature_count_table_df_value):
    correlation_ = np.corrcoef(feature_count_table_df_value)
    correlation_flattened = np.ndarray.flatten(correlation_)
    # correlation_df.to_csv('table_with_correlation_coefficients.csv')

    fig = plt.figure(figsize=(15, 15))
    ax1 = fig.add_subplot(211)
    ax1.hist(correlation_flattened)
    plt.savefig('hist.png')


def corr_heatmap(feature_count_table_df_value):
    correlation_ = np.corrcoef(feature_count_table_df_value)
    sns.heatmap(correlation_, vmin=-1, vmax=1)
    plt.savefig('heatmap.png')






