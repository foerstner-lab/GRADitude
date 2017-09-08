from graditudelib import normalize
from graditudelib import visualizing_kinetics
from graditudelib import k_means
from graditudelib import elbow_curve
from graditudelib import silhouette
from graditudelib import hierarchical_clustering
from graditudelib import DBSCAN_clustering
from graditudelib import Nearest_Neighbors
from graditudelib import pca_after_clustering
from graditudelib import tSNE


def test_run_normalize():
    normalize.normalized_count_table(
        "../data/gene_wise_quantifications_combined_extended_test.csv",
        13,
        "../data/filtered_alignment_stats.csv",
        1,
        "normalized_table.csv",
        "size_factor_table.csv",
    )


def test_run_visualizing_kinetics():
    visualizing_kinetics.plot_kinetics(
        "../data/gene_wise_quantifications_combined_extended_test.csv",
        'chiX',
        13,
        '.html')


def test_run_k_means_clustering():
    k_means.generate_k_means_clustering(
        "../data/gene_wise_quantifications_combined_extended_test.csv",
        12,
        7,
        'normalized_by_log10_with_clusters.csv',
        'log10',
        1)


def test_run_elbow_method():
    elbow_curve.k_means_clustering_elbow(
        "../data/gene_wise_quantifications_combined_extended_test.csv",
        13,
        2,
        10)


def test_run_silhouette_analysis():
    silhouette.silhouette_analysis(
        "../data/gene_wise_quantifications_combined_extended_test.csv",
        13,
        2,
        10)


def test_run_hierarchical_clustering():
    hierarchical_clustering.generate_hierarchical_clustering(
        "../data/gene_wise_quantifications_combined_extended_test.csv",
        12,
        7,
        'normalized_by_log10_with_clusters_hierarchical.csv',
        'log10',
        1)


def test_run_db_scan_clustering():
    DBSCAN_clustering.generate_dbscan_clustering("../data/gene_wise_quantifications_combined_extended_test.csv",
                                                 12,
                                                 'normalized_by_log10_with_clusters_DBSCAN.csv',
                                                 'log10',
                                                 1)


def test_run_nearest_neighbors():
    Nearest_Neighbors.generate_nearest_neighbors("../data/gene_wise_quantifications_combined_extended_test.csv",
                                                 12, )


def test_run_pca():
    pca_after_clustering.pca_analysis('../data/normalized_by_log10_with_clusters.csv',
                                      12,
                                      'pca_after_clustering.html')


def test_run_t_sne_analysis():
    tSNE.t_sne_analysis("../data/gene_wise_quantifications_combined_extended_test.csv",
                        12,
                        1,
                        'log10',
                        'no_cluster',
                        'test')


# test_run_normalize()
# test_run_visualizing_kinetics()
# test_run_k_means_clustering()
# test_run_elbow_method()
# test_run_silhouette_analysis()
# test_run_hierarchical_clustering()
# test_run_db_scan_clustering()
# test_run_nearest_neighbors()
#test_run_pca()
test_run_t_sne_analysis()
