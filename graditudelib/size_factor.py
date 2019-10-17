import pandas as pd


def size_factor_extraction(ref_feature_count_table, size_factor_table):
    table = pd.read_table(ref_feature_count_table, sep='\t')
    filtered_table = create_a_new_table_filtered_ercc(table).transpose()
    filtered_table.to_csv(size_factor_table, sep='\t')


def create_a_new_table_filtered_ercc(alignment_table):
    series = []
    for index, row in alignment_table.iterrows():
        selection = row['Libraries']
        if selection.startswith('spike_1') & ('No. of aligned reads' in selection):
            series.append(row)

    filtered_table = pd.DataFrame(series)
    values_matrix = filtered_table.fillna(lambda x: 0)
    row_max_values = int(values_matrix.max(axis=1))
    values_matrix_index = values_matrix.set_index('Libraries')
    normalized_values = values_matrix_index.divide(
        row_max_values, axis=0)
    return normalized_values
