import pandas as pd
from sklearn.neighbors import NearestNeighbors

import matplotlib.pyplot as plt


def generate_nearest_neighbors(feature_count_table,
                               feature_count_start_column, n_neighbors, output_file):
    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column)
    nearest_neighbors(value_matrix, n_neighbors, output_file)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):]


def _extract_attributes(feature_count_table_df,
                        feature_count_start_column):
    return feature_count_table_df.iloc[:, : int(feature_count_start_column)]


def nearest_neighbors(value_matrix, n_neighbors, output_file):
    nearest_neighbors_ = NearestNeighbors(n_neighbors=n_neighbors).fit(value_matrix)
    distances, indices = nearest_neighbors_.kneighbors(value_matrix)
    my_distance = distances[:, -1]
    sorted_list = sorted(my_distance, reverse=True)
    plt.plot(sorted_list)
    plt.savefig(output_file)
    plt.close()
