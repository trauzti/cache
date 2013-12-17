# Modified from http://code.activestate.com/recipes/576532/
from collections import deque

class alg:
    def __repr__(self):
        return "ARC"

    def __init__(self, c):
        self.c = c        # Cache size
        self.cn = 0       # Items in cache now
        self.cached = {}  # Cached keys
        self.hitcount = 0
        self.count = 0
        self.p = 0
        self.t1 = deque()
        self.t2 = deque()
        self.b1 = deque()
        self.b2 = deque()

    def setup(self, reqlist):
                # I'm an online algorithm :-)
        pass

    def replace(self, args):
        if self.t1 and ((args in self.b2 and len(self.t1) == self.p) or (len(self.t1) > self.p)):
            old = self.t1.pop()
            self.b1.appendleft(old)
        else:
            old = self.t2.pop()
            self.b2.appendleft(old)
        del self.cached[old]

    def get(self, key):
        self.count += 1
        if key in self.t1:
            self.t1.remove(key)
            self.t2.appendleft(key)
            self.hitcount += 1
            return 1
        elif key in self.t2:
            self.t2.remove(key)
            self.t2.appendleft(key)
            self.hitcount += 1
            return 1
        return 0

    def put(self, key, val=1):
        if key in self.cached:
            return
        self.cached[key] = 1
        if key in self.b1:
            self.p = min(self.c, self.p + max(len(self.b2) / len(self.b1) , 1))
            self.replace(key)
            self.b1.remove(key)
            self.t2.appendleft(key)
            return
        if key in self.b2:
            self.p = max(0, self.p - max(len(self.b1)/len(self.b2) , 1))
            self.replace(key)
            self.b2.remove(key)
            self.t2.appendleft(key)
            return
        if len(self.t1) + len(self.b1) == self.c:
            if len(self.t1) < self.c:
                self.b1.pop()
                self.replace(key)
            else:
                del self.cached[self.t1.pop()]
        else:
            total = len(self.t1) + len(self.b1) + len(self.t2) + len(self.b2)
            if total >= self.c:
                if total == (2 * self.c):
                    self.b2.pop()
                self.replace(key)
        self.t1.appendleft(key)
