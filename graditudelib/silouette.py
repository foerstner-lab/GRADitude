
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import silhouette_score
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--normalized_table", required=True)
    args = parser.parse_args()
    normalized_table = pd.read_csv(args.normalized_table, sep='\t')
    read_countings_values_only = normalized_table[list(filter(
        lambda col: col.startswith("Grad"), normalized_table.columns))]
    silhouette(read_countings_values_only)


def silhouette(table):
    s = []
    for n_clusters in range(2, 10):
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(table)

        labels = kmeans.labels_
        centroids = kmeans.cluster_centers_

        s.append(silhouette_score(table, labels, metric='euclidean'))

    plt.plot(s)
    plt.ylabel("Silouette")
    plt.xlabel("k")
    plt.title("Silouette for K-means behaviour")
    plt.savefig('silouette.png')

main()
