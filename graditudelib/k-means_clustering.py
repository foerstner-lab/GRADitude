import pandas as pd
from sklearn.cluster import KMeans
import argparse
import config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--normalized_table", required=True)
    args = parser.parse_args()
    normalized_table = pd.read_csv(args.normalized_table, sep='\t')
    grad_rows = normalized_table[list(filter(lambda col: col.startswith("Grad"), normalized_table.columns))]
    attribute_rows = normalized_table[list(filter(lambda col: "Grad" not in col, normalized_table.columns))]
    clustering = k_means_clustering(grad_rows)
    final_table_with_clusters = pd.concat([attribute_rows, clustering], axis=1)
    final_table_with_clusters.to_csv(config.NORMALIZED_TABLE + 'normalized_table_with_clusters', sep='\t')


def k_means_clustering(table):
    mat = table.as_matrix()
    k_means = KMeans(n_clusters=7, random_state=0)
    k_means.fit(table)
    labels = k_means.labels_
    results = pd.DataFrame(data=labels, columns=['cluster'])
    table["Cluster_label"] = pd.Series(k_means.labels_).astype(int)
    return table


main()