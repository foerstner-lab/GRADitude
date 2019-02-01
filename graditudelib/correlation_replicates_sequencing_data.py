import pandas as pd
from scipy.stats import spearmanr
import matplotlib.pyplot as plt


def correlation_replicates_sd(table_replicate1, table_replicate2, table_start_column,
                              table_end_column, output_table,
                              output_figure):
    table_1r = pd.read_csv(table_replicate1, sep="\t")
    table_2r = pd.read_csv(table_replicate2, sep="\t")

    table_1r.set_index('Gene', inplace=True)
    table_1r.index = table_1r.index + '_' + table_1r.groupby(level=0).cumcount().astype(str)

    table_2r.set_index('Gene', inplace=True)
    table_2r.index = table_2r.index + '_' + table_2r.groupby(level=0).cumcount().astype(str)
    no_in_1 = table_2r[~table_2r.index.isin(table_1r.index)]
    index_no_in_1 = no_in_1.index
    table_2r.drop(index_no_in_1, inplace=True)

    value_matrix_table_1r = _extract_value_matrix(table_1r, table_start_column,
                                                  table_end_column)
    attribute_matrix_1r = attribute_matrix(table_1r, table_start_column)
    value_matrix_table_2r = _extract_value_matrix(table_2r, table_start_column,
                                                  table_end_column)
    concat_df = correlation(value_matrix_table_1r, value_matrix_table_2r)
    plot(concat_df, output_figure)
    pd.concat([attribute_matrix_1r, concat_df],
              axis=1).to_csv(output_table, sep='\t')


def _extract_value_matrix(feature_count_table_df, feature_count_start_column,
                          feature_count_end_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):int(
        feature_count_end_column)]


def attribute_matrix(feature_count_table_df, feature_count_start_column):
    return feature_count_table_df.iloc[:, : int(feature_count_start_column)]


def correlation(value_matrix_1r, value_matrix_2r):
    concat_dataframe = pd.DataFrame()
    for index_r1, row_r1 in value_matrix_1r.iterrows():
        row_r2 = value_matrix_2r.loc[index_r1]
        concat_row = pd.concat([row_r1, row_r2])
        rho = spearmanr(row_r1, row_r2, axis=None)[0]
        p_value = spearmanr(row_r1, row_r2, axis=None)[1]
        concat_row.at["rho"] = rho
        concat_row.at["pvalue"] = p_value
        concat_dataframe = concat_dataframe.append(concat_row)[concat_row.keys().tolist()]

    return concat_dataframe


def plot(concat_df, output_figure):
    plt.style.use('ggplot')
    fig = plt.figure()
    axes_x = fig.add_subplot(1, 1, 1)
    axes_x.set_xlim(concat_df["rho"].min(), 1)
    plt.hist(concat_df["rho"], bins=50)
    plt.title("Spearman correlation coefficient between replicates (RNA-Seq)",
              fontsize=13)
    plt.xlabel("Spearman correlation coefficient", fontsize=15)
    plt.ylabel("Occurance", fontsize=15)
    plt.savefig(output_figure)
