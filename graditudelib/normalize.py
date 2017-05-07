#!/usr/bin/env python

import pandas as pd
from scipy.stats.mstats import gmean

# def normalize(args):
#     feature_counting_table = pd.read_table(args.feature_counting_table)
#     return feature_counting_table


def main():
    create_a_new_table('read_alignment_stats.csv')
    geometric_mean('filtered_alignment_stats.csv')


def create_a_new_table(files):
    series = []
    alignment_table = pd.read_table(files)
    for index, row in alignment_table.iterrows():
        selection = row['Libraries']
        if selection.startswith('ERCC') & ('No. of aligned reads' in selection):
            series.append(row)
    filtered_table = pd.DataFrame(series)
    filtered_table.to_csv('filtered_alignment_stats.csv', index =None)


def geometric_mean(table):
    table_new = pd.read_table(table, sep=",")
    table_new['g_mean'] = gmean(table_new.iloc[0:, 1:], axis=1)
    return table_new.to_csv('alignment_stats_with_g_mean.csv', index=None)


main()
