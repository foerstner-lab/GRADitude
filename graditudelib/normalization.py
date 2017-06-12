import pandas as pd
import numpy as np


def main():
    table = read_table('../input/normalized_table_ERCC_without_pellet.csv')
    max_table = new_table_max(table)
    log2_table= new_table_log2(table)
    log10_table = new_table_log10(table)
    max_table.to_csv('normalized_by_max_value_without_pellet.csv', sep=',', header=True, index=None)
    log2_table.to_csv('normalized_by_log2_value_without_pellet.csv', sep=',', header=True, index=None)
    log10_table.to_csv('normalized_by_log10_value_without_pellet.csv', sep=',', header=True, index=None)


def read_table(file):
    table = pd.read_csv(file)
    return table


def new_table_max(table_read):
    read_countings_values_only = table_read[list(filter(lambda col: col.startswith("Grad_47"), table_read.columns))]
    row_max_values = read_countings_values_only.max(axis=1)
    normalized_values = read_countings_values_only.divide(row_max_values, axis=0)
    normalized_values.fillna(0, inplace=True)  #problem with the number 2082
    return normalized_values


def new_table_log2(table_read):
    pseudo_count = 1.0
    read_countings_values_only = table_read[list(filter(lambda col: col.startswith("Grad_47"), table_read.columns))]
    normalized_values = read_countings_values_only.applymap(lambda val: val + pseudo_count).applymap(np.log2)
    return normalized_values


def new_table_log10(table_read):
    pseudo_count = 1.0
    read_countings_values_only = table_read[list(filter(lambda col: col.startswith("Grad_47"), table_read.columns))]
    normalized_values = read_countings_values_only.applymap(lambda val: val + pseudo_count).applymap(np.log10)
    return normalized_values

main()
