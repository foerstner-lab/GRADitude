import argparse
#from graditudelib import normalize


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", "-v", action="store_true", help="show version")
    subparsers = parser.add_subparsers(help="commands")

    counting_table_parser = subparsers.add_parser("counting-table")
    counting_table_parser.add_argument("--feature_counting_table", help='parse the counting table')
    counting_table_parser.set_defaults(func=table_parser)

    args = parser.parse_args()
    if "func" in dir(args):
        args.func(args)


def table_parser(args):
    # print(args)
    # print(args.feature_counting_table)
    #normalize.normalize(args)

main()
