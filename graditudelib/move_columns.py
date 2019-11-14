import pandas as pd


def move_columns_(feature_count_table, number_of_columns, output_file):
    quanti_table = pd.read_csv(feature_count_table, sep='\t')
    table_column_inverted = create_gene_quanti_table_modified(quanti_table, number_of_columns)
    table_column_inverted.to_csv(output_file, sep='\t', index=None)


def create_gene_quanti_table_modified(gene_quanti_table, number_of_columns):
    cols = gene_quanti_table.columns.tolist()
    cols = cols[-number_of_columns:] + cols[:-number_of_columns]
    gene_quanti_table_with_gene_column_modified = gene_quanti_table[cols]
    return gene_quanti_table_with_gene_column_modified


