import pandas as pd
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN


def clustering(feature_count_table, feature_count_start_column, feature_count_end_column,
               number_of_clusters, clustering_methods, epsilon, min_samples, output_file):
    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column, feature_count_end_column)
    attribute_matrix = _extract_attributes(feature_count_table_df,
                                           feature_count_start_column)
    if clustering_methods == 'k-means':
        table_with_clusters = k_means_clustering(value_matrix, number_of_clusters)
    elif clustering_methods == 'hierarchical_clustering':
        table_with_clusters = hierarchical_clustering(value_matrix, number_of_clusters)
    elif clustering_methods == 'DBSCAN':
        table_with_clusters = dbscan_clustering(value_matrix, epsilon, min_samples)
    pd.concat([attribute_matrix, table_with_clusters],
              axis=1).to_csv(output_file, sep='\t', index=None)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column, feature_count_end_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):feature_count_end_column]


def _extract_attributes(feature_count_table_df,
                        feature_count_start_column):
    return feature_count_table_df.iloc[:, : int(feature_count_start_column)]


def hierarchical_clustering(values_matrix, number_of_clusters):
    h_clustering = AgglomerativeClustering(n_clusters=number_of_clusters,
                                           affinity="euclidean", linkage="ward")
    h_clustering.fit(values_matrix)
    labels = h_clustering.labels_
    pd.DataFrame(data=labels, columns=['cluster'])
    values_matrix["Cluster_label"] = pd.Series(h_clustering.labels_).astype(int)
    return values_matrix


def k_means_clustering(values_matrix, number_of_clusters):
    k_means = KMeans(n_clusters=number_of_clusters, random_state=0)
    k_means.fit(values_matrix)
    labels = k_means.labels_
    pd.DataFrame(data=labels, columns=['cluster'])
    values_matrix["Cluster_label"] = pd.Series(k_means.labels_).astype(int)
    return values_matrix


def dbscan_clustering(values_matrix, epsilon, min_samples):
    dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)
    dbscan.fit_predict(values_matrix)
    labels = dbscan.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    print('Estimated number of clusters: %d' % n_clusters_)
    pd.DataFrame(data=labels, columns=['cluster'])
    values_matrix["Cluster_label"] = pd.Series(dbscan.labels_).astype(int)
    return values_matrix
