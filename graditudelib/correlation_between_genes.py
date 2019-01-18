import pandas as pd
from scipy import stats


def correlation(
        feature_count_table, feature_count_start_column, feature_count_end_column,
        correlation_type,
        output_table):
    feature_count_table_df = pd.read_table(feature_count_table, sep='\t')
    feature_count_table_df.set_index(['Gene'], inplace=True)
    feature_count_table_df_value = _extract_value_matrix(feature_count_table_df,
                                                         feature_count_start_column,
                                                         feature_count_end_column)
    if correlation_type == "Spearman":
        corr_hist_spearman(feature_count_table_df_value, output_table)
    else:
        corr_hist_pearson(feature_count_table_df_value, output_table)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column, feature_count_end_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):feature_count_end_column]


def corr_hist_spearman(feature_count_table_df_value, output_table):
    rho = stats.spearmanr(feature_count_table_df_value.values.T)[0]
    rho_df = pd.DataFrame(rho, columns=feature_count_table_df_value.index,
                          index=feature_count_table_df_value.index)
    rho_df.to_csv(output_table, sep="\t")


def corr_hist_pearson(feature_count_table_df_value, output_table):
    rho = stats.spearmanr(feature_count_table_df_value.values.T)
    rho_df = pd.DataFrame.from_records(rho, columns=feature_count_table_df_value.index,
                                       index=feature_count_table_df_value.index)

    rho_df.to_csv(output_table, sep="\t")
