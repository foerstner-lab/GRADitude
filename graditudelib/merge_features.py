import pandas as pd


def merge_features_(feature_count_table, output_file):
    feature_count_table_df = pd.read_table(feature_count_table, sep='\t')
    exctract_name_information(feature_count_table_df, output_file)


def exctract_name_information(feature_count_table_df, output_file):
    feature_count_table_df['Feature'].replace(['antisense_RNA', 'RNase_P_RNA', 'SRP_RNA', "tmRNA"],
                                              ['ncRNA', 'ncRNA', 'ncRNA', "ncRNA"], inplace=True)
    feature_count_table_df.to_csv(output_file, sep='\t', index=None)

