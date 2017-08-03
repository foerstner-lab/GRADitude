import pandas as pd
import numpy as np
import argparse
import config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--normalized_table", required=True)
    args = parser.parse_args()
    normalized_table = pd.read_csv(args.normalized_table, sep='\t')
    grad_rows = normalized_table[list(filter(lambda col: col.startswith("Grad"), normalized_table.columns))]
    attribute_rows = normalized_table[list(filter(lambda col: "Grad" not in col, normalized_table.columns))]
    max_table = new_table_max(normalized_table)
    log2_table = new_table_log2(normalized_table)
    log10_table = new_table_log10(normalized_table)
    final_table_max = pd.concat([attribute_rows, max_table], axis=1)
    final_table_log2 = pd.concat([attribute_rows, log2_table], axis=1)
    final_table_log10 = pd.concat([attribute_rows, log10_table], axis=1)
    final_table_max.to_csv(config.NORMALIZED_TABLE + 'normalized_by_max_value.csv', sep='\t', header=True, index=None)
    final_table_log2.to_csv(config.NORMALIZED_TABLE + 'normalized_by_log2_value.csv', sep='\t', header=True, index=None)
    final_table_log10.to_csv(config.NORMALIZED_TABLE + 'normalized_by_log10_value.csv', sep='\t', header=True, index=None)


def new_table_max(table_read):
    read_countings_values_only = table_read[list(filter(lambda col: col.startswith("Grad"), table_read.columns))]
    row_max_values = read_countings_values_only.max(axis=1)
    normalized_values = read_countings_values_only.divide(row_max_values, axis=0)
    normalized_values.fillna(0, inplace=True)  #problem with the number 2082
    return normalized_values


def new_table_log2(table_read):
    pseudo_count = 1.0
    read_countings_values_only = table_read[list(filter(lambda col: col.startswith("Grad"), table_read.columns))]
    normalized_values = read_countings_values_only.applymap(lambda val: val + pseudo_count).applymap(np.log2)
    return normalized_values


def new_table_log10(table_read):
    pseudo_count = 1.0
    read_countings_values_only = table_read[list(filter(lambda col: col.startswith("Grad"), table_read.columns))]
    normalized_values = read_countings_values_only.applymap(lambda val: val + pseudo_count).applymap(np.log10)
    return normalized_values

main()
