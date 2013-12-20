import random
import time

# Takes k random sample items from the cache and evicts the oldest item
# This is the same algorithm as allkeys-lru in Redis (there k=3 by default)

class alg:
    def __repr__(self):
        return "kRANDOM_LRU(k=%d)" % self.k

    def __init__(self, c, k=3):
        random.seed(1337)
        # c is cache size
        self.c = c
        self.k = k
        self.cn = 0
        self.cache = [] # (key)
        self.stored = {} # key => timestamp
        self.hitcount = 0
        self.count = 0

    def setup(self, reqlist):
        # I'm an online algorithm :-)
        pass

    def get(self, key):
        self.count += 1
        if key in self.stored:
            current_time = time.time()
            old_time = self.stored[key]
            assert old_time <= current_time
            self.stored[key] = current_time
            self.hitcount += 1
            return 1
        return 0

    def put(self, key, val=1):
        if key not in self.stored:
            current_time = time.time()
            if self.cn == self.c:
                # 0 <= is[0],...,is[self.k-1] <= self.cn-1
                ivals = [ random.randint(0, self.cn-1) for i in xrange(self.k) ]
                oldest_time = float("inf")
                oldest_key = None
                oldest_i = None
                for i in ivals:
                    o_key = self.cache[i]
                    o_time = self.stored[o_key]
                    if o_time < oldest_time:
                        oldest_i = i
                        oldest_time = o_time
                        oldest_key = o_key
                assert oldest_i != None
                assert oldest_key != None
                del self.stored[oldest_key]
                self.cache[oldest_i] = key
            else:
                self.cn += 1
                self.cache.append(key)
            self.stored[key] = current_time
