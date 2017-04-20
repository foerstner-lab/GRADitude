#!/usr/bin/env python

import pandas as pd


def normalize(args):
    print(args.feature_counting_table)
    table = pd.read_table(args.feature_counting_table)
    return table


