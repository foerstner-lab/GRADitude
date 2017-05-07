#!/usr/bin/env python

import pandas as pd
import os
import csv

# def normalize(args):
#     feature_counting_table = pd.read_table(args.feature_counting_table)
#     return feature_counting_table


def main():
    create_a_new_table('read_alignment_stats.csv')


def create_a_new_table(files):
    series = []
    alignment_table = pd.read_table(files)
    for index, row in alignment_table.iterrows():
        selection = row['Libraries']
        if selection.startswith('ERCC') & ('No. of aligned reads' in selection):
            series.append(row)
    filtered_table = pd.DataFrame(series)
    filtered_table.to_csv('filtered_alignment_stats.csv')

main()
