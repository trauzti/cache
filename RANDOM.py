from heapq import heappush, heappop
import random

class alg:
    def __repr__(self):
        return "RANDOM"

    def __init__(self, c, **kwargs):
        random.seed(1337)
        # c is cache size
        self.c = c
        self.cn = 0
        self.cache = []
        self.stored = {}
        self.hitcount = 0
        self.count = 0

    def setup(self, reqlist):
        # I'm an online algorithm :-)
        pass

    def get(self, key):
        self.count += 1
        if key in self.stored:
            self.hitcount += 1
            return 1
        return 0

    def put(self, key, val=1):
        if key not in self.stored:
            if self.cn == self.c:
                i = random.randint(0, self.cn-1) # 0 <= i <= (self.cn-1)
                evict_key = self.cache[i]
                del self.stored[evict_key]
                self.cache[i] = key
            else:
                self.cn += 1
                self.cache.append(key)
            self.stored[key] = 1
