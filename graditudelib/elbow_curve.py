from scipy.spatial.distance import cdist, pdist
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import config
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--normalized_table", required=True)
    args = parser.parse_args()
    normalized_table = pd.read_csv(args.normalized_table, sep='\t')
    grad_rows = normalized_table[list(filter(lambda col: col.startswith("Grad"), normalized_table.columns))]
    attribute_rows = normalized_table[list(filter(lambda col: "Grad" not in col, normalized_table.columns))]
    elbow(grad_rows)


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
