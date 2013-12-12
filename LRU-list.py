class Node:
    def __init__(self, key):
        self.key = key
        self.next = None
        self.prev = None

    def __repr__(self):
        return "Node(%s)" % self.key


class alg:
    def walk(self):
        n = self.first
        while n:
            print n.key
            if n.next:
                assert n.next.prev == n
            if n.prev:
                assert n.prev.next == n
            n = n.next

    def __repr__(self):
        return "LRU"

    def __init__(self, c):
        # c is cache size
        self.c = c
        self.cn = 0
        self.first = None
        self.last = None
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
            n = self.stored[key]
            if n != self.first:
                if n == self.last:
                    self.last = n.prev
                else:
                    n.next.prev = n.prev # Unneccessary if last
                n.prev.next = n.next     # Unneccessary if first
                n.prev = None            #
                self.first.prev = n      # Put it in front
                n.next = self.first      # ...
                self.first = n           # Make it first


        else:
            self.put(key)

    def put(self, key):
        if key not in self.stored:
            n = Node(key)
            self.stored[key] = n
            n.next = self.first
            if self.first:
                self.first.prev = n
            self.first = n
            if self.cn == self.c:
                del self.stored[self.last.key]
                self.last = self.last.prev
                self.last.next = None
            else:
                self.cn += 1
                if not self.last:
                    self.last = n
