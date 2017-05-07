#!/usr/bin/env python

import pandas as pd
from scipy.stats.mstats import gmean


# def normalize(args):
#     feature_counting_table = pd.read_table(args.feature_counting_table)
#     return feature_counting_table


def main():
    alignment_table = pd.read_table('read_alignment_stats.csv')
    filtered_table = create_a_new_table(alignment_table)
    filtered_table.to_csv('filtered_alignment_stats.csv', index=None)

    g_mean = geometric_mean_by_row(filtered_table)

    divide_rows_by_geometric_mean(filtered_table, g_mean)


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
    for index, row in table.reset_index(drop=True).iterrows():
        if g_mean[index] != 0:
            new_row = row.multiply(1 / g_mean[index])
        else:
            print("g_mean[index] == 0")

        # print(new_row)


main()
