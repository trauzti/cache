class alg:
    def __repr__(self):
        return "CLOCK"

    def __init__(self, c, **kwargs):
        # c is cache size
        self.c = c  # Max
        self.cn = 0 # Current
        self.hand = 0
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
            self.stored[key] = 1
            return 1
        return 0

    def put(self, key, val=1):
        if key not in self.stored:
            self.stored[key] = 1
            if self.cn == self.c:
                i = 0
                while 1:
                    assert i <= self.cn
                    item = self.cache[self.hand]
                    if self.stored[item] == 0:
                        del self.stored[item]
                        self.cache[self.hand] = key
                        self.stored[key] = 1
                        break
                    else:
                        self.stored[item] = 0
                    self.hand = (self.hand + 1) % self.cn
                    i += 1
            else:
                assert self.cn < self.c
                self.cache.append(key)
                self.cn += 1
