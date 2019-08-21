import pandas as pd


def extract_columns(feature_count_table, name_columns, output_table):
    attribute_df = pd.read_csv(feature_count_table, sep='\t')
    at_dict = attribute_df.Attributes.apply(
        lambda attributes: dict([key_value_pair.split('=') for
                                 key_value_pair in attributes.split(';')]))
    for atr in name_columns:
        attribute_df[atr] = at_dict.apply(lambda at_dic:
                                          at_dic.get(atr))
    attribute_df.to_csv(output_table, index=None, sep='\t')

