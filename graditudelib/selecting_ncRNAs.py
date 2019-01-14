import pandas as pd


def selecting_specific_features(normalized_table, feature_count_start_column,
                                feature_count_end_column, features, output_file):
    normalized_table_df = pd.read_table(normalized_table)
    features_rows = finding_nc_rnas_rows(normalized_table_df, features)
    attribute_table = _extract_attributes(features_rows, feature_count_start_column)
    nc_rnas_table = _extract_value_specific_feature(features_rows, feature_count_start_column,
                                                    feature_count_end_column)
    pd.concat([attribute_table, nc_rnas_table],
              axis=1).to_csv(output_file, sep='\t', index=None)


def finding_nc_rnas_rows(normalized_table, features):
    return normalized_table.loc[normalized_table['Feature'].isin(features)]


def _extract_value_specific_feature(features_rows, feature_count_start_column, feature_count_end_column):
    return features_rows.iloc[:, feature_count_start_column:feature_count_end_column]


def _extract_attributes(features_rows,
                        feature_count_start_column):
    return features_rows.iloc[:, : int(feature_count_start_column)]
