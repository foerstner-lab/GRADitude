import pandas as pd
from scipy.stats.mstats import gmean
import numpy as np
import os

from config import OUTPUT_DIR, SIZE_FACTORS_DIR


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    alignment_table = pd.read_table('../data/read_alignment_stats.csv')
    create_a_new_table(alignment_table)
    csv_file = read_filtered_alignment_stats(OUTPUT_DIR + 'filtered_alignment_stats.csv')
    g_mean = geometric_mean_by_row(csv_file)
    normalized_table = divide_rows_by_geometric_mean(csv_file, g_mean)
    value = get_medians(normalized_table)
    print_to_csv(value)


def create_a_new_table(alignment_table):
    series = []
    for index, row in alignment_table.iterrows():
        selection = row['Libraries']
        if selection.startswith('ERCC') & ('No. of aligned reads' in selection):
            series.append(row)

    filtered_table = pd.DataFrame(series)
    filtered_table.to_csv(OUTPUT_DIR + 'filtered_alignment_stats.csv', index=None)
    return filtered_table


def read_filtered_alignment_stats(file):
    table = pd.read_csv(file, sep=',')
    table.drop(table.columns[[1, -1]], axis=1, inplace=True)  #without pellet
    #table.drop(table.columns[[1]], axis=1, inplace=True) #with_pellet
    return table


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


def print_to_csv(numbers):
    if not os.path.exists(SIZE_FACTORS_DIR):
        os.makedirs(SIZE_FACTORS_DIR)
    pd.Series.from_array(numbers.to_csv(SIZE_FACTORS_DIR + 'size_factor_ERCC_to_normalize_tables_without_pellet.csv', index=None, header=None))


main()
