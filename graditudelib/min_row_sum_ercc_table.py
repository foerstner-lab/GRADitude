import pandas as pd


def filtering_ercc_table(ref_feature_count_table, min_row_sum,
                         filtered_ref_feature_count_table):
    ref_feature_count_table_df = pd.read_table(ref_feature_count_table, sep='\t')
    table_filtered_ercc = create_a_new_table_filtered_ercc(ref_feature_count_table_df)
    colum_with_libraries = _extract_gene_matrix(table_filtered_ercc)
    table_filtered_min_row_sum = min_row_sum_ercc_table(table_filtered_ercc, colum_with_libraries,
                                                        min_row_sum)
    table_filtered_min_row_sum.to_csv(filtered_ref_feature_count_table, sep='\t', index=None)


def _extract_gene_matrix(feature_count_table_df):
    gene_column = feature_count_table_df[list(filter(
        lambda col: col.startswith("Libraries"), feature_count_table_df.columns))]
    return gene_column


def create_a_new_table_filtered_ercc(alignment_table):
    series = []
    for index, row in alignment_table.iterrows():
        selection = row['Libraries']
        if selection.startswith('ERCC') & ('No. of aligned reads' in selection):
            series.append(row)
    filtered_table = pd.DataFrame(series)
    return filtered_table


def min_row_sum_ercc_table(table_filtered_ercc, colum_with_libraries, min_row_sum):
    gene_table_final = []
    summed_values = table_filtered_ercc.sum(axis=1)
    combined_df = pd.concat([colum_with_libraries, summed_values], axis=1)
    combined_df.columns = ['Gene', 'sum_of_values']
    selected_df = combined_df[~(combined_df['sum_of_values'] <= min_row_sum)]
    selected_df.reset_index(drop=True, inplace=True)
    my_keys = selected_df['Gene'].tolist()
    for index, row in table_filtered_ercc.iterrows():
        gene = row["Libraries"]
        if gene in my_keys:
            gene_table_final.append(row)
    df_with_min_row_samples = pd.DataFrame(gene_table_final)
    df_with_min_row_samples.reset_index(drop=True, inplace=True)
    return df_with_min_row_samples
