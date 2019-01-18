import pandas as pd
import scipy.stats.mstats


def normalized_count_table(
        feature_count_table,
        feature_count_start_column,
        feature_count_end_column,
        ref_feature_count_table,
        ref_feature_count_start_column,
        ref_feature_count_end_column,
        normalized_table,
        size_factor_table):
    ref_feature_count_table_df = pd.read_table(ref_feature_count_table, sep='\t')
    feature_count_table_df = pd.read_table(feature_count_table)
    size_factors = _calc_size_factors(ref_feature_count_table_df,
                                      ref_feature_count_start_column, ref_feature_count_end_column)
    normalized_table_df = _normalize_by_size_factor(feature_count_table_df,
                                                    feature_count_start_column,
                                                    feature_count_end_column, size_factors)
    normalized_table_df.to_csv(normalized_table, sep='\t', index=None)
    size_factors.to_csv(size_factor_table, sep='\t', header=['size_factors'])


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column, feature_count_end_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):feature_count_end_column]


def _calc_size_factors(ref_feature_count_table_df,
                       ref_feature_count_start_column, ref_feature_count_end_column):
    # TODO: Documentation the calculation with formula
    counting_value_matrix = _extract_value_matrix(
        ref_feature_count_table_df, ref_feature_count_start_column,
        int(ref_feature_count_end_column))
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
    g_mean = scipy.stats.mstats.gmean(counting_value_matrix, axis=1)
    return g_mean


def _normalize_by_size_factor(feature_counting_table_df,
                              feature_count_start_column,
                              feature_count_end_column, size_factor):
    df = feature_counting_table_df.copy()
    value_columns = df.iloc[:, int(feature_count_start_column
                                   ):int(feature_count_end_column)].columns
    """Divide the gene quantification table for the size factor to normalize the data"""
    df[value_columns] = df[value_columns].divide(list(size_factor), axis=1)
    return df
