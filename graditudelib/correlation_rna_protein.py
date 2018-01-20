import pandas as pd
from scipy import stats


def rna_protein_correlation(feature_count_table, feature_count_start_column, feature_count_end_column, protein_table,
                            protein_count_start_column, protein_count_end_column,
                            output_file):
    sequencing_table = pd.read_table(feature_count_table)
    protein_table = pd.read_table(protein_table)
    sequencing_table.set_index('Gene', inplace=True)
    protein_table.set_index('Protein.IDs', inplace=True)
    value_matrix_sequencing = _extract_value_matrix(sequencing_table, feature_count_start_column,
                                                    feature_count_end_column)
    value_matrix_protein = _extract_value_matrix(protein_table, protein_count_start_column, protein_count_end_column)
    correlation(value_matrix_sequencing, value_matrix_protein, output_file)


def _extract_value_matrix(feature_count_table_df, feature_count_start_column, feature_count_end_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column):int(feature_count_end_column)]


def correlation(value_matrix_sequencing, value_matrix_protein, output_file):
    correlation_dataframe = pd.DataFrame(0, columns=value_matrix_sequencing.index, index=value_matrix_protein.index)
    # i = 0
    for index_gene, row_gene in value_matrix_sequencing.iterrows():
        # i = i + 1
        # print(str(i) + ": " + index_gene)
        # if i == 2:
        #     break
        for index_protein, row_protein in value_matrix_protein.iterrows():
            rho = stats.spearmanr(row_gene, row_protein)[0]
            correlation_dataframe.loc[index_protein, index_gene] = rho
            # print(correlation_dataframe.loc[index_protein, index_gene])

    correlation_dataframe.to_csv(output_file, sep='\t')
