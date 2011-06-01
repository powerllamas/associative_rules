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
            resource.getrusage(resource.RUSAGE_SELF)
            pass

        def record_post_rules(self):
            pass

    Stats = StatsUnix
else:
    class StatsWin:
        def record_post_large_sets(self):
            pass

        def record_post_rules(self):
            pass

    Stats = StatsWin
