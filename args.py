# -*- coding: utf-8 -*-

import argparse

def process_args():
    def percent_value(string):
        val = float(string)
        if 0.0 <= val <=1.0:
            return val
        else:
            raise argparse.ArgumentTypeError(u"{0} is not from the range of 0..1".format(string))

    def algorithm_name(string):
        if string.lower() not in ('apriori', 'dic'):
            raise argparse.ArgumentTypeError("uNo algorithm named {0} is known.".format(string))
        else:
            return string.lower()

    def dic_granularity(string):
        val = int(string)
        if val <= 0:
            raise argparse.ArgumentTypeError(u"DIC's granularity must be positive.")
        else:
            return val


    parser = argparse.ArgumentParser(
            description=u"Induction of associative rules from datasets.",
            epilog=u"For current version check 'http://github.com/KrzysztofUrban/associative_rules'."
        )
    parser.add_argument('infile',
            help=u"input file")
    parser.add_argument('outfile',
            nargs='?',
            help=u"output file"
        )
    parser.add_argument('-a, --algorithm',
            dest='algorithm',
            type=algorithm_name,
            default='dic',
            help=u"name of preferred algorithm - apriori or dic"
        )
    parser.add_argument('-c, --confidence',
            dest='minconf',
            type=percent_value,
            default=0.7,
            help=u"minimum confidence (0..1)"
        )
    parser.add_argument('-s, --support',
            dest="minsup",
            type=percent_value,
            default=0.4,
            help=u"minimum support (0..1)"
        )
    parser.add_argument('-m',
            dest="m",
            type=dic_granularity,
            default=100,
            help=u"DIC's granularity"
        )
    return parser.parse_args()
