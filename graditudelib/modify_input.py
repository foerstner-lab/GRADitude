import pandas as pd


def filtering_input(feature_count_table, column_to_drop, ref_feature_count_table,
                    filtered_feature_count_table, filtered_ref_feature_count_table):
    feature_count_table_df = pd.read_table(feature_count_table, sep='\t')
    table_filtered_gene_quanti = create_gene_quanti_table_modified(feature_count_table_df,
                                                                   column_to_drop)
    table_filtered_gene_quanti.to_csv('test.csv', sep='\t', index=None)
    ref_feature_count_table_df = pd.read_table(ref_feature_count_table, sep='\t')
    table_filtered_ercc = create_a_new_table_filtered_ercc(ref_feature_count_table_df)
    table_filtered_ercc.to_csv(filtered_ref_feature_count_table, sep='\t', index=None)
    table_filtered_gene_quanti.to_csv(filtered_feature_count_table, sep='\t', index=None)


def create_a_new_table_filtered_ercc(alignment_table):
    series = []
    for index, row in alignment_table.iterrows():
        selection = row['Libraries']
        if selection.startswith('ERCC') & ('No. of aligned reads' in selection):
            series.append(row)

    filtered_table = pd.DataFrame(series)
    return filtered_table


def create_gene_quanti_table_modified(gene_quanti_table, column_to_drop):
    cols = gene_quanti_table.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    gene_quanti_table_with_gene_column_modified = gene_quanti_table[cols]
    gene_without_column = gene_quanti_table_with_gene_column_modified.drop(column_to_drop, axis=1)
    return gene_without_column
