from graditudelib import config
import pandas as pd
from scipy.stats.mstats import gmean
import numpy as np
import os


def main(params):
    reference_read_counts = pd.read_table(params.reference_read_count_file)
    g_mean = geometric_mean_by_row(reference_read_counts)
    normalized_table = divide_rows_by_geometric_mean(csv_file, g_mean)
    value = get_medians(normalized_table)
    print_to_csv(value, 'size_factor_ERCC_to_normalize_tables_without_pellet.csv')
    sf_table = read_table_size_factor(config.SIZE_FACTORS_DIR +
                                      'size_factor_ERCC_to_normalize_tables_without_pellet.csv')
    read_counts = read_table_quanti(params.read_count_file)
    table = new_table_(sf_table, read_counts)
    table.to_csv(config.OUTPUT_DIR + 'normalized_table_ERCC_without_pellet.csv', index=0)


def geometric_mean_by_row(table):
    g_mean = gmean(table.iloc[0:, 1:], axis=1)
    return g_mean


def divide_rows_by_geometric_mean(table, g_mean):
    rows = []
    for index, row in table.reset_index(drop=True).iterrows():
        if g_mean[index] != 0:
            rows.append(row.multiply(1 / g_mean[index]))
    return pd.DataFrame(rows)


def get_medians(table):
    names = []
    values = []
    for col_name in table.columns:
        index = table.columns.get_loc(col_name)
        if index == 0:
            continue
        column = table.iloc[0:, index]
        median_value = np.median(column)
        names.append(col_name)
        values.append(median_value)

    return pd.concat([pd.Series(names), pd.Series(values)], axis=1)


def print_to_csv(numbers, output_file):
    if not os.path.exists(config.SIZE_FACTORS_DIR):
        os.makedirs(config.SIZE_FACTORS_DIR)
    pd.Series.from_array(numbers.to_csv(config.SIZE_FACTORS_DIR + output_file, index=None, header=None))


def read_table_size_factor(table):
    file = pd.read_table(table, sep=',')
    file.columns = ['Samples', 'Size_factors']
    return file


def read_table_quanti(table2):
    file2 = pd.read_table(table2, sep='\t')
    return file2


def new_table_(first, second):
    cols = []
    for i, row in first.iterrows():
        name = row["Samples"]
        value = row["Size_factors"]

        col = second[name] / value
        cols.append(col)

    return pd.concat(cols, axis=1)


# main()
