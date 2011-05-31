# -*- coding: utf-8 -*-

import argparse

from stats import is_posix

def process_args():
    def percent_value(string):
        val = float(string)
        if 0.0 <= val <=1.0:
            return val
        else:
            raise argparse.ArgumentTypeError("{0} is not from the range of 0..1".format(string))

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
    if is_posix():
        parser.add_argument('-p, --profile', 
                dest="display_stats",
                action='store_true', 
                help=u"display time and memory statistics"
            )
    return parser.parse_args()
