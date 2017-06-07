import pandas as pd

input_dir = 'input'


def main():
    alignment_table = pd.read_table(input_dir + '/read_alignment_stats.csv')
    filtered_table = create_a_new_table(alignment_table)
    filtered_table.to_csv(input_dir + '/filtered_alignment_stats.csv', index=None)


def create_a_new_table(alignment_table):
    series = []
    for index, row in alignment_table.iterrows():
        selection = row['Libraries']
        if selection.startswith('ERCC') & ('No. of aligned reads' in selection):
            series.append(row)

    filtered_table = pd.DataFrame(series)
    return filtered_table

main()
