import pandas as pd
from scipy.stats import spearmanr
import numpy as np


def find_complexes(tables_containing_list_complexes, protein_table,
                   feature_count_start_column, feature_count_end_column,
                   output_table):
    tables_containing_list_complexes_df = pd.read_excel(tables_containing_list_complexes)
    protein_table_df = pd.read_csv(protein_table, sep='\t')
    selected_complexes = get_into_excel_complexes_table(tables_containing_list_complexes_df,
                                                        protein_table_df,
                                                        feature_count_start_column,
                                                        feature_count_end_column)
    table_with_selected_complexes = modifying_first_letter(selected_complexes)
    table_with_complete_complexes = correlation(table_with_selected_complexes, output_table)
    finding_number_of_complexes(table_with_complete_complexes)


def get_into_excel_complexes_table(tables_containing_list_complexes, protein_table,
                                   feature_count_start_column,
                                   feature_count_end_column):
    output_df = pd.DataFrame()
    for column_idx in tables_containing_list_complexes:
        col = tables_containing_list_complexes[column_idx].dropna()
        for row in range(0, col.size):
            complex_name = col.name
            gene_name = col[row]
            selected_df = protein_table.loc[protein_table['Gene.names'] == gene_name]
            selected_df = selected_df.iloc[:, int(feature_count_start_column): feature_count_end_column]

            cols = list(selected_df)
            if selected_df.empty:
                # print("empty")
                selected_df = pd.DataFrame().append({'complex_name': complex_name, "gene": gene_name}, ignore_index=True)
            else:
                selected_df['complex_name'] = complex_name
                selected_df['gene'] = gene_name
                cols = ['complex_name', 'gene'] + cols
                selected_df = selected_df.loc[:, cols]

            output_df = output_df.append(selected_df)
    return output_df


def modifying_first_letter(table_with_complexes):
    table_capitalized = table_with_complexes.gene.str.capitalize()
    table_capitalized_last = table_capitalized.apply(lambda s: (s[:1].upper() + s[1:-1] + s[-1:].upper())[:len(s)])
    table_capitalized_df = pd.Series.to_frame(table_capitalized_last)
    table_concat = pd.concat([table_capitalized_df, table_with_complexes], axis=1)
    return table_concat


def correlation(table_with_selected_complexes, output_table):
    table_dropped = table_with_selected_complexes.iloc[:, 1:-1]
    series_by_complex = {}
    for index, row in table_dropped.iterrows():
        complex_name = row['complex_name']
        if complex_name not in series_by_complex:
            series_by_complex[complex_name] = []

        series_by_complex[complex_name].append(row.drop('complex_name'))

    table_with_selected_complexes['rho_median'] = None
    table_with_selected_complexes['rho_mean'] = None
    table_with_selected_complexes['standard_deviation'] = None
    for key in series_by_complex.keys():
        series = series_by_complex[key]
        series_df = pd.DataFrame.from_records(series).dropna(axis=1)
        if series_df.empty:
            continue

        rho, pval = spearmanr_corrected(series_df, axis=1)
        standard_deviation = series_df.stack().std()
        rho_median = calculate_median_upper_triangle(rho)
        rho_mean = calculate_mean_upper_triaglie(rho)
        table_with_selected_complexes.loc[
            table_with_selected_complexes.complex_name == key,
            'rho_median'] = rho_median
        table_with_selected_complexes.loc[
            table_with_selected_complexes.complex_name == key,
            'rho_mean'] = rho_mean
        table_with_selected_complexes.loc[
            table_with_selected_complexes.complex_name == key,
            'standard_deviation'] = \
            standard_deviation

    table_with_complete_complexes = table_with_selected_complexes.dropna(
        subset=['rho_median'], how='all')
    table_with_complete_complexes.to_csv(
        output_table, sep='\t', index=None)
    return table_with_complete_complexes


def finding_number_of_complexes(table_with_selected_complexes):
    table_with_complexes_df_grouped = table_with_selected_complexes.groupby(
        'complex_name').agg(
        lambda x: set(x)).reset_index()
    print(len(table_with_complexes_df_grouped.index))


def calculate_median_upper_triangle(matrix):
    return np.median(matrix[np.triu_indices_from(matrix, 1)])


def calculate_mean_upper_triaglie(matrix):
    return np.mean(matrix[np.triu_indices_from(matrix, 1)])


def spearmanr_corrected(a, b=None, axis=0):
    rho, pval = spearmanr(a, b, axis=axis)

    # handle edge case where rho is not a matrix (len(series_df) == 2)
    if np.isscalar(rho):
        rho = np.array([[1, rho], [rho, 1]])

    return rho, pval
