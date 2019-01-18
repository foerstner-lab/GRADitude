import pandas as pd


def dropping_column(feature_count_table, column_to_drop, output_file):
    feature_count_table_df = pd.read_table(feature_count_table)
    table_filtered_gene_quanti = create_gene_quanti_table_modified(feature_count_table_df,
                                                                   column_to_drop)
    table_filtered_gene_quanti.to_csv(output_file, sep='\t', index=None)


def create_gene_quanti_table_modified(gene_quanti_table, column_to_drop):
    cols = gene_quanti_table.columns.tolist()
    gene_quanti_table_with_gene_column_modified = gene_quanti_table[cols]
    gene_quanti_table_with_gene_column_modified.drop(column_to_drop, axis=1,
                                                     inplace=True)
    return gene_quanti_table_with_gene_column_modified
