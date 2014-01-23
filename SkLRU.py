import sys

class Node:
    def __init__(self, key, val=None):
        self.key = key
        self.val = val
        self.next = None
        self.prev = None
        self.level = None

    def __repr__(self):
        return "Node(%s -> %s)" % (self.key, self.val)


# From: http://www.cs.cornell.edu/~qhuang/papers/sosp_fbanalysis.pdf
# Quadruply-segmented LRU. Four queues are maintained at levels 0 to 3. On a cache miss, the item is inserted at the head of
# queue 0. On a cache hit, the item is moved to the head of the next higher queue (items in queue 3 move to the head of queue 3).
# Each queue is allocated 1/4 of the total cache size and items are evicted from the tail of a queue to the head of the next lower
# queue to maintain the size invariants.
# IMPORTANT: Items evicted from queue 0 are evicted from the cache.
# This

# Question: Shouldn't we utilize the space efficiently? The bottom level should be able to use more than 25% of the space
# if the other levels are not full?
class alg:
    def __init__(self, c, k=4, **kwargs):
        # c is the cache size
        assert (c % 4) == 0 # just for simplicity
        self.queue_size = c / 4
        self.c = c
        self.cn = 0
        # head and tail for each level
        # levels go from 0 to numlevels-1

        # 0 is the bottom queue
        # numlevels -1 is the top queue
        self.numlevels = k
        self.bottom = 0
        self.top = k - 1
        self.heads = [None for i in xrange(k)]
        self.tails = [None for i in xrange(k)]
        self.sizes = [0 for i in xrange(k)]
        self.stored = {}
        self.hitcount = 0
        self.count = 0

    # Walks the list and asserts that links are correct
    def walk(self):
        for i in range(len(self.heads)):
            n = self.heads[i]
            s = "head(Level: %d, size=%d)" % (i, self.sizes[i])
            while n:
                s+= "->(%s)" % n.key
                if n.prev:
                    assert n.prev.next == n
                if n.next:
                    assert n.next.prev == n
                else:
                    break
                n = n.next
            s += "<- tail"
            assert n == self.tails[i]
            print s

    def __repr__(self):
        return "S%dLRU" % self.numlevels

    def setup(self, reqlist):
        # I'm an online algorithm :-)
        pass

    def unlink(self, n):
        for i in range(len(self.heads)):
            if n == self.heads[i]:
                self.heads[i] = n.next
            if n == self.tails[i]:
                #print "updating tail in unlink"
                self.tails[i] = n.prev
                pass
        self.sizes[n.level] -= 1
        if n.prev:
            n.prev.next = n.next
        if n.next:
            n.next.prev = n.prev
        n.prev = None
        n.next = None
        n.level = None

    def maintainSizes(self):
        i = self.top
        while i > 0:
            while self.sizes[i] > self.queue_size:
                n = self.evictFromLevel(i)
                #print "Moving %s from Level %d -> %d" % (n, i, i+1)
                self.insertAtLevel(n, i-1)
            i -= 1
        assert i == 0
        while self.sizes[i] > self.queue_size:
            n = self.evictFromLevel(self.bottom)
            del self.stored[n.key]
            #print "Evicting %s from cache" % n

    # Does not remove from the tail, just inserts at the head
    # Updates the lenghts array
    def insertAtLevel(self, n, level):
        oldhead = self.heads[level]
        n.level = level
        if not oldhead:
            self.heads[level] = n
            n.prev = None
            n.next = None
        else:
            oldhead.prev = n
            n.prev = None
            n.next = oldhead
            self.heads[level] = n

        oldtail = self.tails[level]
        if not oldtail:
            self.tails[level] = n
        else:
            pass
        self.sizes[level] += 1


    # put n at the LRU head of the level above
    # n has already been unlinked
    def upgradeLevel(self, n, levelTo):
        assert n.prev == None
        assert n.next == None
        self.insertAtLevel(n, levelTo)


    def evictFromLevel(self, level):
        n = self.tails[level]
        self.unlink(n)
        return n

    # usage x = get(key)
    # if the key is found in the cache, put it in the LRU head and return the value
    # else return None
    def get(self, key):
        self.count += 1
        if key in self.stored:
            self.hitcount += 1
            n = self.stored[key]
            levelTo = min(self.top, n.level+1)
            self.unlink(n)
            self.upgradeLevel(n, levelTo)
            self.maintainSizes()
            return n.val
        return None

    def put(self, key, val=1):
        if key not in self.stored:
            n = Node(key, val)
            self.stored[key] = n
            self.insertAtLevel(n, self.bottom) # insert into queue 0
        else:
            # Overwrite it correctly
            n = self.stored[key]
            n.val = val
            levelTo = max(0, n.level-1)
            self.unlink(n)
            self.upgradeLevel(n, levelTo)
        if n.level == None:
            from ipdb import set_trace; set_trace()
        self.maintainSizes()

    def print_statistics(self):
        print "Hit ratio: %.5f" % (self.hitcount / (0.0 + self.count))
