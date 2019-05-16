import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist, pdist
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def k_means_clustering_elbow(feature_count_table, feature_count_start_column,
                             feature_count_end_column,
                             min_number_of_clusters, max_number_of_clusters, output_plots1,
                             output_plot2):
    feature_count_table_df = pd.read_csv(feature_count_table, sep='\t')
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column,
                                         feature_count_end_column)
    elbow_methods(value_matrix, min_number_of_clusters, max_number_of_clusters,
                  output_plots1)
    elbow_methods1(value_matrix, min_number_of_clusters,
                   max_number_of_clusters, output_plot2)


def elbow_methods(value_matrix, min_number_of_clusters,
                  max_number_of_clusters, output_plots1):
    range_k = range(int(min_number_of_clusters), int(max_number_of_clusters))
    k_m = [KMeans(n_clusters=k).fit(value_matrix) for k in range_k]
    centroids = [k.cluster_centers_ for k in k_m]
    d_k = [cdist(value_matrix, cent, 'euclidean') for cent in centroids]
    dist = [np.min(D, axis=1) for D in d_k]
    w_css = [sum(d ** 2) for d in dist]
    tss = sum(pdist(value_matrix) ** 2) / value_matrix.shape[0]

    bss = tss - w_css
    fig = plt.figure()
    axes_x = fig.add_subplot(111)
    axes_x.plot(range_k, bss / tss * 100, 'b*-')
    plt.grid(True)
    plt.xlabel('Number of clusters', fontsize=15)
    plt.ylabel('Percentage of variance explained', fontsize=15)
    plt.title('Elbow for KMeans clustering', fontsize=18)
    plt.savefig(output_plots1, format='pdf')


def elbow_methods1(value_matrix, min_number_of_clusters,
                   max_number_of_clusters, output_plot2):
    range_k = range(int(min_number_of_clusters), int(max_number_of_clusters))
    k_m = [KMeans(n_clusters=k).fit(value_matrix) for k in range_k]
    centroids = [k.cluster_centers_ for k in k_m]
    d_k = [cdist(value_matrix, cent, 'euclidean') for cent in centroids]
    dist = [np.min(D, axis=1) for D in d_k]
    avg_within_sum_of_squares = [sum(d) / value_matrix.shape[0] for d in dist]
    fig = plt.figure()
    axes_x = fig.add_subplot(111)
    axes_x.plot(range_k, avg_within_sum_of_squares, 'b*-')
    plt.grid(True)
    plt.xlabel('Number of clusters', fontsize=15)
    plt.ylabel('Average within-cluster sum of squares', fontsize=15)
    plt.title('Elbow for KMeans clustering', fontsize=18)
    plt.savefig(output_plot2, format='pdf')


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column, feature_count_end_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):int(
        feature_count_end_column)]
