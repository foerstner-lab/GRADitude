import pandas as pd
import scipy.stats.mstats


def normalized_count_table(
        feature_count_table,
        feature_count_start_column,
        ref_feature_count_table,
        ref_feature_count_start_column,
        normalized_table,
        size_factor_table):
    ref_feature_count_table_df = pd.read_table(ref_feature_count_table, sep=',')
    feature_count_table_df = pd.read_table(feature_count_table)
    size_factors = _calc_size_factors(ref_feature_count_table_df,
                                      ref_feature_count_start_column)

    _get_normalized_table(feature_count_table_df,
                          feature_count_start_column,
                          size_factors).to_csv(normalized_table, sep='\t', index=None)
    size_factors.to_csv(size_factor_table, sep='\t', header=['size_factors'])


def _extract_value_matrix(ref_feature_count_table_df,
                          ref_feature_count_start_column):
    return ref_feature_count_table_df.iloc[:, ref_feature_count_start_column:]


def _calc_size_factors(ref_feature_count_table_df,
                       ref_feature_count_start_column):

    # TODO: Documentation the calculation with formula
    counting_value_matrix = _extract_value_matrix(
        ref_feature_count_table_df, ref_feature_count_start_column)
    geometric_means = _geometric_means(counting_value_matrix)
    scaled_counting_value_matrix = _multiply_geometric_means_with_value_matrix(
        counting_value_matrix, geometric_means)
    return scaled_counting_value_matrix.median(axis=0)


def _multiply_geometric_means_with_value_matrix(counting_value_matrix,
                                                geometric_means):
    """Before the multiplication remove rows where the geometric mean is 0"""
    nonzero = geometric_means != 0.0
    nonzero_geometric_mean = geometric_means[nonzero]
    nonzero_counting_value_matrix = counting_value_matrix[nonzero]
    return nonzero_counting_value_matrix.divide(nonzero_geometric_mean, axis=0)


def _geometric_means(counting_value_matrix):
    return scipy.stats.mstats.gmean(counting_value_matrix, axis=1)


def _get_normalized_table(feature_counting_table_df,
                          feature_count_start_column, size_factor):
    counting_value_matrix = _extract_value_matrix(feature_counting_table_df,
                                                  feature_count_start_column)
    return counting_value_matrix.divide(size_factor)
