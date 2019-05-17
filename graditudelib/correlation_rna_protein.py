import pandas as pd
from scipy import stats


def rna_protein_correlation(feature_count_table, feature_count_start_column,
                            feature_count_end_column, protein_table,
                            protein_count_start_column, protein_count_end_column,
                            index_sequencing, index_protein,
                            correlation,
                            output_file):
    sequencing_table = pd.read_csv(feature_count_table, sep="\t")
    protein_table = pd.read_csv(protein_table, sep="\t")
    sequencing_table.set_index(index_sequencing, inplace=True)
    sequencing_table.index = \
        sequencing_table.index + '_' + sequencing_table.groupby(
            level=0).cumcount().astype(str)
    protein_table.set_index(index_protein, inplace=True)
    protein_table.index = \
        protein_table.index + '_' + protein_table.groupby(
            level=0).cumcount().astype(str)
    value_matrix_sequencing = _extract_value_matrix(sequencing_table, feature_count_start_column,
                                                    feature_count_end_column)
    value_matrix_protein = _extract_value_matrix(protein_table, protein_count_start_column,
                                                 protein_count_end_column)
    if correlation == "Spearman":
        correlation_spearman(value_matrix_sequencing, value_matrix_protein, output_file)
    else:
        correlation_pearson(value_matrix_sequencing, value_matrix_protein, output_file)


def _extract_value_matrix(feature_count_table_df, feature_count_start_column,
                          feature_count_end_column):
    return feature_count_table_df.iloc[:, int(feature_count_start_column) - 1:int(
        feature_count_end_column) - 1]


def correlation_spearman(value_matrix_sequencing, value_matrix_protein, output_file):
    correlation_dataframe = pd.DataFrame(0, columns=value_matrix_sequencing.index,
                                         index=value_matrix_protein.index)

    for index_gene, row_gene in value_matrix_sequencing.iterrows():

        for index_protein, row_protein in value_matrix_protein.iterrows():
            rho = stats.spearmanr(row_gene, row_protein)[0]
            correlation_dataframe.loc[index_protein, index_gene] = rho

    correlation_dataframe.to_csv(output_file, sep='\t', index_label="Gene")


def correlation_pearson(value_matrix_sequencing, value_matrix_protein, output_file):
    correlation_dataframe = pd.DataFrame(0, columns=value_matrix_sequencing.index,
                                         index=value_matrix_protein.index)

    for index_gene, row_gene in value_matrix_sequencing.iterrows():

        for index_protein, row_protein in value_matrix_protein.iterrows():
            rho = stats.pearsonr(row_gene, row_protein)[0]
            correlation_dataframe.loc[index_protein, index_gene] = rho

    correlation_dataframe.to_csv(output_file, sep='\t', index_label="Gene")
