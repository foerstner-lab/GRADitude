import pandas as pd
from config import OUTPUT_DIR, SIZE_FACTORS_DIR, NORMALIZED_TABLE, INPUT_DIR


def main():
    sf_table = read_table_size_factor(SIZE_FACTORS_DIR + 'size_factor_ERCC_to_normalize_tables_without_pellet.csv')
    q_table = read_table_quanti(INPUT_DIR + 'gene_wise_quantifications_combined_extended.csv')
    table = new_table_(sf_table, q_table)
    table.to_csv('normalized_table_ERCC_without_pellet.csv', index=0)
    # able.to_csv('normalized_table_ERCC_with_pellet.csv', index=0)


def read_table_size_factor(table):
    file = pd.read_table(table, sep=',')
    return file


def read_table_quanti(table2):
    file2 = pd.read_table(table2, sep='\t')
    return file2


def new_table_(first, second):
    cols = []
    for i, row in first.iterrows():
        name = row["Samples"]
        value = row["median"]

        col = second[name] / value
        cols.append(col)

    return pd.concat(cols, axis=1)


main()
