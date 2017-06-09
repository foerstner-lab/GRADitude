import pandas as pd
from config import OUTPUT_DIR, SIZE_FACTORS_DIR, NORMALIZED_TABLE, INPUT_DIR


def main():
    table = read_table(INPUT_DIR + '')
    normalized_table = new_table(table)
    normalized_table.to_csv('normalized_by_max_value_without_pellet.csv', sep=',', header=True, index=None)


def read_table(file):
    table = pd.read_excel(file)
    return table


def new_table(table_read):

    rows = []
    for i, row in table_read.iloc[:, 11:].iterrows():
        res = divide_by_max(row)
        rows.append(res)

    computed_df = pd.concat(rows, axis=1).transpose()

    cols = []
    for col in table_read.iloc[:, 0:11]:
        cols.append(table_read[col])
    for col in computed_df:
        cols.append(computed_df[col])

    return pd.concat(cols, axis=1)


def divide_by_max(row):
    max_val = 0
    for item in row:
        if item > max_val:
            max_val = item

    return row / max_val


main()
