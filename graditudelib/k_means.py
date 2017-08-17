import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def generate_k_means_clustering(feature_count_table,
                                feature_count_start_column,
                                number_of_clusters,
                                output_file, scaling_method, pseudo_count):
    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column)
    new_table = normalize_values(value_matrix, scaling_method, pseudo_count)
    attribute_matrix = _extract_attributes(feature_count_table_df,
                                           feature_count_start_column)
    clustering_table = k_means_clustering(new_table, number_of_clusters)
    pd.concat([attribute_matrix, clustering_table],
              axis=1).to_csv(output_file, sep='\t')


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):]


def _extract_attributes(feature_count_table_df,
                        feature_count_start_column):
    return feature_count_table_df.iloc[:, : int(feature_count_start_column)]


def k_means_clustering(values_matrix, number_of_clusters):
    values_matrix.as_matrix()
    k_means = KMeans(n_clusters=number_of_clusters, random_state=0)
    k_means.fit(values_matrix)
    labels = k_means.labels_
    pd.DataFrame(data=labels, columns=['cluster'])
    values_matrix["Cluster_label"] = pd.Series(k_means.labels_).astype(int)
    return values_matrix


def normalize_values(read_counting_table, scaling_method, pseudo_count):
    pseudo_count = 1.0
    read_countings_values_only = read_counting_table[list(filter(
        lambda col: col.startswith("Grad_47"), read_counting_table.columns))]
    if scaling_method == "no_normalization":
        normalized_values = read_countings_values_only
    elif scaling_method == "log2":
        normalized_values = read_countings_values_only.applymap(
            lambda val: val + pseudo_count).applymap(np.log2)
    elif scaling_method == "log10":
        normalized_values = read_countings_values_only.applymap(
            lambda val: val + pseudo_count).applymap(np.log10)
    elif scaling_method == "normalized_to_max":
        row_max_values = read_countings_values_only.max(axis=1)
        normalized_values = read_countings_values_only.divide(
            row_max_values, axis=0)
    elif scaling_method == "normalized_to_range":
        row_max_values = read_countings_values_only.max(axis=1)
        row_min_values = read_countings_values_only.min(axis=1)
        normalized_values = read_countings_values_only.subtract(
            row_min_values, axis=0).divide(row_max_values, axis=0)
    else:
        print("Normalization method not known")
    return normalized_values

