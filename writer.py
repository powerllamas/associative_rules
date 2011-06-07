# -*- coding: utf-8 -*-

from collections import defaultdict
from string import Formatter

class Writer(object):
    __header_template = u"""
Algorithm:                  {algorithm}
Data set:                   {infile}
Minimum support:            {minsup}
Minimum confidence:         {minconf}
M:                          {m}
Number of rules:            {nr_of_rules}
Memory usage:               {memory_use}
Total time:                 {real_time}
User time:                  {user_time}
Large sets generation time: {set_gen_time}

**RULES
"""

    __rules_template = u"""
#{nr}: {antecedent} => {consequent}
Support:    {support}
Confidence: {confidence}
"""

    def __init__(self, filename=None):
        self.__filename = filename
        self.__data = defaultdict(lambda: u"<missing>")
        self.__rules = []

    def add_rules(self, rules):
        self.__rules = rules
        self.__data['nr_of_rules'] = len(rules)

    def add_stats(self, stats):
        self.__data['real_time'] = Writer.__parse_time(stats.real_time)
        self.__data['user_time'] = Writer.__parse_time(stats.user_time)
        self.__data['set_gen_time'] = Writer.__parse_time(stats.set_gen_time)
        self.__data['memory_use'] = Writer.__parse_memory(stats.memory_use)

    @staticmethod
    def __parse_memory(memory):
        return str(memory/(1024.0*1024.0)) + " Mb"

    @staticmethod
    def __parse_time(time):
        return str(time) + " s"

    def add_args(self, args):
        self.__data['infile'] = args.infile
        self.__data['minsup'] = args.minsup
        self.__data['minconf'] = args.minconf
        self.__data['algorithm'] = args.algorithm
        if args.algorithm == 'dic':
            self.__data['m'] = args.m

    def write(self):
        header = Writer.dictformat(self.__header_template, self.__data)
        if self.__filename is not None:
            with open(self.__filename, 'w') as file:
                file.write(header)
                if not self.__rules:
                    file.write(u"<empty>")
                else:
                    for nr, rule in enumerate(self.__rules, start=1):
                        rule_string = Writer.__format_rule(nr, rule)
                        file.write(rule_string)
        else:
            print header,
            if not self.__rules:
                print u"<empty>",
            else:
                for nr, rule in enumerate(self.__rules, start=1):
                    rule_string = Writer.__format_rule(nr, rule)
                    print rule_string,

    @staticmethod
    def dictformat(string, dictionary):
        formatter = Formatter()
        return formatter.vformat(string, (), dictionary)

    @staticmethod
    def __format_rule(nr, rule):
        data = defaultdict(lambda: u"<missing>")
        antecedent, consequent, support, confidence = rule
        data['nr'] = nr
        data['antecedent'] = " AND ".join(str(x) for x in antecedent)
        data['consequent'] = " AND ".join(str(x) for x in consequent)
        data['support'] = support
        data['confidence'] = confidence
        rule_string = Writer.dictformat(Writer.__rules_template, data)
        return rule_string
