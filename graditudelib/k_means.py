import pandas as pd
from sklearn.cluster import KMeans


def generate_k_means_clustering(feature_count_table,
                                feature_count_start_column,
                                number_of_clusters,
                                output_file):
    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column)
    attribute_matrix = _extract_attributes(feature_count_table_df,
                                           feature_count_start_column)
    clustering_table = k_means_clustering(value_matrix, number_of_clusters)
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
