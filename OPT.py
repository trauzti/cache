from heapq import heappush, heappop

class alg:
    def __repr__(self):
        return "OPT"

    def __init__(self, c, **kwargs):
        self.c = c        # Cache size
        self.cn = 0       # Items in cache now
        self.stored = {}  # Stored keys
        self.heap = []    # (-dist, key, valid)
        self.hitcount = 0
        self.count = 0
        self.nextref = {}

    def getnextref(self, key):
        ne = float("inf")
        if self.nextref[key]:
            ne = self.nextref[key][-1]
        return ne

    def deletefurthest(self):
        valid = False
        delkey = None
        while not valid:
            deldist, delkey, valid = heappop(self.heap)
        realdeldist = -deldist
        item = self.stored[delkey]
        del self.stored[delkey]

    def setup(self, reqlist):
        # reqlist: (mode, key , size)
        index = len(reqlist) - 1
        for line in reversed(reqlist):
            key = line.replace("\n", "").split(" ")[0]
            self.nextref.setdefault(key, []).append(index)
            index -= 1
        assert index == -1


    def get(self, key, val=1):
        assert self.nextref[key]
        self.count += 1
        self.nextref[key].pop()
        if key in self.stored:
            old = self.stored[key]
            old[2] = False
            nr = self.getnextref(key)
            item = [-nr, key, True]
            self.stored[key] = item
            heappush(self.heap, item)
            self.hitcount += 1
            return 1
        return 0

    def put(self, key, val=1):
        if key not in self.stored:
            if self.cn == self.c:
                self.deletefurthest()
            else:
                self.cn += 1
            dist = self.getnextref(key)
            item  = [-dist, key, True]
            self.stored[key] = item
            heappush(self.heap, item)
