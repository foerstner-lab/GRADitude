import pandas as pd
import numpy as np


def merge_exctracted_attributes(feature_count_table, output_table):
    table = pd.read_csv(feature_count_table, sep='\t')
    table['Parent'] = np.where(table['Parent'].isnull(), table['name'], table['Parent'])
    table['Parent'] = np.where(table['Parent'].isnull(), table['ID'], table['Parent'])
    table.rename(columns={'Parent': 'Gene'}, inplace=True)
    table.to_csv(output_table, index=None, sep='\t')

