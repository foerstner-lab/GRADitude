import pandas as pd
from graditudelib import normalize

def _generate_data_frame():
    return pd.DataFrame(
        {'desc': ["X", "Y", "Z"],
         'A': [1, 2, 3],
         'B': [4, 5, 6],
         'C': [8, 1, 3]},
        index=list('abc'))[["desc", "A", "B", "C"]]

def test_extract_value_matrix():
    pd.util.testing.assert_frame_equal(
        normalize._extract_value_matrix(_generate_data_frame(), 1),
        pd.DataFrame(
            {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [8, 1, 3]},
            index=list('abc'))[["A", "B", "C"]])

"""
def test_calc_geometric_means():
    assert normalize._calc_geometric_means(_generate_data_frame()) == [0, 4, 6]

def test_calc_size_factors():
    assert normalize._calc_size_factors(_generate_data_frame(), 0) == [2, 3, 4]
"""
