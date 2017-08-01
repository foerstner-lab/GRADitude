from scipy.spatial.distance import cdist, pdist
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from config import OUTPUT_DIR


def main():
    table = read_table(OUTPUT_DIR + 'normalized_table_ERCC_without_pellet.csv')
    elbow(table)


def read_table(file):
    normalized_table = pd.read_csv(file, sep=',')
    new_table = normalized_table.drop(normalized_table.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -2, -1]], axis=1)
    return new_table


def elbow(d_frame):
    range_k = range(2, 10)
    k_m = [KMeans(n_clusters=k).fit(d_frame) for k in range_k]
    centroids = [k.cluster_centers_ for k in k_m]
    d_k = [cdist(d_frame, cent, 'euclidean') for cent in centroids]
    c_idx = [np.argmin(D, axis=1) for D in d_k]
    dist = [np.min(D, axis=1) for D in d_k]
    avg_within_sum_of_squares = [sum(d)/d_frame.shape[0] for d in dist]
    w_css = [sum(d**2) for d in dist]
    tss = sum(pdist(d_frame)**2)/d_frame.shape[0]
    bss = tss - w_css
    k_idx = 10-1
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range_k, avg_within_sum_of_squares, 'b*-')
    plt.grid(True)
    plt.xlabel('Number of clusters')
    plt.ylabel('Average within-cluster sum of squares')
    plt.title('Elbow for KMeans clustering')
    plt.savefig('elbow_for_kmeans_clustering.png')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range_k, bss/tss*100, 'b*-')
    plt.grid(True)
    plt.xlabel('Number of clusters')
    plt.ylabel('Percentage of variance explained')
    plt.title('Elbow for KMeans clustering')
    plt.savefig('elbow_for_kmeans_clustering2.png')


main()
