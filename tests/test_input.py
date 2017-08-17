from graditudelib import normalize
from graditudelib import visualizing_kinetics
from graditudelib import k_means


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
        'normalized_by_max_value_with_clusters.csv',
        'log10',
        1)


#test_run_normalize()
#test_run_visualizing_kinetics()
test_run_k_means_clustering()
