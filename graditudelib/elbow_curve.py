import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist, pdist
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def k_means_clustering_elbow(feature_count_table, feature_count_start_column, min_number_of_clusters,
                             max_number_of_clusters):

    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column)
    elbow_methods(value_matrix, min_number_of_clusters, max_number_of_clusters)
    elbow_methods1(value_matrix, min_number_of_clusters, max_number_of_clusters)


def elbow_methods(value_matrix, min_number_of_clusters,
                  max_number_of_clusters):
    range_k = range(int(min_number_of_clusters), int(max_number_of_clusters))
    k_m = [KMeans(n_clusters=k).fit(value_matrix) for k in range_k]
    centroids = [k.cluster_centers_ for k in k_m]
    d_k = [cdist(value_matrix, cent, 'euclidean') for cent in centroids]
    dist = [np.min(D, axis=1) for D in d_k]
    w_css = [sum(d ** 2) for d in dist]
    tss = sum(pdist(value_matrix) ** 2) / value_matrix.shape[0]
    bss = tss - w_css
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range_k, bss/tss*100, 'b*-')
    plt.grid(True)
    plt.xlabel('Number of clusters')
    plt.ylabel('Percentage of variance explained')
    plt.title('Elbow for KMeans clustering')
    plt.savefig('elbow_for_kmeans_clustering2.pdf', format='pdf')


def elbow_methods1(value_matrix, min_number_of_clusters,
                   max_number_of_clusters):
    range_k = range(int(min_number_of_clusters), int(max_number_of_clusters))
    k_m = [KMeans(n_clusters=k).fit(value_matrix) for k in range_k]
    centroids = [k.cluster_centers_ for k in k_m]
    d_k = [cdist(value_matrix, cent, 'euclidean') for cent in centroids]
    dist = [np.min(D, axis=1) for D in d_k]
    avg_within_sum_of_squares = [sum(d)/value_matrix.shape[0] for d in dist]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range_k, avg_within_sum_of_squares, 'b*-')
    plt.grid(True)
    plt.xlabel('Number of clusters')
    plt.ylabel('Average within-cluster sum of squares')
    plt.title('Elbow for KMeans clustering')
    plt.savefig('elbow_for_kmeans_clustering.pdf', format='pdf')


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):]


