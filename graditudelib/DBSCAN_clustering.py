from sklearn.cluster import DBSCAN
import pandas as pd
import numpy as np


def generate_dbscan_clustering(feature_count_table,
                               feature_count_start_column,
                               scaling_method, pseudo_count, epsilon, min_samples, output_file):
    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column)
    new_table = normalize_values(value_matrix, scaling_method, pseudo_count)
    attribute_matrix = _extract_attributes(feature_count_table_df,
                                           feature_count_start_column)
    clustering_table = dbscan_clustering(new_table, epsilon, min_samples)
    pd.concat([attribute_matrix, clustering_table],
              axis=1).to_csv(output_file, sep='\t', index=0)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):]


def _extract_attributes(feature_count_table_df,
                        feature_count_start_column):
    return feature_count_table_df.iloc[:, : int(feature_count_start_column)]


def dbscan_clustering(values_matrix, epsilon, min_samples):
    dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)
    dbscan.fit_predict(values_matrix)
    labels = dbscan.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    print('Estimated number of clusters: %d' % n_clusters_)
    pd.DataFrame(data=labels, columns=['cluster'])
    values_matrix["Cluster_label"] = pd.Series(dbscan.labels_).astype(int)
    return values_matrix


def normalize_values(values_matrix, scaling_method, pseudo_count):
    if scaling_method == "no_normalization":
        normalized_values = values_matrix
    elif scaling_method == "log2":
        normalized_values = values_matrix.applymap(
            lambda val: val + pseudo_count).applymap(np.log2)
    elif scaling_method == "log10":
        normalized_values = values_matrix.applymap(
            lambda val: val + pseudo_count).applymap(np.log10)
    elif scaling_method == "normalized_to_max":
        values_matrix = values_matrix.fillna(lambda x: 0)
        row_max_values = values_matrix.max(axis=1)
        normalized_values = values_matrix.divide(
            row_max_values, axis=0)
        normalized_values = pd.DataFrame(normalized_values).fillna(0)
    elif scaling_method == "normalized_to_range":
        values_matrix = values_matrix.fillna(lambda x: 0)
        row_max_values = values_matrix.max(axis=1)
        row_min_values = values_matrix.min(axis=1)
        normalized_values = values_matrix.subtract(
            row_min_values, axis=0).divide(row_max_values, axis=0)
        normalized_values = pd.DataFrame(normalized_values).fillna(0)
    else:
        print("Normalization method not known")
    return normalized_values

