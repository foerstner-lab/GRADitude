import pandas as pd


def exclude_the_min_row_sum(feature_count_table,
                            feature_count_start_column, min_row, output_file):
    feature_count_table_df = pd.read_table(feature_count_table)
    matrix_value_with_gene_name = _extract_value_matrix_with_gene_row(feature_count_table_df,
                                                                      feature_count_start_column)
    colum_with_gene_name = _extract_gene_matrix(feature_count_table_df)
    attribute_matrix = _extract_attributes(feature_count_table_df, feature_count_start_column)
    min_row_sum(matrix_value_with_gene_name, attribute_matrix,  colum_with_gene_name, min_row, output_file)


def _extract_value_matrix_with_gene_row(feature_count_table_df,
                                        feature_count_start_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):]


def _extract_gene_matrix(feature_count_table_df):
    gene_column = feature_count_table_df[list(filter(
        lambda col: col.startswith("Gene"), feature_count_table_df.columns))]
    return gene_column


def _extract_attributes(feature_count_table_df,
                        feature_count_start_column):
    return feature_count_table_df.iloc[:, : int(feature_count_start_column)-1]


def min_row_sum(value_matrix, attribute_matrix, gene_column, min_row, output_file):
    gene_table_final = []
    combined_df_ext = pd.concat([attribute_matrix, gene_column, value_matrix], axis=1)
    normalized_values = value_matrix.sum(axis=1)
    combined_df = pd.concat([gene_column, normalized_values], axis=1)
    combined_df.columns = ['Gene', 'sum_of_values']
    selected_df = combined_df[~(combined_df['sum_of_values'] <= min_row)]
    selected_df.reset_index(drop=True, inplace=True)
    my_keys = selected_df['Gene'].tolist()
    for index, row in combined_df_ext.iterrows():
        gene = row["Gene"]
        if gene in my_keys:
            gene_table_final.append(row)
    df_with_min_row_samples = pd.DataFrame(gene_table_final)
    df_with_min_row_samples.reset_index(drop=True, inplace=True)
    df_with_min_row_samples.to_csv(output_file, sep='\t', index= None)
