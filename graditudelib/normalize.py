#!/usr/bin/env python

import pandas as pd


def normalize(args):
    print(args.feature_counting_table)
    feature_counting_table = pd.read_table(args.feature_counting_table)
    feature_spiked_in_counting_table = pd.read_table(args.feature_spiked_in_counting_table)
    feature_minimal_counting_feature_table = pd.read_table(args.feature_minimal_counting_feature_table)
    return feature_counting_table, feature_spiked_in_counting_table, feature_minimal_counting_feature_table
