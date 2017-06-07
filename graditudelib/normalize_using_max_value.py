import pandas as pd
import os


output_dir = "./output"
csvs_div_maximum = output_dir + '/csvs_div_maximum/'


def main():
    path = output_dir + "/csv_nb_vs_seq/"
    for (path, dirs, files) in os.walk(path):
        for file in files:
            table_read = read_table(os.path.join(path + file))
            new_table(table_read, file)


def read_table(file):
    table = pd.read_table(file, sep=',')
    return table


def new_table(table_read, name):
    result_table = pd.DataFrame()
    for col_name in table_read.columns:
        table_read.columns.get_loc(col_name)
        max_val = table_read[col_name].max()
        result_table[col_name] = table_read[col_name].apply(lambda x: x / max_val)

    return result_table.to_csv(csvs_div_maximum + name, sep=',', header=True, index=None)

main()
