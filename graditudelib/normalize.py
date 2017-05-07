#!/usr/bin/env python

import pandas as pd
from scipy.stats.mstats import gmean
import numpy as np



# def normalize(args):
#     feature_counting_table = pd.read_table(args.feature_counting_table)
#     return feature_counting_table


def main():
    alignment_table = pd.read_table('read_alignment_stats.csv')
    filtered_table = create_a_new_table(alignment_table)
    filtered_table.to_csv('filtered_alignment_stats.csv', index=None)

    g_mean = geometric_mean_by_row(filtered_table)

    normalized_table = divide_rows_by_geometric_mean(filtered_table, g_mean)

    get_medians(normalized_table)


def create_a_new_table(alignment_table):
    series = []
    for index, row in alignment_table.iterrows():
        selection = row['Libraries']
        if selection.startswith('ERCC') & ('No. of aligned reads' in selection):
            series.append(row)

    filtered_table = pd.DataFrame(series)
    return filtered_table


def geometric_mean_by_row(table):
    g_mean = gmean(table.iloc[0:, 1:], axis=1)
    return g_mean


def divide_rows_by_geometric_mean(table, g_mean):
    rows = []
    for index, row in table.reset_index(drop=True).iterrows():
        if g_mean[index] != 0:
            rows.append(row.multiply(1 / g_mean[index]))
        # else:
            # print("g_mean[index] == 0")
            # rows.append(row.multiply(g_mean[index]))

    return pd.DataFrame(rows)


def get_medians(table):
    for col_name in table.columns:
        index = table.columns.get_loc(col_name)
        if index == 0:
            continue

        column = table.iloc[0:, index]
        median_value = np.median(column)
        print(median_value)

main()
