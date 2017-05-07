import argparse
from graditudelib import normalize


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", "-v", action="store_true", help="show version")
    subparsers = parser.add_subparsers(help="commands")

    normalize_parser = subparsers.add_parser("normalize")
    normalize_parser.set_defaults(func=normalize_table)
    normalize_parser.add_argument("--feature_counting_table", required=True)
    normalize_parser.add_argument("--spike_in_counting_table", required=True)
    normalize_parser.add_argument("--minimal_counting_feature", type=int)

    """    
    counting_table_parser = subparsers.add_parser("--spike-in-counting-table", "-s")
    
    counting_table_parser.add_argument("--feature_counting_table", help='parse the counting table')
    

    spike_in_counting_table = subparsers.add_parser('spiked_in_counting_table')
    spike_in_counting_table.add_argument("--feature_spiked_in_counting_table")
    spike_in_counting_table.set_defaults(func=spiked_in_table_parser)

    minimal_counting_feature = subparsers.add_parser('minimal_counting_feature')
    minimal_counting_feature.add_argument("--feature_minimal_counting_table", help='parse the minimal counting table')
    minimal_counting_feature.set_defaults(func=minimal_table_parser)

    minimal_counting_spiked_in = subparsers.add_parser('minimal_counting_spiked_in')
    minimal_counting_spiked_in.add_argument("--feature_minimal_counting_spiked_in_table")
    minimal_counting_spiked_in.set_defaults(func=minimal_spike_in_table_parser)
    """
    args = parser.parse_args()
    if "func" in dir(args):
        args.func(args)


def normalize_table(args):
    normalize.normalize(args.feature_counting_table)
    normalize.normalize(args.spike_in_counting_table)
    normalize.normalize(args.minimal_counting_feature)

"""
def table_parser(args):
    normalize.normalize(args)


def minimal_table_parser(args):
    normalize.normalize(args)


def spiked_in_table_parser(args):
    normalize.normalize(args)


def minimal_spike_in_table_parser(args):
    normalize.normalize(args)
"""

main()
