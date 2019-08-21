import pandas as pd
import itertools


def main():
    attribute_df = pd.read_csv("/home/silvia/work/GRADitude/data/gene_wise_quantifications_combined.csv", sep='\t')
    attribute_df['at_dic'] = attribute_df.Attributes.apply(
        lambda attributes: dict([key_value_pair.split('=') for
                                 key_value_pair in attributes.split(';')]))
    attribute_df['at_dic_keys'] = attribute_df['at_dic'].apply(
        lambda at_dic: list(at_dic.keys()))
    merged_attribute_list = list(itertools.chain.
                                 from_iterable(attribute_df
                                               ['at_dic_keys']))
    nonredundant_list = sorted(list(set(merged_attribute_list)))

    attributes = {}
    for atr in nonredundant_list:
        attributes[atr] = attribute_df['at_dic'].apply(lambda at_dic:
                                                       at_dic.get(atr))
    result = pd.DataFrame(attributes)

    return result


main()
