from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import silhouette_score


def silhouette_analysis(feature_count_table, feature_count_start_column,
                        feature_count_end_column,
                        min_number_of_clusters, max_number_of_clusters):
    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column, feature_count_end_column)
    silhouette_plot(value_matrix, min_number_of_clusters, max_number_of_clusters)
    score(value_matrix, min_number_of_clusters, max_number_of_clusters)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column, feature_count_end_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):feature_count_end_column]


def silhouette_plot(value_matrix, min_number_of_clusters,
                    max_number_of_clusters):
    silhouette = []
    for n_clusters in range(int(min_number_of_clusters), int(max_number_of_clusters)):
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(value_matrix)
        labels = kmeans.labels_
        silhouette.append(silhouette_score(
            value_matrix, labels, metric='euclidean'))

    plt.plot(silhouette)
    plt.ylabel("Silhouette", fontsize=15)
    plt.xlabel("Number of clusters", fontsize=15)
    plt.title("Silhouette for K-means behaviour", fontsize=18)
    plt.savefig('silhouette.pdf')


def score(value_matrix, min_number_of_clusters,
          max_number_of_clusters):
    for n_clusters in range(int(min_number_of_clusters), int(max_number_of_clusters)):
        clusterer = KMeans(n_clusters=n_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(value_matrix)
        silhouette_avg = silhouette_score(value_matrix, cluster_labels)
        print("For n_clusters =", n_clusters,
              "The average silhouette_score is :", silhouette_avg)
