import pandas as pd
import numpy as np
import pytest
import numpy.testing
import pandas.util.testing
from graditudelib import normalize


def _generate_data_frame():
    return pd.DataFrame(
        {'desc': ["X", "Y", "Z"],
         'A': [2, 2, 0],
         'B': [4, 6, 0],
         'C': [8, 3, 0],
         'D': [2, 1, 0]},
        index=list('abc'))[["desc", "A", "B", "C", "D"]]


def test_extract_value_matrix():
    pd.util.testing.assert_frame_equal(
        normalize._extract_value_matrix(_generate_data_frame(), 1),
        pd.DataFrame(
            {'A': [2, 2, 0], 'B': [4, 6, 0], 'C': [8, 3, 0], 'D': [2, 1, 0]},
            index=list('abc'))[["A", "B", "C", "D"]])


def test_geometric_means():
    numpy.testing.assert_array_almost_equal(
        normalize._geometric_means(
            _generate_data_frame()[["A", "B", "C", "D"]]),
        np.array([3.363586, 2.44949, 0]))


def test_multiply_geometric_means_with_value_matrix():
    pandas.util.testing.assert_frame_equal(
        normalize._multiply_geometric_means_with_value_matrix(
            _generate_data_frame()[["A", "B", "C", "D"]],
            np.array([3.363586, 2.44949, 0])),
        pd.DataFrame({'A': [0.594603, 0.816496], 'B': [1.189207, 2.449489],
                      'C': [2.378414, 1.224745], 'D': [0.594603, 0.408248]},
                     index=list('ab')))


def test_calc_size_factors():
    pd.util.testing.assert_series_equal(
        normalize._calc_size_factors(_generate_data_frame(), 1),
        pd.Series([0.7055495, 1.819348, 1.8015795, 0.5014255], index=list('ABCD')))


# def test_normalize_by_size_factor():
#     pandas.util.testing.assert_frame_equal(normalize._normalize_by_size_factor(_generate_data_frame(),
#                                                                                1,  pd.Series([1, 2, 3, 4])))



