import pandas as pd
from sklearn.neighbors import NearestNeighbors

import matplotlib.pyplot as plt


def generate_nearest_neighbors(feature_count_table,
                               feature_count_start_column):
    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column)
    nearest_neighbors(value_matrix)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):]


def _extract_attributes(feature_count_table_df,
                        feature_count_start_column):
    return feature_count_table_df.iloc[:, : int(feature_count_start_column)]


def nearest_neighbors(value_matrix):
    nearest_neighbors_ = NearestNeighbors(n_neighbors=41).fit(value_matrix)
    distances, indices = nearest_neighbors_.kneighbors(value_matrix)

    my_distance = distances[:, -1]
    my_distance_df = pd.DataFrame(my_distance)
    my_distance_df_div = my_distance_df.divide(len(my_distance))
    sorted_df = my_distance_df_div.sort_values(by=0, ascending=False)
    sorted_list = sorted_df[0].tolist()
    plt.plot(sorted_list)
    plt.show()
