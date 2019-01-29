import pandas as pd
import numpy as np


def scaling_(feature_count_table, feature_count_start_column, feature_count_end_column,
             pseudo_count, scaling_method, output_file):
    feature_count_table_df = pd.read_table(feature_count_table)
    value_matrix = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column, feature_count_end_column)
    attribute_matrix = _extract_attributes(feature_count_table_df,
                                           feature_count_start_column)
    normalized_table = normalize_values(value_matrix, scaling_method, pseudo_count)
    pd.concat([attribute_matrix, normalized_table],
              axis=1).to_csv(output_file, sep='\t', index=0)


def _extract_value_matrix(feature_count_table_df, feature_count_start_column,
                          feature_count_end_column):
    return feature_count_table_df.iloc[:, feature_count_start_column:(
        feature_count_end_column)]


def _extract_attributes(feature_count_table_df,
                        feature_count_start_column):
    return feature_count_table_df.iloc[:, : feature_count_start_column]


def normalize_values(values_matrix, scaling_method, pseudo_count):
    if scaling_method == "no_normalization":
        normalized_values = values_matrix
    elif scaling_method == "log2":
        normalized_values = values_matrix.applymap(
            lambda val: val + pseudo_count).applymap(np.log2)
    elif scaling_method == "log10":
        normalized_values = values_matrix.applymap(
            lambda val: val + pseudo_count).applymap(np.log10)
    elif scaling_method == "to_max":
        values_matrix = values_matrix.fillna(lambda x: 0)
        row_max_values = values_matrix.max(axis=1)
        normalized_values = values_matrix.divide(
            row_max_values, axis=0)
        normalized_values = pd.DataFrame(normalized_values).fillna(0)
    elif scaling_method == "to_range":
        row_max_values = values_matrix.max(axis=1)
        row_min_values = values_matrix.min(axis=1)
        normalized_values = values_matrix.subtract(
            row_min_values, axis=0).divide(row_max_values, axis=0)
    else:
        print("Normalization method not known")
    return normalized_values
