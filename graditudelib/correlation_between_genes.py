import pandas as pd
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from scipy import stats


def correlation(
        feature_count_table, feature_count_start_column, output_file):
    feature_count_table_df = pd.read_table(feature_count_table, sep='\t')
    feature_count_table_df_value = _extract_value_matrix(feature_count_table_df, feature_count_start_column)
    feature_count_table_df_value.set_index(['Gene'], inplace=True)
    corr_hist(feature_count_table_df_value, output_file)
    #corr_heatmap(feature_count_table_df_value)


def _extract_value_matrix(feature_count_table_df,
                          feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):]


def corr_hist(feature_count_table_df_value, output_file):
    rho, p = stats.spearmanr(feature_count_table_df_value.values.T)
    rho_df = pd.DataFrame.from_records(rho)
    plt.hist(rho_df)
    plt.savefig(output_file)



