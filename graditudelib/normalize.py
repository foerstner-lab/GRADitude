import pandas as pd
from scipy.stats.mstats import gmean
import numpy as np

input_dir = 'input'
output_dir = 'output'


def main():
    csv_file = read_filtered_alignment_stats(input_dir + '/filtered_alignment_stats.csv')
    #csv_file = read_filtered_alignment_stats('../input/filtered_alignment_stats.csv')
    g_mean = geometric_mean_by_row(csv_file)
    normalized_table = divide_rows_by_geometric_mean(csv_file, g_mean)
    value = get_medians(normalized_table)
    print_to_csv(value)


def read_filtered_alignment_stats(file):
    table = pd.read_csv(file, sep=',')
    table.drop(table.columns[[1, -1]], axis=1, inplace=True)
    return table


def geometric_mean_by_row(table):
    g_mean = gmean(table.iloc[0:, 1:], axis=1)
    return g_mean


def divide_rows_by_geometric_mean(table, g_mean):
    rows = []
    for index, row in table.reset_index(drop=True).iterrows():
        if g_mean[index] != 0:
            rows.append(row.multiply(1 / g_mean[index]))
            # else:
            #     print("g_mean[index] == 0")
            #     rows.append(row.multiply(g_mean[index]))
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
    pd.Series.from_array(numbers.to_csv(output_dir + '/size_factor_ERCC_to_normalize_tables.csv', index=None, header=None))
    #pd.Series.from_array(numbers.to_csv('../output/size_factor_ERCC_to_normalize_tables.csv', index=None, header=None))


main()
