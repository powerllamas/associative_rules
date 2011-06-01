# -*- coding: utf-8 -*-

from collections import defaultdict
from string import Formatter

class Writer:
    __header_template = u"""
    Dane: {infile}
    Min sup: {minsup}
    Min conf: {minconf}
    No of rules: {nr_of_rules}
    Pamiec: {memory_use}
    Calkowity czas: {total_time}
    Czas bez we/wy: {user_time}
    Czas generowania zb. cz.: {set_gen_time}

    **RULES
    """

    __rules_template = u"""
    {nr}: {rule}
    Support: {sup}
    Confidence: {conf}
    """
    def __init__(self, filename=None):
        self.__filename = filename
        self.__data = defaultdict(lambda: u"<missing>")

    def add_rules(rules):
        pass

    def add_stats(stats):
        pass

    def add_args(self, args):
        self.__data['infile'] = args.infile
        self.__data['minsup'] = args.minsup
        self.__data['minconf'] = args.minconf

    def write(self):
        header = Writer.dictformat(self.__header_template, self.__data)
        if self.__filename is not None:
            with open(self.__filename, 'w') as file:
                file.write(header)
        else:
            print header

    @staticmethod
    def dictformat(string, dictionary):
        formatter = Formatter()
        return formatter.vformat(string, (), dictionary)
