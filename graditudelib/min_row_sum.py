import pandas as pd


def exclude_the_min_row_sum(feature_count_table,
                            feature_count_start_column, feature_count_end_column, min_row, output_file):
    feature_count_table_df = pd.read_table(feature_count_table)
    matrix_value = _extract_value_matrix(feature_count_table_df,
                                         feature_count_start_column, feature_count_end_column)
    colum_with_gene_name = _extract_gene_matrix(feature_count_table_df)
    attribute_matrix = _extract_attributes(feature_count_table_df, feature_count_start_column)
    min_row_sum(matrix_value, attribute_matrix, colum_with_gene_name, min_row, output_file)


def _extract_value_matrix(feature_count_table_df, feature_count_start_column,
                          feature_count_end_column):
    return feature_count_table_df.iloc[:, feature_count_start_column:(
        feature_count_end_column)]


def _extract_gene_matrix(feature_count_table_df):
    gene_column = feature_count_table_df[list(filter(
        lambda col: col.startswith("Attributes"), feature_count_table_df.columns))]
    return gene_column


def _extract_attributes(feature_count_table_df,
                        feature_count_start_column):
    return feature_count_table_df.iloc[:, : feature_count_start_column]


def min_row_sum(value_matrix, attribute_matrix, gene_column, min_row, output_file):
    gene_table_final = []
    combined_df_ext = pd.concat([attribute_matrix, value_matrix], axis=1)
    summed_values = value_matrix.sum(axis=1)
    combined_df = pd.concat([gene_column, summed_values], axis=1)
    combined_df.columns = ['Attributes', 'sum_of_values']
    selected_df = combined_df[~(combined_df['sum_of_values'] <= min_row)]
    selected_df.reset_index(drop=True, inplace=True)
    my_keys = selected_df['Attributes'].tolist()
    for index, row in combined_df_ext.iterrows():
        gene = row["Attributes"]
        if gene in my_keys:
            gene_table_final.append(row)
    df_with_min_row_samples = pd.DataFrame(gene_table_final)
    df_with_min_row_samples.reset_index(drop=True, inplace=True)
    df_with_min_row_samples.to_csv(output_file, sep='\t', index=0)
