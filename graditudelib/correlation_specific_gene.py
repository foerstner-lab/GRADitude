import pandas as pd
from scipy.stats import spearmanr
from scipy.stats import pearsonr


def corr_specific_gene_vs_all(feature_count_table,
                              feature_count_start_column,
                              feature_count_end_column,
                              name_column_with_genes_name,
                              name, correlation, output_file):
    table_protein = pd.read_table(feature_count_table)
    matrix = _extract_value_matrix(table_protein,
                                   feature_count_start_column,
                                   feature_count_end_column)
    gene_column = _exctract_gene_column(table_protein,
                                        name_column_with_genes_name)
    table_with_genes = pd.concat([gene_column, matrix], axis=1)
    table_with_genes_new_index = \
        table_with_genes.set_index(name_column_with_genes_name)
    gene_row_specific_gene = \
        _extract_gene_row(table_with_genes_new_index, name)
    if correlation == "Spearman":
        spearman_correlation(gene_row_specific_gene,
                             table_with_genes_new_index, output_file)
    else:
        pearson_correlation(gene_row_specific_gene,
                            table_with_genes_new_index, output_file)


def _extract_gene_row(feature_count_table_df, gene_name):
    return feature_count_table_df.loc[feature_count_table_df.index == gene_name]


def _extract_value_matrix(feature_count_table_df, feature_count_start_column,
                          feature_count_end_column):
    return feature_count_table_df.iloc[:,
                                       feature_count_start_column:feature_count_end_column]


def _exctract_gene_column(feature_count_table_df, name_column_with_genes_name):
    return feature_count_table_df[[name_column_with_genes_name]]


def pearson_correlation(gene_row_specific_gene, table_with_genes_new_index, output_file):
    rho_list = []
    p_value_list = []
    for index_gene, row_gene in table_with_genes_new_index.iterrows():
        rho = pearsonr(gene_row_specific_gene.iloc[0], row_gene)[0]
        rho_list.append(rho)
        p_value = pearsonr(gene_row_specific_gene.iloc[0], row_gene)[1]
        p_value_list.append(p_value)
    table_with_genes_new = table_with_genes_new_index.reset_index()
    rho_df = pd.DataFrame(rho_list)
    p_df = pd.DataFrame(p_value_list)
    table_with_rho_and_pvalue = pd.concat([table_with_genes_new, rho_df, p_df], axis=1)
    table_with_rho_and_pvalue.columns.values[[-2, -1]] = ['Pearson_coefficient', 'p_value']
    table_with_rho_and_pvalue.to_csv(output_file, sep='\t', index=None)


def spearman_correlation(gene_row_specific_gene, table_with_genes_new_index, output_file):
    rho_list = []
    p_value_list = []
    for index_gene, row_gene in table_with_genes_new_index.iterrows():
        rho = spearmanr(gene_row_specific_gene.iloc[0], row_gene)[0]
        rho_list.append(rho)
        p_value = spearmanr(gene_row_specific_gene.iloc[0], row_gene)[1]
        p_value_list.append(p_value)
    table_with_genes_new = table_with_genes_new_index.reset_index()
    rho_df = pd.DataFrame(rho_list)
    p_df = pd.DataFrame(p_value_list)
    table_with_rho_and_pvalue = pd.concat([table_with_genes_new, rho_df, p_df], axis=1)
    table_with_rho_and_pvalue.columns.values[[-2, -1]] = ['Spearman_coefficient', 'p_value']
    table_with_rho_and_pvalue.to_csv(output_file, sep='\t', index=None)
