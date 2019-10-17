import pandas as pd


def normalized_count_table_spikein(feature_count_table, feature_count_start_column, feature_count_end_column,
                                   size_factors_table, normalized_table):
    feature_count_table_df = pd.read_csv(feature_count_table, sep='\t')
    size_factor_table_df = pd.read_csv(size_factors_table, sep='\t')
    normalized_table_df = _normalize_by_size_factor(feature_count_table_df, feature_count_start_column,
                                                    feature_count_end_column,
                                                    size_factor_table_df)
    normalized_table_df.to_csv(normalized_table, sep='\t', index=None)


def _normalize_by_size_factor(feature_counting_table_df,
                              feature_count_start_column, feature_count_end_column, size_factor_table):
    df = feature_counting_table_df.copy()
    value_columns = df.iloc[:, int(feature_count_start_column
                                   ):int(feature_count_end_column)].columns
    series_column = pd.Series(size_factor_table['spike_1_20bp - No. of aligned reads'].values)
    """Divide the gene quantification table for the size factor to normalize the data"""
    df[value_columns] = df[value_columns].divide(list(series_column), axis=1)
    return df
