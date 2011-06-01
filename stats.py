# -*- coding: utf-8 -*-

import os


def is_posix():
    return os.name == 'posix'

class StatsBase:
    def __init__(self):
        self.real_time = 0.0
        self.user_time = 0.0
        self.set_gen_time = 0.0
        self.memory_use = 0

if is_posix():
    import resource

    class StatsUnix(StatsBase):
        def record_post_large_sets(self):
            usage = resource.getrusage(resource.RUSAGE_SELF)
            self.set_gen_time = usage.ru_utime + usage.ru_stime
            memory = usage.ru_maxrss * resource.getpagesize()
            self.memory_use = memory

        def record_post_rules(self):
            usage = resource.getrusage(resource.RUSAGE_SELF)
            self.real_time = usage.ru_utime + usage.ru_stime
            self.user_time = usage.ru_utime
            memory = usage.ru_maxrss * resource.getpagesize()
            self.memory_use = max(memory, self.memory_use)

    Stats = StatsUnix
else:
    class StatsWin:
        def record_post_large_sets(self):
            pass

        def record_post_rules(self):
            pass

    Stats = StatsWin
