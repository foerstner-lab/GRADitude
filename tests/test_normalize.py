import pandas as pd
from graditudelib import normalize
import numpy as np
import numpy.testing
import pandas.util.testing


# def _generate_data_frame():
#     return pd.DataFrame(
#         {'desc': ["X", "Y", "Z"],
#          'A': [2, 2, 0],
#          'B': [4, 6, 0],
#          'C': [8, 3, 0],
#          'D': [2, 1, 0]},
#         index=list('abc'))[["desc", "A", "B", "C", "D"]]
#
#
# def test_extract_value_matrix():
#     pd.util.testing.assert_frame_equal(
#         normalize._extract_value_matrix(_generate_data_frame(), 1),
#         pd.DataFrame(
#             {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [8, 1, 3], 'D': [2, 1, 6]},
#             index=list('abc'))[["A", "B", "C", "D"]])
#
#
# def test_geometric_means():
#     numpy.testing.assert_array_almost_equal(
#         normalize._geometric_means(
#             _generate_data_frame()[["A", "B", "C", "D"]]),
#         np.array([3.363586, 2.44949, 0]))
#
#
# def test_multiply_geometric_means_with_value_matrix():
#     pandas.util.testing.assert_frame_equal(
#         normalize._multiply_geometric_means_with_value_matrix(
#             _generate_data_frame()[["A", "B", "C", "D"]],
#             np.array([3.363586, 2.44949, 0])),
#         pd.DataFrame({'A': [0.594603, 0.816496], 'B': [1.189207, 2.449489],
#                       'C': [2.378414, 1.224745], 'D': [0.594603, 0.408248]},
#                      index=list('ab')))
#
#
# def test_calc_size_factors():
#     pd.util.testing.assert_series_equal(
#         normalize._calc_size_factors(_generate_data_frame(), 1),
#         pd.Series([0.891905336252, 1.02062072616], index=list('ab')))


def test_run_normalize():
    normalize.normalized_count_table(
        "../data/gene_wise_quantifications_combined_extended_test.csv",
        13,
        "../data/filtered_alignment_stats.csv",
        1,
        "normalized_table.csv",
        "size_factor_table.csv",
    )


test_run_normalize()

