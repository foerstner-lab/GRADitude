import pandas as pd
from sklearn.cluster import KMeans


def main():
    normalized_table = read_table('normalized_by_max_value_without_pellet.csv')
    k_means_clustering(normalized_table)


def read_table(file):
    table_ = pd.read_csv(file, sep=',')
    return table_


def k_means_clustering(table):
    mat = table.as_matrix()
    k_means = KMeans(n_clusters=6, random_state=0)
    k_means.fit(table)
    labels = k_means.labels_
    results = pd.DataFrame(data=labels, columns=['cluster'])
    table["Cluster_label"] = pd.Series(k_means.labels_).astype(int)
    table.to_csv('test.csv', index=0)


main()