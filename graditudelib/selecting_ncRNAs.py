import pandas as pd
import argparse


def selecting_specific_features(normalized_table, feature_count_start_column, features, output_file ):
    parser = argparse.ArgumentParser()
    parser.add_argument("--normalized_table", "-n")
    parser.add_argument("--feature_count_start_column", "-fc", type=int)
    parser.add_argument("--features", '-f',  nargs="+")
    parser.add_argument('--output_file', '-o')
    args = parser.parse_args()
    # normalized_table_df = pd.read_table(
    #     '/home/silvia/work/2017-05-15_Jens_E_Coli_grad_seq_analysis/2017-10-30-tSNE_only_ncRNAs/input/Normalized_with_pellet_gene_wise_quantifications_combined_extended_MIN_ROW_SUM_0.csv')
    normalized_table_df = pd.read_table(args.normalized_table)
    features_rows = finding_nc_rnas_rows(normalized_table_df)
    attribute_table = _extract_attributes(features_rows, args.feature_count_start_column)
    nc_rnas_table = _extract_value_specific_feature(features_rows, args.feature_count_start_column)
    pd.concat([attribute_table, nc_rnas_table],
              axis=1).to_csv(args.output_file, sep='\t', index=None)


def finding_nc_rnas_rows(normalized_table):
    return normalized_table.loc[normalized_table['Feature'] == 'ncRNA']


def _extract_value_specific_feature(features_rows, feature_count_start_column):
    return features_rows.iloc[:, feature_count_start_column:]


def _extract_attributes(features_rows,
                        feature_count_start_column):
    return features_rows.iloc[:, : int(feature_count_start_column)]


main()
